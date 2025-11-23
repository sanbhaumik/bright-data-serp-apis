"""
PDF Report Generator for Competitive Intelligence

Generates professional PDF reports from intelligence data
gathered by the Competitive Intelligence Agent.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from datetime import datetime


class IntelligencePDFGenerator:
    """Generate professional PDF reports from competitive intelligence data"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Create custom paragraph styles for the report"""

        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Company name style
        self.styles.add(ParagraphStyle(
            name='CompanyName',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=HexColor('#2563eb'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))

        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=HexColor('#1a1a1a'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        ))

        # Insight style
        self.styles.add(ParagraphStyle(
            name='Insight',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=HexColor('#4a5568'),
            spaceAfter=8,
            leftIndent=20,
            fontName='Helvetica'
        ))

        # Source style
        self.styles.add(ParagraphStyle(
            name='Source',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=HexColor('#718096'),
            spaceAfter=4,
            leftIndent=30,
            fontName='Helvetica-Oblique'
        ))

        # Footer style
        self.styles.add(ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=HexColor('#a0aec0'),
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))

    def generate_report(self, intelligence_data, filename='competitive_intelligence_report.pdf'):
        """
        Generate a PDF report from intelligence data

        Args:
            intelligence_data: List of intelligence dicts (one per company)
            filename: Output PDF filename

        Returns:
            str: Path to generated PDF file
        """
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        # Build the report content
        story = []

        # Add title page
        story.extend(self._build_title_page(intelligence_data))
        story.append(PageBreak())

        # Add intelligence briefs for each company
        for i, intel in enumerate(intelligence_data):
            story.extend(self._build_company_brief(intel))
            if i < len(intelligence_data) - 1:
                story.append(PageBreak())

        # Build PDF
        doc.build(story)
        return filename

    def _build_title_page(self, intelligence_data):
        """Build the title page"""
        story = []

        # Add spacing
        story.append(Spacer(1, 1.5*inch))

        # Title
        title = Paragraph(
            "Competitive Intelligence Report",
            self.styles['CustomTitle']
        )
        story.append(title)
        story.append(Spacer(1, 0.3*inch))

        # Subtitle with company count
        company_count = len(intelligence_data)
        companies = ', '.join([intel['domain'] for intel in intelligence_data])

        subtitle = Paragraph(
            f"Analysis of {company_count} Competitor{'s' if company_count > 1 else ''}",
            self.styles['Heading2']
        )
        story.append(subtitle)
        story.append(Spacer(1, 0.5*inch))

        # Companies analyzed
        companies_text = Paragraph(
            f"<b>Companies:</b> {companies}",
            self.styles['Normal']
        )
        story.append(companies_text)
        story.append(Spacer(1, 0.3*inch))

        # Report metadata
        date_text = Paragraph(
            f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            self.styles['Normal']
        )
        story.append(date_text)
        story.append(Spacer(1, 0.1*inch))

        powered_by = Paragraph(
            "<b>Powered by:</b> Bright Data SERP API",
            self.styles['Normal']
        )
        story.append(powered_by)

        return story

    def _build_company_brief(self, intel):
        """Build intelligence brief for a single company"""
        story = []

        # Company name header
        company_header = Paragraph(
            f"🏢 {intel['domain'].upper()}",
            self.styles['CompanyName']
        )
        story.append(company_header)
        story.append(Spacer(1, 0.2*inch))

        # Executive Summary
        story.append(Paragraph("📊 Executive Summary", self.styles['SectionHeader']))

        summary = intel['intelligence_summary']

        # Market Position
        story.append(Paragraph("<b>Market Position:</b>", self.styles['Normal']))
        story.append(Paragraph(summary['market_position'], self.styles['Insight']))

        # Key Customers
        story.append(Paragraph("<b>Key Customers & Use Cases:</b>", self.styles['Normal']))
        story.append(Paragraph(summary['key_customers'], self.styles['Insight']))

        # Strategic Moves
        story.append(Paragraph("<b>Recent Strategic Moves:</b>", self.styles['Normal']))
        story.append(Paragraph(summary['recent_moves'], self.styles['Insight']))

        # Product Strategy
        story.append(Paragraph("<b>Product Strategy:</b>", self.styles['Normal']))
        story.append(Paragraph(summary['product_focus'], self.styles['Insight']))

        story.append(Spacer(1, 0.3*inch))

        # Detailed Findings
        story.append(Paragraph("📋 Detailed Findings", self.styles['SectionHeader']))

        # Competitive Positioning
        story.extend(self._build_findings_section(
            "Competitive Positioning",
            intel['positioning']
        ))

        # Customer Intelligence
        story.extend(self._build_findings_section(
            "Customer Intelligence",
            intel['customers']
        ))

        # Strategic Activity
        story.extend(self._build_findings_section(
            "Strategic Activity",
            intel['strategic_moves']
        ))

        # Product Developments
        story.extend(self._build_findings_section(
            "Product Developments",
            intel['product_strategy']
        ))

        return story

    def _build_findings_section(self, section_title, results):
        """Build a findings section with sources"""
        story = []

        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph(
            f"<b>{section_title}</b> ({len(results)} sources)",
            self.styles['Normal']
        ))

        for i, result in enumerate(results, 1):
            # Title
            title_text = f"{i}. {result['title']}"
            story.append(Paragraph(title_text, self.styles['Insight']))

            # URL (if available)
            if result['url'] and result['url'] != 'No URL':
                url_text = f"🔗 <link href='{result['url']}'>{result['url'][:80]}...</link>"
                story.append(Paragraph(url_text, self.styles['Source']))

            # Description (if available)
            if result['description'] and result['description'] != 'No description available':
                desc_text = result['description'][:200]
                story.append(Paragraph(desc_text, self.styles['Source']))

            story.append(Spacer(1, 0.1*inch))

        return story
