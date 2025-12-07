"""
Phase 1 Components: Data-Driven Indication Discovery
Includes frequency table, heatmap, and filtering capabilities
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from utils.export import generate_indication_discovery_pdf
    EXPORT_AVAILABLE = True
except ImportError:
    EXPORT_AVAILABLE = False

# =============================================================================
# BRAND COLOURS
# =============================================================================
DEEP_BLUE = "#0A1E4A"
VIOLET = "#A24DBE"
MAGENTA_PINK = "#E04F8A"
LIGHT_BLUE = "#B3E0F2"
SOFT_LAVENDER = "#E3D9F2"
WHITE = "#FFFFFF"

# Scientific approach display names
APPROACH_LABELS = {
    'literature_mining': 'Literature Mining',
    'clinical_trials': 'Clinical Trials',
    'structure_similarity': 'Structure Similarity',
    'adverse_events': 'Adverse Events',
    'gene_expression': 'Gene Expression',
    'disease_gene_signature': 'Disease-Gene Signature',
    'drug_disease_signature': 'Drug-Disease Signature',
    'interactome': 'Interactome',
    'gwas': 'GWAS'
}

APPROACH_COLUMNS = list(APPROACH_LABELS.keys())


def load_frequency_data() -> pd.DataFrame:
    """Load the frequency table data."""
    data_path = Path(__file__).parent.parent / "data" / "ripk1_frequency_table.csv"
    return pd.read_csv(data_path)


def load_evidence_data() -> pd.DataFrame:
    """Load the evidence details data."""
    data_path = Path(__file__).parent.parent / "data" / "ripk1_evidence_details.csv"
    return pd.read_csv(data_path)


def load_competitive_data() -> pd.DataFrame:
    """Load the competitive landscape data."""
    data_path = Path(__file__).parent.parent / "data" / "ripk1_competitive_landscape.csv"
    return pd.read_csv(data_path)


def render_summary_metrics(df: pd.DataFrame):
    """Render the summary metric cards."""
    
    total_indications = len(df)
    validated_count = len(df[df['relevancy'] == 'Yes'])
    partial_count = len(df[df['relevancy'] == 'Partial'])
    max_score = df['frequency_score'].max()
    avg_score = df['frequency_score'].mean()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
<div class="metric-card">
<h3>Indications Identified</h3>
<div class="value">{total_indications}</div>
</div>
""", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
<div class="metric-card">
<h3>Validated (High Confidence)</h3>
<div class="value" style="color: {VIOLET};">{validated_count}</div>
</div>
""", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
<div class="metric-card">
<h3>Partial Evidence</h3>
<div class="value" style="color: {MAGENTA_PINK};">{partial_count}</div>
</div>
""", unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
<div class="metric-card">
<h3>Top Score</h3>
<div class="value">{max_score}/9</div>
</div>
""", unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
<div class="metric-card">
<h3>Average Score</h3>
<div class="value">{avg_score:.1f}/9</div>
</div>
""", unsafe_allow_html=True)


