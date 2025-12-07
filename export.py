"""
Export Utilities: PDF Report Generation
Generates branded PDF reports for indication expansion analysis
"""

import io
from datetime import datetime
from fpdf import FPDF
from pathlib import Path

# =============================================================================
# BRAND COLOURS (RGB for PDF)
# =============================================================================
DEEP_BLUE_RGB = (10, 30, 74)
VIOLET_RGB = (162, 77, 190)
MAGENTA_PINK_RGB = (224, 79, 138)
LIGHT_BLUE_RGB = (179, 224, 242)
SOFT_LAVENDER_RGB = (227, 217, 242)
WHITE_RGB = (255, 255, 255)


class ExcelraPDF(FPDF):
    """Custom PDF class with Excelra branding."""
    
    def __init__(self, logo_path: str = None):
        super().__init__()
        self.logo_path = logo_path
        
    def header(self):
        """Add branded header to each page."""
        # Header background
        self.set_fill_color(*LIGHT_BLUE_RGB)
        self.rect(0, 0, 210, 25, 'F')
        
        # Logo (if available)
        if self.logo_path and Path(self.logo_path).exists():
            self.image(self.logo_path, 10, 5, 30)
        
        # Title
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(*DEEP_BLUE_RGB)
        self.set_xy(45, 8)
        self.cell(0, 5, 'Indication Expansion Analysis', 0, 0, 'L')
        
        # Subtitle
        self.set_font('Helvetica', '', 9)
        self.set_text_color(*VIOLET_RGB)
        self.set_xy(45, 14)
        self.cell(0, 5, 'Powered by Excelra GRIP Platform', 0, 0, 'L')
        
        self.ln(25)
    
    def footer(self):
        """Add branded footer to each page."""
        self.set_y(-20)
        
        # Footer line
        self.set_draw_color(*VIOLET_RGB)
        self.line(10, self.get_y(), 200, self.get_y())
        
        # Footer text
        self.set_font('Helvetica', '', 8)
        self.set_text_color(*DEEP_BLUE_RGB)
        self.ln(3)
        self.cell(0, 5, 'www.excelra.com | Where data means more', 0, 0, 'C')
        
        # Page number
        self.set_xy(-30, -15)
        self.cell(0, 5, f'Page {self.page_no()}', 0, 0, 'R')
    
    def section_title(self, title: str):
        """Add a section title."""
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(*DEEP_BLUE_RGB)
        self.ln(5)
        self.cell(0, 10, title, 0, 1, 'L')
        
        # Underline
        self.set_draw_color(*VIOLET_RGB)
        self.line(10, self.get_y(), 80, self.get_y())
        self.ln(5)
    
    def subsection_title(self, title: str):
        """Add a subsection title."""
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(*VIOLET_RGB)
        self.ln(3)
        self.cell(0, 8, title, 0, 1, 'L')
    
    def body_text(self, text: str):
        """Add body text."""
        self.set_font('Helvetica', '', 10)
        self.set_text_color(*DEEP_BLUE_RGB)
        self.multi_cell(0, 5, text)
    
    def metric_box(self, label: str, value: str, x: float, y: float, width: float = 45):
        """Draw a metric box."""
        # Box background
        self.set_fill_color(*SOFT_LAVENDER_RGB)
        self.rect(x, y, width, 20, 'F')
        
        # Border
        self.set_draw_color(*VIOLET_RGB)
        self.rect(x, y, width, 20, 'D')
        
        # Value
        self.set_xy(x, y + 2)
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(*VIOLET_RGB)
        self.cell(width, 8, str(value), 0, 0, 'C')
        
        # Label
        self.set_xy(x, y + 11)
        self.set_font('Helvetica', '', 7)
        self.set_text_color(*DEEP_BLUE_RGB)
        self.cell(width, 5, label, 0, 0, 'C')


