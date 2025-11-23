"""
Competitive Intelligence Agent - Powered by Bright Data SERP API

Automatically research competitors and generate intelligence reports
by leveraging real-time search engine data.
"""

import json
from enrichment_agent import CompetitiveIntelAgent
from pdf_generator import IntelligencePDFGenerator


def format_intelligence_report(intel):
    """
    Format intelligence data into a readable report

    Args:
        intel: Intelligence dict from CompetitiveIntelAgent

    Returns:
        str: Formatted markdown report
    """
    domain = intel['domain']
    summary = intel['intelligence_summary']

    report = f"""
{'='*70}
COMPETITIVE INTELLIGENCE BRIEF: {domain.upper()}
{'='*70}

📊 MARKET POSITION
{summary['market_position']}

👥 KEY CUSTOMERS & USE CASES
{summary['key_customers']}

🚀 RECENT STRATEGIC MOVES
{summary['recent_moves']}

💡 PRODUCT STRATEGY
{summary['product_focus']}

{'='*70}
DETAILED FINDINGS
{'='*70}

## Competitive Positioning ({len(intel['positioning'])} sources)
"""

    for i, result in enumerate(intel['positioning'], 1):
        report += f"\n{i}. {result['title']}\n"
        report += f"   🔗 {result['url']}\n"
        report += f"   {result['description']}\n"

    report += "\n## Customer Intelligence ({} sources)\n".format(len(intel['customers']))
    for i, result in enumerate(intel['customers'], 1):
        report += f"\n{i}. {result['title']}\n"
        report += f"   🔗 {result['url']}\n"
        report += f"   {result['description']}\n"

    report += "\n## Strategic Activity ({} sources)\n".format(len(intel['strategic_moves']))
    for i, result in enumerate(intel['strategic_moves'], 1):
        report += f"\n{i}. {result['title']}\n"
        report += f"   🔗 {result['url']}\n"
        report += f"   {result['description']}\n"

    report += "\n## Product Developments ({} sources)\n".format(len(intel['product_strategy']))
    for i, result in enumerate(intel['product_strategy'], 1):
        report += f"\n{i}. {result['title']}\n"
        report += f"   🔗 {result['url']}\n"
        report += f"   {result['description']}\n"

    report += f"\n{'='*70}\n"
    report += "Generated using Bright Data SERP API\n"
    report += f"{'='*70}\n"

    return report


def research_competitors(domains, output_format='text', generate_pdf=True):
    """
    Research multiple competitors and generate intelligence reports

    Args:
        domains: List of company domains to research
        output_format: 'text' for terminal output, 'json' for structured data, 'pdf' for PDF only
        generate_pdf: Whether to generate PDF report (default: True)

    Returns:
        list: Intelligence reports for each domain
    """
    print("="*70)
    print("🔬 COMPETITIVE INTELLIGENCE AGENT")
    print("   Powered by Bright Data SERP API")
    print("="*70)
    print(f"\n📋 Researching {len(domains)} competitor(s)...\n")

    agent = CompetitiveIntelAgent()
    reports = []

    for domain in domains:
        try:
            intel = agent.research_company(domain)
            reports.append(intel)

            if output_format == 'text':
                print(format_intelligence_report(intel))
            elif output_format == 'json':
                print(json.dumps(intel, indent=2))

        except Exception as e:
            print(f"\n❌ Error researching {domain}: {e}\n")
            continue

    print(f"\n✅ Successfully generated {len(reports)} intelligence report(s)")

    # Generate PDF report if requested
    if generate_pdf and reports:
        print("\n📄 Generating PDF report...")
        pdf_generator = IntelligencePDFGenerator()

        # Create filename based on companies researched
        if len(domains) == 1:
            pdf_filename = f"{domains[0].replace('.', '_')}_intelligence_report.pdf"
        else:
            pdf_filename = "competitive_intelligence_report.pdf"

        pdf_path = pdf_generator.generate_report(reports, pdf_filename)
        print(f"✅ PDF report saved to: {pdf_path}")

    return reports


if __name__ == "__main__":
    # Example: Research competitors
    # You can pass one or more company domains
    competitors = [
        "openai.com"
    ]

    # Generate intelligence reports with PDF output
    reports = research_competitors(
        competitors,
        output_format='text',  # Options: 'text', 'json', 'pdf'
        generate_pdf=True      # Set to True to generate PDF report
    )

    # Optionally save as JSON
    with open('intelligence_reports.json', 'w') as f:
        json.dump(reports, f, indent=2)
        print("💾 JSON data saved to intelligence_reports.json")