def render_filters(df: pd.DataFrame, key_prefix: str = "default") -> pd.DataFrame:
    """Render filters and return filtered dataframe.
    
    Args:
        df: The dataframe to filter
        key_prefix: Unique prefix for widget keys to avoid duplicate element errors
    """
    
    st.markdown("### Filter & Sort")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        therapeutic_areas = ['All'] + sorted(df['therapeutic_area'].unique().tolist())
        selected_ta = st.selectbox(
            "Therapeutic Area", 
            therapeutic_areas,
            key=f"{key_prefix}_therapeutic_area"
        )
    
    with col2:
        relevancy_options = ['All', 'Yes', 'Partial', 'No']
        selected_relevancy = st.selectbox(
            "Relevancy", 
            relevancy_options,
            key=f"{key_prefix}_relevancy"
        )
    
    with col3:
        min_score = st.slider(
            "Minimum Score", 
            0, 9, 0,
            key=f"{key_prefix}_min_score"
        )
    
    with col4:
        sort_options = ['Frequency Score (High to Low)', 'Frequency Score (Low to High)', 
                       'Indication Name (A-Z)', 'Therapeutic Area']
        sort_by = st.selectbox(
            "Sort By", 
            sort_options,
            key=f"{key_prefix}_sort_by"
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_ta != 'All':
        filtered_df = filtered_df[filtered_df['therapeutic_area'] == selected_ta]
    
    if selected_relevancy != 'All':
        filtered_df = filtered_df[filtered_df['relevancy'] == selected_relevancy]
    
    filtered_df = filtered_df[filtered_df['frequency_score'] >= min_score]
    
    # Apply sorting
    if sort_by == 'Frequency Score (High to Low)':
        filtered_df = filtered_df.sort_values('frequency_score', ascending=False)
    elif sort_by == 'Frequency Score (Low to High)':
        filtered_df = filtered_df.sort_values('frequency_score', ascending=True)
    elif sort_by == 'Indication Name (A-Z)':
        filtered_df = filtered_df.sort_values('indication_name')
    elif sort_by == 'Therapeutic Area':
        filtered_df = filtered_df.sort_values(['therapeutic_area', 'frequency_score'], ascending=[True, False])
    
    return filtered_df


def render_frequency_heatmap(df: pd.DataFrame):
    """Render the frequency table as an interactive heatmap."""
    
    st.markdown("### Frequency Table Heatmap")
    st.markdown("""
<p style="color: #666; font-size: 0.9rem; font-family: 'Poppins', sans-serif;">
Each cell indicates whether the indication was identified through that scientific approach (1) or not (0).
Darker colours indicate evidence present. Click on an indication to view details.
</p>
""", unsafe_allow_html=True)
    
    # Prepare data for heatmap
    heatmap_df = df[['indication_name'] + APPROACH_COLUMNS].copy()
    heatmap_df = heatmap_df.set_index('indication_name')
    
    # Rename columns for display
    heatmap_df.columns = [APPROACH_LABELS[col] for col in heatmap_df.columns]
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_df.values,
        x=heatmap_df.columns,
        y=heatmap_df.index,
        colorscale=[
            [0, SOFT_LAVENDER],
            [0.5, LIGHT_BLUE],
            [1, VIOLET]
        ],
        showscale=False,
        hovertemplate='<b>%{y}</b><br>%{x}: %{z}<extra></extra>'
    ))
    
    # Add score annotations
    scores = df.set_index('indication_name')['frequency_score']
    
    fig.update_layout(
        height=max(400, len(df) * 35),
        margin=dict(l=200, r=100, t=50, b=100),
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=11, family='Poppins'),
            side='bottom'
        ),
        yaxis=dict(
            tickfont=dict(size=11, family='Poppins'),
            autorange='reversed'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins')
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_ranked_list(df: pd.DataFrame):
    """Render the ranked indication list with expandable details."""
    
    st.markdown("### Ranked Indications")
    
    # Reset index to ensure clean iteration
    df_display = df.reset_index(drop=True)
    
    for idx in range(len(df_display)):
        row = df_display.iloc[idx]
        score = int(row['frequency_score'])
        relevancy = str(row['relevancy'])
        indication_name = str(row['indication_name'])
        therapeutic_area = str(row['therapeutic_area'])
        
        # Relevancy indicator
        if relevancy == 'Yes':
            relevancy_color = VIOLET
            relevancy_text = "Validated"
        elif relevancy == 'Partial':
            relevancy_color = MAGENTA_PINK
            relevancy_text = "Partial"
        else:
            relevancy_color = LIGHT_BLUE
            relevancy_text = "Limited"
        
        # Create expander with simple label
        label = indication_name + " — Score: " + str(score) + "/9 | " + therapeutic_area
        
        with st.expander(label):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Therapeutic Area:** {therapeutic_area}")
                st.markdown(f"**Frequency Score:** {score}/9")
                st.markdown(f"**Validation Status:** :{relevancy_text}")
            
            with col2:
                # Show which approaches identified this indication
                st.markdown("**Evidence Sources:**")
                approaches_present = []
                for col in APPROACH_COLUMNS:
                    if row[col] == 1:
                        approaches_present.append(APPROACH_LABELS[col])
                
                for approach in approaches_present:
                    st.write(f"• {approach}")


def render_therapeutic_area_breakdown(df: pd.DataFrame):
    """Render therapeutic area breakdown chart."""
    
    st.markdown("### Therapeutic Area Breakdown")
    
    ta_counts = df['therapeutic_area'].value_counts().reset_index()
    ta_counts.columns = ['Therapeutic Area', 'Count']
    
    fig = go.Figure(data=[go.Bar(
        y=ta_counts['Therapeutic Area'],
        x=ta_counts['Count'],
        orientation='h',
        marker_color=VIOLET,
        hovertemplate='%{y}: %{x} indications<extra></extra>'
    )])
    
    fig.update_layout(
        height=300,
        margin=dict(l=150, r=50, t=20, b=50),
        xaxis=dict(title='Number of Indications', tickfont=dict(family='Poppins')),
        yaxis=dict(tickfont=dict(family='Poppins')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins')
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_competitive_landscape(df: pd.DataFrame, freq_df: pd.DataFrame):
    """Render competitive landscape summary."""
    
    st.markdown("### Competitive Landscape")
    st.markdown("""
<p style="color: #666; font-size: 0.9rem; font-family: 'Poppins', sans-serif;">
Overview of RIPK1 inhibitor development programmes across the industry.
</p>
""", unsafe_allow_html=True)
    
    # Group by company and highest phase
    company_summary = df.groupby('company').agg({
        'drug_name': lambda x: ', '.join(x.unique()),
        'highest_phase': 'first',
        'indication': lambda x: ', '.join(x.unique()[:3]) + ('...' if len(x.unique()) > 3 else '')
    }).reset_index()
    
    # Create phase indicator
    phase_order = {'Phase 2': 3, 'Phase 1': 2, 'Preclinical': 1}
    company_summary['phase_rank'] = company_summary['highest_phase'].map(phase_order)
    company_summary = company_summary.sort_values('phase_rank', ascending=False)
    
    for _, row in company_summary.iterrows():
        phase = row['highest_phase']
        if phase == 'Phase 2':
            phase_color = VIOLET
        elif phase == 'Phase 1':
            phase_color = MAGENTA_PINK
        else:
            phase_color = LIGHT_BLUE
        
        st.markdown(f"""
<div style="background: {WHITE}; border: 1px solid {LIGHT_BLUE}; border-left: 4px solid {phase_color}; 
            border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem; font-family: 'Poppins', sans-serif;">
<div style="display: flex; justify-content: space-between; align-items: center;">
<div>
<strong style="color: {DEEP_BLUE}; font-size: 1rem;">{row['company']}</strong>
<p style="margin: 0.25rem 0 0 0; font-size: 0.85rem; color: #666;">{row['drug_name']}</p>
</div>
<div style="background: {phase_color}; color: white; padding: 0.25rem 0.75rem; 
            border-radius: 15px; font-size: 0.8rem; font-weight: 600;">
{phase}
</div>
</div>
<p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; color: #888;">
<em>Indications: {row['indication']}</em>
</p>
</div>
""", unsafe_allow_html=True)


def render_methodology_panel():
    """Render the methodology explanation panel."""
    
    st.markdown("### Methodology")
    
    with st.expander("View Scientific Approach Details"):
        st.markdown(f"""
<div style="font-family: 'Poppins', sans-serif; color: {DEEP_BLUE};">
<p style="margin-bottom: 1rem;">
This analysis integrates evidence from <strong>nine complementary scientific approaches</strong>, 
each contributing to a comprehensive view of indication expansion opportunities:
</p>
</div>
""", unsafe_allow_html=True)
        
        approaches = [
            {
                "name": "Literature Mining",
                "description": "Systematic extraction of target-disease associations from published scientific literature using NLP and machine learning.",
                "data_source": "PubMed, PMC, Patent literature"
            },
            {
                "name": "Clinical Trials",
                "description": "Analysis of clinical trial data for related compounds and mechanisms, including completed, ongoing, and terminated studies.",
                "data_source": "ClinicalTrials.gov, EudraCT, CTOD"
            },
            {
                "name": "Structure Similarity",
                "description": "Identification of potential indications from structurally similar compounds with known therapeutic applications.",
                "data_source": "GOSTAR, ChEMBL"
            },
            {
                "name": "Adverse Events",
                "description": "Mining of adverse event databases for therapeutic signal detection (drug repositioning from side effects).",
                "data_source": "FAERS, VigiBase"
            },
            {
                "name": "Gene Expression",
                "description": "Analysis of disease-specific gene expression signatures to identify conditions where target modulation may be beneficial.",
                "data_source": "GEO, ArrayExpress, TCGA"
            },
            {
                "name": "Disease-Gene Signatures",
                "description": "Matching of target biology to disease molecular profiles using transcriptomic and proteomic data.",
                "data_source": "DisGeNET, OMIM, proprietary datasets"
            },
            {
                "name": "Drug-Disease Signatures",
                "description": "Connectivity mapping between drug perturbation signatures and disease expression profiles.",
                "data_source": "CMap, LINCS L1000"
            },
            {
                "name": "Interactome Analysis",
                "description": "Network-based prediction using protein-protein interactions and pathway proximity to disease genes.",
                "data_source": "STRING, BioGRID, proprietary interactome"
            },
            {
                "name": "GWAS",
                "description": "Genetic association evidence from genome-wide studies linking target or pathway to disease risk.",
                "data_source": "GWAS Catalog, UK Biobank, FinnGen"
            },
        ]
        
        col1, col2 = st.columns(2)
        
        for i, approach in enumerate(approaches):
            with col1 if i % 2 == 0 else col2:
                st.markdown(f"""
<div style="background: {SOFT_LAVENDER}33; border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem; font-family: 'Poppins', sans-serif;">
<div style="font-weight: 600; color: {VIOLET}; font-size: 0.95rem; margin-bottom: 0.25rem;">
{i+1}. {approach["name"]}
</div>
<div style="font-size: 0.85rem; color: {DEEP_BLUE}; margin-bottom: 0.5rem;">
{approach["description"]}
</div>
<div style="font-size: 0.75rem; color: #888;">
<strong>Sources:</strong> {approach["data_source"]}
</div>
</div>
""", unsafe_allow_html=True)
        
        st.markdown(f"""
<div style="background: linear-gradient(135deg, {VIOLET}15 0%, {MAGENTA_PINK}15 100%); 
            border-radius: 8px; padding: 1rem; margin-top: 1rem; font-family: 'Poppins', sans-serif;">
<p style="margin: 0; color: {DEEP_BLUE}; font-size: 0.9rem;">
<strong>Scoring:</strong> Each indication receives a frequency score (1-9) based on the number of approaches 
providing supporting evidence. Higher scores indicate stronger multi-source validation.
</p>
</div>
""", unsafe_allow_html=True)


def render_export_section(freq_df, target: str):
    """Render the export/download section."""
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
<div style="text-align: center; padding: 1rem 0;">
<p style="font-family: 'Poppins', sans-serif; color: {DEEP_BLUE}; margin-bottom: 0.5rem;">
Download a PDF report of this analysis
</p>
</div>
""", unsafe_allow_html=True)
        
        if EXPORT_AVAILABLE:
            try:
                # Get logo path
                assets_path = Path(__file__).parent.parent / "assets"
                logo_path = str(assets_path / "logo.png") if (assets_path / "logo.png").exists() else None
                
                # Generate PDF
                pdf_bytes = generate_indication_discovery_pdf(target, freq_df, logo_path)
                
                # Download button
                st.download_button(
                    label="Download Indication Discovery Report (PDF)",
                    data=pdf_bytes,
                    file_name=f"{target}_indication_discovery_{pd.Timestamp.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    key="download_discovery_pdf"
                )
            except Exception as e:
                st.warning(f"PDF export unavailable: Install fpdf2 to enable downloads.")
        else:
            st.info("PDF export available with fpdf2 library. Run: pip install fpdf2")


def render_phase_1(target: str):
    """Main render function for Phase 1."""
    
    # Load data
    freq_df = load_frequency_data()
    evidence_df = load_evidence_data()
    competitive_df = load_competitive_data()
    
    # Stage indicator
    st.markdown("""
<div style="display: inline-block;" class="stage-indicator stage-discovery">
Indication Discovery
</div>
""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Intro text
    st.markdown(f"""
<div style="background: linear-gradient(135deg, {LIGHT_BLUE}20 0%, {SOFT_LAVENDER}20 100%); 
            padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid {VIOLET}; font-family: 'Poppins', sans-serif;">
<p style="margin: 0; color: {DEEP_BLUE}; font-size: 0.95rem;">
<strong>Target:</strong> RIPK1 (Receptor-Interacting Serine/Threonine-Protein Kinase 1)<br><br>
Using Excelra's multi-source approach, we have systematically identified <strong>{len(freq_df)} potential indications</strong> 
for RIPK1 inhibitor expansion. Each indication has been scored across <strong>9 scientific approaches</strong> 
and validated against published literature.
</p>
</div>
""", unsafe_allow_html=True)
    
    # Summary metrics
    render_summary_metrics(freq_df)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create tabs for different views (no icons)
    tab1, tab2, tab3, tab4 = st.tabs([
        "Frequency Table", 
        "Ranked List", 
        "Analytics",
        "Competitive Landscape"
    ])
    
    with tab1:
        # Filters with unique key prefix
        filtered_df = render_filters(freq_df, key_prefix="freq_table")
        
        st.markdown(f"*Showing {len(filtered_df)} of {len(freq_df)} indications*")
        
        # Heatmap
        if len(filtered_df) > 0:
            render_frequency_heatmap(filtered_df)
        else:
            st.warning("No indications match the current filters.")
    
    with tab2:
        # Filters with different unique key prefix
        filtered_df = render_filters(freq_df, key_prefix="ranked_list")
        
        if len(filtered_df) > 0:
            render_ranked_list(filtered_df)
        else:
            st.warning("No indications match the current filters.")
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            render_therapeutic_area_breakdown(freq_df)
        
        with col2:
            # Score distribution (no icon)
            st.markdown("### Score Distribution")
            
            fig = go.Figure(data=[go.Histogram(
                x=freq_df['frequency_score'],
                nbinsx=9,
                marker_color=VIOLET,
                hovertemplate='Score: %{x}<br>Count: %{y}<extra></extra>'
            )])
            
            fig.update_layout(
                height=300,
                margin=dict(l=50, r=50, t=20, b=50),
                xaxis=dict(title='Frequency Score', tickfont=dict(family='Poppins'), dtick=1),
                yaxis=dict(title='Number of Indications', tickfont=dict(family='Poppins')),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Poppins'),
                bargap=0.1
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Relevancy breakdown (no icon)
        st.markdown("### Validation Status")
        
        relevancy_counts = freq_df['relevancy'].value_counts()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            yes_count = relevancy_counts.get('Yes', 0)
            st.markdown(f"""
<div style="background: linear-gradient(135deg, {VIOLET}, {MAGENTA_PINK}); 
            padding: 1.5rem; border-radius: 12px; text-align: center; color: white; font-family: 'Poppins', sans-serif;">
<div style="font-size: 2.5rem; font-weight: 700;">{yes_count}</div>
<div style="font-size: 0.9rem;">Validated (High Confidence)</div>
<div style="font-size: 0.8rem; opacity: 0.8; margin-top: 0.5rem;">
Strong clinical or preclinical evidence
</div>
</div>
""", unsafe_allow_html=True)
        
        with col2:
            partial_count = relevancy_counts.get('Partial', 0)
            st.markdown(f"""
<div style="background: {LIGHT_BLUE}; 
            padding: 1.5rem; border-radius: 12px; text-align: center; color: {DEEP_BLUE}; font-family: 'Poppins', sans-serif;">
<div style="font-size: 2.5rem; font-weight: 700;">{partial_count}</div>
<div style="font-size: 0.9rem;">Partial Evidence</div>
<div style="font-size: 0.8rem; opacity: 0.7; margin-top: 0.5rem;">
Emerging evidence; requires validation
</div>
</div>
""", unsafe_allow_html=True)
        
        with col3:
            no_count = relevancy_counts.get('No', 0)
            st.markdown(f"""
<div style="background: {SOFT_LAVENDER}; 
            padding: 1.5rem; border-radius: 12px; text-align: center; color: {DEEP_BLUE}; font-family: 'Poppins', sans-serif;">
<div style="font-size: 2.5rem; font-weight: 700;">{no_count}</div>
<div style="font-size: 0.9rem;">Limited Evidence</div>
<div style="font-size: 0.8rem; opacity: 0.7; margin-top: 0.5rem;">
Data-driven signal; not yet validated
</div>
</div>
""", unsafe_allow_html=True)
    
    with tab4:
        render_competitive_landscape(competitive_df, freq_df)
    
    # Methodology panel
    st.markdown("<br>", unsafe_allow_html=True)
    render_methodology_panel()
    
    # Export section
    render_export_section(freq_df, target)
    
    # Call to action
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
<div style="background: linear-gradient(135deg, {VIOLET}15 0%, {MAGENTA_PINK}15 100%); 
            padding: 1.5rem; border-radius: 12px; text-align: center; border: 1px solid {VIOLET}30; font-family: 'Poppins', sans-serif;">
<p style="margin: 0; color: {DEEP_BLUE}; font-size: 1rem;">
<strong>Ready to dive deeper?</strong><br>
Select <strong>Deep-Dive Analysis</strong> from the sidebar to explore detailed 
evidence maps and biological hypotheses for the top 5 validated indications.
</p>
</div>
""", unsafe_allow_html=True)