def generate_indication_discovery_pdf(
    target: str,
    freq_df,
    logo_path: str = None
) -> bytes:
    """Generate PDF report for Indication Discovery analysis."""
    
    pdf = ExcelraPDF(logo_path)
    pdf.add_page()
    
    # Title
    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(*DEEP_BLUE_RGB)
    pdf.cell(0, 15, f'Indication Discovery Report: {target}', 0, 1, 'C')
    
    # Date
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(*VIOLET_RGB)
    pdf.cell(0, 5, f'Generated: {datetime.now().strftime("%d %B %Y")}', 0, 1, 'C')
    pdf.ln(10)
    
    # Executive Summary
    pdf.section_title('Executive Summary')
    
    total = len(freq_df)
    validated = len(freq_df[freq_df['relevancy'] == 'Yes'])
    partial = len(freq_df[freq_df['relevancy'] == 'Partial'])
    max_score = freq_df['frequency_score'].max()
    avg_score = freq_df['frequency_score'].mean()
    
    summary_text = f"""Using Excelra's multi-source approach, we have systematically identified {total} potential indications for {target} inhibitor expansion. Each indication has been scored across 9 scientific approaches and validated against published literature.

Of the {total} indications identified, {validated} show high-confidence validation with strong clinical or preclinical evidence, while {partial} show partial evidence requiring further validation."""
    
    pdf.body_text(summary_text)
    pdf.ln(5)
    
    # Metrics
    y_pos = pdf.get_y()
    pdf.metric_box('Total Indications', str(total), 10, y_pos, 35)
    pdf.metric_box('Validated', str(validated), 50, y_pos, 35)
    pdf.metric_box('Partial', str(partial), 90, y_pos, 35)
    pdf.metric_box('Top Score', f'{max_score}/9', 130, y_pos, 35)
    pdf.metric_box('Avg Score', f'{avg_score:.1f}/9', 170, y_pos, 35)
    
    pdf.ln(30)
    
    # Top Indications Table
    pdf.section_title('Top Ranked Indications')
    
    # Table header
    pdf.set_fill_color(*VIOLET_RGB)
    pdf.set_text_color(*WHITE_RGB)
    pdf.set_font('Helvetica', 'B', 9)
    
    col_widths = [60, 45, 25, 30, 30]
    headers = ['Indication', 'Therapeutic Area', 'Score', 'Validation', 'Evidence']
    
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 8, header, 1, 0, 'C', True)
    pdf.ln()
    
    # Table rows (top 10)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(*DEEP_BLUE_RGB)
    
    top_indications = freq_df.head(10)
    
    for _, row in top_indications.iterrows():
        # Alternate row colours
        pdf.set_fill_color(*SOFT_LAVENDER_RGB)
        
        pdf.cell(col_widths[0], 7, str(row['indication_name'])[:35], 1, 0, 'L')
        pdf.cell(col_widths[1], 7, str(row['therapeutic_area'])[:25], 1, 0, 'L')
        pdf.cell(col_widths[2], 7, f"{row['frequency_score']}/9", 1, 0, 'C')
        pdf.cell(col_widths[3], 7, str(row['relevancy']), 1, 0, 'C')
        
        # Count evidence sources
        evidence_count = sum([row.get(col, 0) for col in [
            'literature_mining', 'clinical_trials', 'structure_similarity',
            'adverse_events', 'gene_expression', 'disease_gene_signature',
            'drug_disease_signature', 'interactome', 'gwas'
        ] if col in row.index])
        pdf.cell(col_widths[4], 7, f'{evidence_count}/9', 1, 0, 'C')
        pdf.ln()
    
    # Methodology
    pdf.add_page()
    pdf.section_title('Methodology')
    
    methodology_text = """This analysis integrates evidence from nine complementary scientific approaches:

1. Literature Mining - Systematic extraction of target-disease associations from published literature
2. Clinical Trials - Analysis of clinical trial data for related compounds and mechanisms
3. Structure Similarity - Identification of indications from structurally similar compounds
4. Adverse Events - Mining of adverse event databases for therapeutic signal detection
5. Gene Expression - Analysis of disease-specific gene expression signatures
6. Disease-Gene Signatures - Matching of target biology to disease molecular profiles
7. Drug-Disease Signatures - Connectivity mapping between drug and disease signatures
8. Interactome Analysis - Network-based prediction using protein-protein interactions
9. GWAS - Genetic association evidence from genome-wide studies

Each indication receives a frequency score (1-9) based on the number of approaches providing supporting evidence."""
    
    pdf.body_text(methodology_text)
    
    # Next Steps
    pdf.ln(10)
    pdf.section_title('Recommended Next Steps')
    
    next_steps = """1. Review the top-ranked indications with your research and business development teams

2. Select 3-5 priority indications for deep-dive analysis including:
   - Detailed biological rationale
   - Competitive landscape assessment
   - Clinical development considerations
   - Commercial opportunity sizing

3. Contact Excelra to commission comprehensive indication dossiers with primary literature review, KOL insights, and detailed competitive intelligence.

For more information, visit www.excelra.com or contact your Excelra representative."""
    
    pdf.body_text(next_steps)
    
    # Return PDF bytes
    return pdf.output()


