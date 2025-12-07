# 🔬 Competitive Intelligence Agent

**Automate competitive research with Bright Data SERP API**

Turn Google search results into actionable business intelligence. This lightweight Python agent automatically gathers market positioning, customer insights, strategic moves, and product developments for any competitor.

---

## 🎯 What It Does

Give it a competitor's domain → Get a comprehensive intelligence brief in seconds.

The agent automatically researches:
- **Market Positioning**: How they position themselves vs competitors
- **Customer Intelligence**: Who uses their product and why
- **Strategic Moves**: Funding rounds, acquisitions, partnerships
- **Product Strategy**: Recent launches and feature announcements

---

## ⚡ Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure SERP API Credentials

**Important:** Never commit your API credentials to version control!

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` with your actual credentials:

```bash
# .env
SERP_API_KEY=your_bright_data_api_key
SERP_ZONE=your_serp_zone

# Optional: Override defaults
DEFAULT_COUNTRY=us
DEFAULT_LANGUAGE=en
```

The `.env` file is automatically excluded from git via `.gitignore`.

### 3. Run Intelligence Gathering

```bash
python main.py
```

---

## 🚀 Example Usage

### Generate PDF Reports

```python
from main import research_competitors

# Research one or more competitors
competitors = ["snowflake.com", "databricks.com"]

# Generate intelligence reports with PDF output
reports = research_competitors(
    competitors,
    output_format='text',  # 'text', 'json', or 'pdf'
    generate_pdf=True      # Creates professional PDF report
)
```

### Programmatic Usage

```python
from enrichment_agent import CompetitiveIntelAgent

agent = CompetitiveIntelAgent()
intel = agent.research_company("openai.com")

# Get structured intelligence report
print(intel['intelligence_summary'])
```

**Terminal Output:**

```
======================================================================
COMPETITIVE INTELLIGENCE BRIEF: OPENAI.COM
======================================================================

📊 MARKET POSITION
OpenAI vs Google Gemini: Which AI Model is Better? - Comprehensive
comparison of capabilities, pricing, and market positioning...

👥 KEY CUSTOMERS & USE CASES
Major Enterprise Customers Using ChatGPT - Morgan Stanley, Salesforce,
and Khan Academy leverage OpenAI for automation and content generation...

🚀 RECENT STRATEGIC MOVES
OpenAI Closes $10B Funding Round Led by Microsoft - Strategic partnership
expands Azure integration and enterprise capabilities...

💡 PRODUCT STRATEGY
GPT-4o Launch Brings Multimodal Capabilities - New model processes text,
images, and audio with improved speed and cost efficiency...
```

---

## 🔧 How It Works

### Powered by Bright Data SERP API

The agent makes **4 targeted search queries** per competitor:

```python
# Query 1: Competitive positioning
self.serp.get_multiple_results(f'{domain} vs competitors', count=3)

# Query 2: Customer intelligence
self.serp.get_multiple_results(f'{domain} customers case study', count=3)

# Query 3: Strategic activity
self.serp.get_multiple_results(f'{domain} funding OR acquisition', count=3)

# Query 4: Product developments
self.serp.get_multiple_results(f'{domain} product launch', count=3)
```

### Why Bright Data SERP API?

✅ **Reliable**: Handles proxy rotation, CAPTCHA solving, rate limiting automatically
✅ **Global**: Search from any country with geo-targeting (`gl` parameter)
✅ **Structured**: Returns clean JSON responses with parsed HTML
✅ **Fast**: Real-time search results without blocks or throttling

---

## 📊 Code Structure

```
competition_research_agent/
├── config.py              # SERP API credentials
├── serp_client.py         # Bright Data SERP API wrapper
├── enrichment_agent.py    # Intelligence gathering logic
├── pdf_generator.py       # PDF report generation
├── main.py                # CLI interface & report formatting
└── requirements.txt       # Dependencies (requests, reportlab)
```

**Total: ~350 lines of Python** - Simple, focused, production-ready.

---

## 🎨 Customization

### Research Different Companies

Edit `main.py`:

```python
competitors = [
    "openai.com",
    "anthropic.com",
    "cohere.ai"
]

reports = research_competitors(competitors)
```

### Add Custom Queries

Extend `enrichment_agent.py`:

```python
# Add pricing intelligence
pricing = self.serp.get_multiple_results(
    f'{domain} pricing plans',
    count=3
)
```

### Change Output Format

```python
# JSON output instead of text report
reports = research_competitors(domains, output_format='json')

# Generate PDF only (no terminal output)
reports = research_competitors(domains, output_format='pdf', generate_pdf=True)

# Terminal output without PDF
reports = research_competitors(domains, output_format='text', generate_pdf=False)
```

---

## 🔍 Use Cases

### Sales & Business Development
- Research prospects before outreach calls
- Understand customer pain points and use cases
- Track competitor product launches

### Product Strategy
- Monitor competitor feature announcements
- Identify market gaps and opportunities
- Benchmark positioning strategies

### Market Research
- Analyze funding trends and strategic moves
- Map competitive landscape dynamics
- Track industry partnerships

### Investor Intelligence
- Due diligence on investment targets
- Track portfolio company competitors
- Monitor market momentum signals

---

## 🛠️ Technical Details

### SERP API Integration

The `SerpClient` class wraps Bright Data's SERP API:

```python
payload = {
    "zone": self.zone,
    "url": f"https://www.google.com/search?q={query}&gl=US&hl=en",
    "format": "json"
}

response = requests.post(
    "https://api.brightdata.com/request",
    json=payload,
    headers={"Authorization": f"Bearer {self.api_key}"}
)
```

### Result Parsing

Extracts structured data from HTML responses:

```python
{
    "title": "Company vs Competitors - Market Analysis",
    "url": "https://example.com/analysis",
    "description": "Detailed comparison of market positioning..."
}
```

### Error Handling

Gracefully handles API errors, parsing failures, and missing data.

---

## 📈 Performance

- **Speed**: ~10-15 seconds per competitor (4 queries)
- **Cost**: ~4 SERP API calls per company researched
- **Scalability**: Batch process 10-100+ competitors
- **Accuracy**: Multiple sources per insight (reduces noise)

---

## 🚧 Limitations & Future Improvements

### Current Limitations
- HTML parsing may miss some result types (ads, featured snippets)
- Limited to Google search (could add Bing, DuckDuckGo)
- No temporal analysis (trends over time)

### Potential Enhancements
- Add sentiment analysis on reviews
- Track changes over time (weekly reports)
- Compare 2+ competitors side-by-side
- Export to PDF/PowerPoint
- Add LLM summarization for deeper insights

---

## 📚 Learn More

- [Bright Data SERP API Documentation](https://docs.brightdata.com/serp-api)
- [Sign up for SERP API access](https://get.brightdata.com/2039fnr15xfy)
- [Example use cases](https://brightdata.com/use-cases)

---

## 🤝 Contributing

This is a reference implementation showcasing Bright Data SERP API capabilities. Feel free to:
- Fork and customize for your use case
- Share feedback on the implementation
- Submit improvements or bug fixes

---

## 📄 License

MIT License - Use freely for commercial or personal projects.

---

## 🎯 Key Takeaway

**With Bright Data SERP API, you can build production-ready competitive intelligence tools in an afternoon.**

This agent demonstrates:
- ✅ Simple API integration (< 50 lines of code)
- ✅ Real business value (actionable intelligence)
- ✅ Clean, maintainable architecture
- ✅ Ready for production scaling

**Ready to build your own SERP-powered tools?**
Get started at [brightdata.com](https://brightdata.com)
