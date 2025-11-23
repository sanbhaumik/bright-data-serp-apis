from serp_client import SerpClient

class CompetitiveIntelAgent:
    """
    Competitive Intelligence Agent powered by Bright Data SERP API

    Automatically gathers and synthesizes market intelligence by querying
    search engines for strategic business insights.
    """

    def __init__(self):
        self.serp = SerpClient()

    def research_company(self, domain):
        """
        Generate a competitive intelligence brief for a company

        Uses Bright Data SERP API to gather real-time market intelligence:
        - Market positioning and differentiation
        - Customer base and use cases
        - Strategic moves (funding, partnerships, launches)
        - Product strategy and recent developments

        Args:
            domain: Company domain (e.g., 'openai.com')

        Returns:
            dict: Structured intelligence report
        """

        print(f"\n🔍 Researching {domain}...")

        # SERP API Query 1: Market Positioning
        # Understand how the company positions itself vs competitors
        print("  → Analyzing market position...")
        positioning = self.serp.get_multiple_results(
            f'{domain} vs competitors',
            count=3
        )

        # SERP API Query 2: Customer Intelligence
        # Discover who uses their product and why
        print("  → Identifying customer base...")
        customers = self.serp.get_multiple_results(
            f'{domain} customers case study',
            count=3
        )

        # SERP API Query 3: Strategic Moves
        # Track funding, acquisitions, partnerships
        print("  → Tracking strategic moves...")
        strategic_moves = self.serp.get_multiple_results(
            f'{domain} funding OR acquisition OR partnership',
            count=3
        )

        # SERP API Query 4: Product Strategy
        # Monitor product launches and feature announcements
        print("  → Monitoring product developments...")
        product_news = self.serp.get_multiple_results(
            f'{domain} product launch OR new feature',
            count=3
        )

        # Synthesize intelligence
        return {
            "domain": domain,
            "positioning": positioning,
            "customers": customers,
            "strategic_moves": strategic_moves,
            "product_strategy": product_news,
            "intelligence_summary": self._generate_summary(
                domain, positioning, customers, strategic_moves, product_news
            )
        }

    def _generate_summary(self, domain, positioning, customers, strategic_moves, product_news):
        """Generate executive summary from gathered intelligence"""

        summary = {
            "market_position": self._extract_key_insight(positioning, "competitive positioning"),
            "key_customers": self._extract_key_insight(customers, "customer adoption"),
            "recent_moves": self._extract_key_insight(strategic_moves, "strategic activity"),
            "product_focus": self._extract_key_insight(product_news, "product innovation"),
        }

        return summary

    def _extract_key_insight(self, results, category):
        """Extract the most relevant insight from search results"""
        if not results:
            return f"No recent {category} data found"

        # Get the first result's title and description
        top_result = results[0]
        title = top_result.get('title', '')
        description = top_result.get('description', '')

        # Combine for insight - use full description for better intelligence
        if title and description and description != 'Description not available':
            # Include full description (up to 400 chars for readability)
            return f"{title} - {description[:400]}"
        elif title:
            return title
        elif description:
            return description[:400]
        else:
            return f"Limited {category} intelligence available"