def generate_deep_dive_pdf(
    target: str,
    indication: str,
    dossier_data: dict,
    logo_path: str = None
) -> bytes:
    """Generate PDF report for Deep-Dive Analysis."""
    
    pdf = ExcelraPDF(logo_path)
    pdf.add_page()
    
    # Title
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(*DEEP_BLUE_RGB)
    pdf.cell(0, 12, f'Indication Dossier: {indication}', 0, 1, 'C')
    
    # Subtitle
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(*VIOLET_RGB)
    pdf.cell(0, 6, f'{target} Inhibitor Expansion Opportunity', 0, 1, 'C')
    
    # Date
    pdf.set_font('Helvetica', '', 9)
    pdf.cell(0, 5, f'Generated: {datetime.now().strftime("%d %B %Y")}', 0, 1, 'C')
    pdf.ln(8)
    
    # Key Metrics
    y_pos = pdf.get_y()
    pdf.metric_box('Evidence Score', f"{dossier_data['frequency_score']}/9", 10, y_pos, 45)
    pdf.metric_box('Validation', dossier_data['validation_status'], 60, y_pos, 45)
    pdf.metric_box('Unmet Need', dossier_data['unmet_need'], 110, y_pos, 45)
    pdf.metric_box('Market Size', dossier_data['market_size'].replace(' by', '\n'), 160, y_pos, 45)
    
    pdf.ln(30)
    
    # Biological Rationale
    pdf.section_title('Biological Rationale')
    
    # Clean up the rationale text
    rationale = dossier_data['biological_rationale'].strip()
    rationale = rationale.replace('**', '').replace('•', '-')
    pdf.body_text(rationale)
    
    # Evidence Summary
    pdf.add_page()
    pdf.section_title('Evidence Summary')
    
    for item in dossier_data['key_evidence']:
        pdf.subsection_title(item['source'])
        pdf.body_text(f"{item['finding']} (Confidence: {item['confidence']})")
        pdf.ln(2)
    
    # Competitive Landscape
    pdf.ln(5)
    pdf.section_title('Competitive Landscape')
    
    if dossier_data['competitive_context']:
        pdf.set_font('Helvetica', 'B', 9)
        pdf.set_fill_color(*VIOLET_RGB)
        pdf.set_text_color(*WHITE_RGB)
        
        col_widths = [50, 50, 40, 50]
        headers = ['Company', 'Drug', 'Phase', 'Status']
        
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 7, header, 1, 0, 'C', True)
        pdf.ln()
        
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(*DEEP_BLUE_RGB)
        
        for item in dossier_data['competitive_context']:
            pdf.cell(col_widths[0], 7, item['company'], 1, 0, 'L')
            pdf.cell(col_widths[1], 7, item['drug'], 1, 0, 'L')
            pdf.cell(col_widths[2], 7, item['phase'], 1, 0, 'C')
            pdf.cell(col_widths[3], 7, item['status'], 1, 0, 'L')
            pdf.ln()
    
    # Key Biomarkers
    pdf.ln(8)
    pdf.section_title('Key Biomarkers')
    
    biomarkers = ', '.join(dossier_data['key_biomarkers'])
    pdf.body_text(biomarkers)
    
    # Recommended Actions
    pdf.ln(5)
    pdf.section_title('Recommended Actions')
    
    for i, action in enumerate(dossier_data['recommended_actions'], 1):
        pdf.body_text(f"{i}. {action}")
        pdf.ln(2)
    
    # Call to Action
    pdf.ln(10)
    pdf.set_fill_color(*SOFT_LAVENDER_RGB)
    pdf.rect(10, pdf.get_y(), 190, 25, 'F')
    
    pdf.set_xy(15, pdf.get_y() + 5)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(*DEEP_BLUE_RGB)
    pdf.cell(0, 5, 'Interested in a comprehensive analysis?', 0, 1, 'L')
    
    pdf.set_x(15)
    pdf.set_font('Helvetica', '', 9)
    pdf.multi_cell(180, 5, 'Contact Excelra to commission a full indication dossier with primary literature review, KOL insights, and detailed competitive intelligence.')
    
    return pdf.output()
