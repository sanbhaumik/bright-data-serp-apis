import requests
from urllib.parse import quote_plus
from config import API_KEY, ZONE, DEFAULT_COUNTRY, DEFAULT_LANGUAGE

class SerpClient:
    """Client for querying Bright Data SERP API"""
    
    def __init__(self):
        self.api_key = API_KEY
        self.zone = ZONE
        self.base_url = "https://api.brightdata.com/request"
    
    def query(self, keyword, gl=DEFAULT_COUNTRY, hl=DEFAULT_LANGUAGE):
        """
        Query search engines for real-time business intelligence

        Args:
            keyword: Search query string
            gl: Geographic location (country code)
            hl: Language code

        Returns:
            dict: Parsed JSON response from SERP API
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "zone": self.zone,
            "url": f"https://www.google.com/search?q={quote_plus(keyword)}&gl={gl.upper()}&hl={hl}",
            "format": "json"
        }

        response = requests.post(self.base_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_multiple_results(self, keyword, count=3):
        """
        Extract multiple search results from SERP API response

        Bright Data SERP API returns structured HTML that we parse to extract:
        - Result titles
        - URLs
        - Descriptions/snippets

        Args:
            keyword: Search query
            count: Number of results to extract (default: 3)

        Returns:
            list: List of dicts with title, url, description
        """
        import re
        from html import unescape
        from html.parser import HTMLParser

        response = self.query(keyword)
        html_content = response.get('body', '')

        if not html_content:
            return []

        results = []

        # More comprehensive extraction patterns
        # Pattern 1: Extract all h3 titles (result titles)
        title_pattern = r'<h3[^>]*class="[^"]*"[^>]*>(.*?)</h3>'
        titles = re.findall(title_pattern, html_content, re.DOTALL)

        # Pattern 2: Extract URLs from links
        url_pattern = r'<a[^>]*href="(/url\?q=|/search\?q=)?(https?://[^"&]+)'
        url_matches = re.findall(url_pattern, html_content)

        # Pattern 3: Extract descriptions - look for common snippet patterns
        # Google uses various div patterns for snippets
        snippet_patterns = [
            r'<div[^>]*data-sncf="[^"]*"[^>]*>(.*?)</div>',
            r'<div[^>]*class="[^"]*VwiC3b[^"]*"[^>]*>(.*?)</div>',
            r'<span[^>]*class="[^"]*st[^"]*"[^>]*>(.*?)</span>',
            r'<div[^>]*style="[^"]*"[^>]*>([^<]{100,500})</div>',
        ]

        snippets = []
        for pattern in snippet_patterns:
            found = re.findall(pattern, html_content, re.DOTALL)
            snippets.extend(found)
            if len(snippets) >= count * 2:
                break

        # Clean and process extracted data
        def clean_text(text):
            """Remove HTML tags and clean text"""
            # Remove all HTML tags
            text = re.sub(r'<[^>]+>', '', text)
            # Decode HTML entities
            text = unescape(text)
            # Remove extra whitespace
            text = ' '.join(text.split())
            return text.strip()

        # Process titles
        clean_titles = [clean_text(t) for t in titles if clean_text(t)]

        # Process URLs
        clean_urls = []
        for url_match in url_matches:
            url = url_match[1] if url_match[0] else url_match[1]
            # Filter out Google's own URLs
            if not any(x in url for x in ['google.com', 'gstatic.com', 'youtube.com/redirect']):
                clean_urls.append(unescape(url))

        # Process snippets
        clean_snippets = []
        for snippet in snippets:
            cleaned = clean_text(snippet)
            # Only include snippets with substantial content
            if len(cleaned) > 50 and len(cleaned) < 500:
                # Filter out common non-content patterns
                if not any(x in cleaned.lower() for x in ['javascript', 'cookie', 'sign in', 'log in']):
                    clean_snippets.append(cleaned)

        # Combine results intelligently
        for i in range(min(count, len(clean_titles))):
            title = clean_titles[i] if i < len(clean_titles) else None
            url = clean_urls[i] if i < len(clean_urls) else None
            description = clean_snippets[i] if i < len(clean_snippets) else None

            # Only add if we have at least a title
            if title and len(title) > 5:
                results.append({
                    'title': title,
                    'url': url if url else 'URL not available',
                    'description': description if description else 'Description not available'
                })

        # If we didn't get enough results, try a simpler fallback
        if len(results) < count:
            # Look for any substantial text blocks
            text_blocks = re.findall(r'>([^<]{80,400})<', html_content)
            for i, block in enumerate(text_blocks[:count]):
                if len(results) >= count:
                    break
                cleaned = clean_text(block)
                if cleaned and len(cleaned) > 50:
                    results.append({
                        'title': cleaned[:100] + '...',
                        'url': 'URL not available',
                        'description': cleaned
                    })

        return results[:count]

    def get_top_result(self, keyword, field='url'):
        """
        Legacy method: Extract single field from top result
        Kept for backward compatibility
        """
        results = self.get_multiple_results(keyword, count=1)
        if not results:
            return '-'

        return results[0].get(field, '-')