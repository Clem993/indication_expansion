"""
Phase 2 Components: Deep-Dive Analysis & Hypothesis Building
Includes detailed indication dossiers, evidence maps, and mechanistic summaries
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from pathlib import Path
import sys

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from utils.export import generate_deep_dive_pdf
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

# =============================================================================
# TOP 5 INDICATION DOSSIERS (Synthetic Data)
# =============================================================================

INDICATION_DOSSIERS = {
    "Amyotrophic Lateral Sclerosis": {
        "therapeutic_area": "Neurology",
        "frequency_score": 8,
        "validation_status": "Validated",
        "unmet_need": "High",
        "market_size": "$2.1B by 2028",
        "biological_rationale": """
RIPK1-mediated necroptosis has been strongly implicated in motor neuron death in ALS. 
Key evidence includes:

• **RIPK1 activation** observed in post-mortem spinal cord tissue from ALS patients
• **Necroptosis markers** (pMLKL, pRIPK3) elevated in both sporadic and familial ALS
• **Optineurin mutations** (linked to familial ALS) lead to RIPK1-dependent cell death
• **TBK1 loss-of-function** mutations in ALS patients result in enhanced RIPK1 activity

Preclinical studies in SOD1-G93A mice demonstrate that RIPK1 inhibition:
- Delays disease onset by 2-3 weeks
- Extends survival by approximately 15%
- Reduces motor neuron loss and neuroinflammation
        """,
        "key_evidence": [
            {"source": "Literature Mining", "finding": "127 publications linking RIPK1/necroptosis to ALS pathology (2018-2024)", "confidence": "High"},
            {"source": "Gene Expression", "finding": "RIPK1 upregulated 2.3-fold in ALS patient motor cortex (GSE124439)", "confidence": "High"},
            {"source": "Clinical Trials", "finding": "DNL747 (Denali) completed Phase 1b in ALS patients", "confidence": "High"},
            {"source": "GWAS", "finding": "RIPK1 pathway genes enriched in ALS risk loci (p<0.001)", "confidence": "Medium"},
            {"source": "Interactome", "finding": "RIPK1 interacts with TDP-43 and FUS aggregation pathways", "confidence": "Medium"},
        ],
        "competitive_context": [
            {"company": "Denali/Sanofi", "drug": "DNL788 (SAR443820)", "phase": "Phase 2", "status": "Active"},
            {"company": "GSK", "drug": "GSK2982772", "phase": "Phase 1", "status": "Completed"},
        ],
        "recommended_actions": [
            "Commission literature review on RIPK1-TDP43 interaction mechanisms",
            "Analyse existing ALS patient biomarker datasets for necroptosis signatures",
            "Evaluate competitive differentiation strategy vs. DNL788",
            "Explore combination potential with anti-SOD1 therapies",
        ],
        "key_biomarkers": ["pRIPK1", "pMLKL", "Neurofilament Light (NfL)", "Chitinase-3-like protein 1"],
    },
    
    "Multiple Sclerosis": {
        "therapeutic_area": "Neurology",
        "frequency_score": 7,
        "validation_status": "Validated",
        "unmet_need": "Medium-High",
        "market_size": "$28.5B by 2028",
        "biological_rationale": """
RIPK1 plays a dual role in MS pathology through both neuroinflammation and oligodendrocyte death:

• **Oligodendrocyte necroptosis** contributes to demyelination independent of T-cell infiltration
• **TNF-induced RIPK1 activation** in oligodendrocytes drives progressive MS pathology
• **Microglial RIPK1** promotes inflammatory cytokine release and disease progression

Preclinical evidence in EAE (experimental autoimmune encephalomyelitis) models shows:
- RIPK1 kinase-dead mice show 60% reduction in disease severity
- RIPK1 inhibitors reduce demyelination and axonal damage
- Combination with anti-CD20 shows synergistic efficacy
        """,
        "key_evidence": [
            {"source": "Literature Mining", "finding": "89 publications on RIPK1/necroptosis in MS (2019-2024)", "confidence": "High"},
            {"source": "Gene Expression", "finding": "MLKL elevated in active MS lesions vs. NAWM", "confidence": "High"},
            {"source": "Disease-Gene Signature", "finding": "Necroptosis pathway enriched in progressive MS transcriptomes", "confidence": "High"},
            {"source": "Clinical Trials", "finding": "GSK2982772 Phase 2a in MS planned (ClinicalTrials.gov)", "confidence": "Medium"},
            {"source": "Adverse Events", "finding": "TNF inhibitors worsen MS; RIPK1 inhibition may provide alternative", "confidence": "Medium"},
        ],
        "competitive_context": [
            {"company": "GSK", "drug": "GSK2982772", "phase": "Phase 2a", "status": "Planned"},
            {"company": "Denali/Sanofi", "drug": "DNL788", "phase": "Phase 1", "status": "Active"},
        ],
        "recommended_actions": [
            "Focus on progressive MS as differentiated indication (high unmet need)",
            "Evaluate oligodendrocyte-specific biomarkers for patient selection",
            "Assess combination strategy with B-cell depleting therapies",
            "Commission analysis of failed TNF inhibitor trials in MS",
        ],
        "key_biomarkers": ["pMLKL in CSF", "MBP (Myelin Basic Protein)", "GFAP", "Oligodendrocyte-derived exosomes"],
    },
    
    "Alzheimer's Disease": {
        "therapeutic_area": "Neurology",
        "frequency_score": 7,
        "validation_status": "Validated",
        "unmet_need": "Very High",
        "market_size": "$13.7B by 2028",
        "biological_rationale": """
RIPK1 activation is emerging as a key driver of neuroinflammation and neuronal loss in AD:

• **Microglial RIPK1** is activated in AD brains, particularly around amyloid plaques
• **MEG3 lncRNA** (elevated in AD) activates RIPK1-dependent necroptosis in neurons
• **RIPK1 inhibition** reduces neuroinflammation and improves cognition in AD mouse models

Key mechanistic insights:
- RIPK1 mediates Aβ-induced microglial activation and cytokine release
- Tau pathology associated with increased necroptotic markers
- RIPK1 inhibition reduces both amyloid and tau burden in preclinical models
        """,
        "key_evidence": [
            {"source": "Literature Mining", "finding": "156 publications linking RIPK1 to AD pathology (2017-2024)", "confidence": "High"},
            {"source": "Gene Expression", "finding": "RIPK1 elevated 1.8-fold in AD hippocampus (Mayo RNA-seq)", "confidence": "High"},
            {"source": "Disease-Gene Signature", "finding": "Necroptosis genes correlate with Braak staging (r=0.67)", "confidence": "High"},
            {"source": "Interactome", "finding": "RIPK1 pathway intersects with TREM2 microglial activation", "confidence": "Medium"},
            {"source": "GWAS", "finding": "No direct GWAS hits, but pathway enrichment observed", "confidence": "Low"},
        ],
        "competitive_context": [
            {"company": "Denali/Sanofi", "drug": "DNL788", "phase": "Preclinical", "status": "AD indication in planning"},
            {"company": "Multiple", "drug": "Various", "phase": "N/A", "status": "No dedicated AD programmes announced"},
        ],
        "recommended_actions": [
            "Evaluate as add-on to anti-amyloid therapies (lecanemab, donanemab)",
            "Design biomarker strategy around neuroinflammation (sTREM2, YKL-40)",
            "Consider early AD / MCI population for clinical differentiation",
            "Assess blood-brain barrier penetration requirements",
        ],
        "key_biomarkers": ["sTREM2", "YKL-40", "GFAP", "pTau-217", "NfL"],
    },
    
    "Ulcerative Colitis": {
        "therapeutic_area": "Gastroenterology",
        "frequency_score": 7,
        "validation_status": "Validated",
        "unmet_need": "Medium",
        "market_size": "$8.9B by 2028",
        "biological_rationale": """
RIPK1-mediated intestinal epithelial cell death is central to UC pathology:

• **IEC necroptosis** drives barrier dysfunction and bacterial translocation
• **RIPK1 activation** in colonocytes correlates with disease activity
• **A20/TNFAIP3 mutations** (UC risk gene) lead to enhanced RIPK1 activity

Clinical evidence:
- GSK2982772 showed significant reduction in UC symptoms in Phase 2a
- Histological improvement observed in endoscopic biopsies
- Effect maintained over 12-week treatment period
        """,
        "key_evidence": [
            {"source": "Clinical Trials", "finding": "GSK2982772 Phase 2a positive results in UC (NCT02903966)", "confidence": "High"},
            {"source": "Literature Mining", "finding": "72 publications on RIPK1 in IBD (2018-2024)", "confidence": "High"},
            {"source": "Gene Expression", "finding": "RIPK3/MLKL elevated in active UC mucosa", "confidence": "High"},
            {"source": "Disease-Gene Signature", "finding": "Necroptosis signature correlates with Mayo score", "confidence": "High"},
            {"source": "GWAS", "finding": "A20/TNFAIP3 IBD risk locus regulates RIPK1", "confidence": "High"},
        ],
        "competitive_context": [
            {"company": "GSK", "drug": "GSK2982772", "phase": "Phase 2b", "status": "Active"},
            {"company": "Denali/Sanofi", "drug": "DNL788", "phase": "Not pursued", "status": "Focused on CNS"},
        ],
        "recommended_actions": [
            "Analyse GSK2982772 Phase 2a data for differentiation opportunities",
            "Evaluate positioning vs. JAK inhibitors and S1P modulators",
            "Consider biologic-refractory population as target indication",
            "Assess combination potential with anti-TNF or anti-IL-23",
        ],
        "key_biomarkers": ["Faecal calprotectin", "CRP", "Mucosal pMLKL", "Intestinal permeability markers"],
    },
    
    "Rheumatoid Arthritis": {
        "therapeutic_area": "Immunology",
        "frequency_score": 7,
        "validation_status": "Validated",
        "unmet_need": "Medium",
        "market_size": "$34.2B by 2028",
        "biological_rationale": """
RIPK1 drives synovial inflammation and joint destruction in RA:

• **Synovial fibroblast RIPK1** promotes inflammatory cytokine production
• **Macrophage necroptosis** releases DAMPs that amplify joint inflammation
• **TNF-RIPK1 axis** is central to RA pathology (explains TNF inhibitor efficacy)

RIPK1 inhibition offers potential advantages over TNF inhibitors:
- May address TNF-independent inflammation
- Potential for patients who fail anti-TNF therapy
- May have better safety profile than JAK inhibitors
        """,
        "key_evidence": [
            {"source": "Clinical Trials", "finding": "GSK2982772 Phase 2a in RA completed (NCT02858492)", "confidence": "High"},
            {"source": "Literature Mining", "finding": "94 publications on RIPK1 in RA (2016-2024)", "confidence": "High"},
            {"source": "Gene Expression", "finding": "RIPK1 pathway genes elevated in RA synovium", "confidence": "High"},
            {"source": "Structure Similarity", "finding": "RIPK1 inhibitors distinct from JAK inhibitor scaffold", "confidence": "Medium"},
            {"source": "Adverse Events", "finding": "JAK inhibitors carry CV/VTE warnings; RIPK1 may be safer", "confidence": "Medium"},
        ],
        "competitive_context": [
            {"company": "GSK", "drug": "GSK2982772", "phase": "Phase 2a", "status": "Completed"},
            {"company": "Multiple", "drug": "Various", "phase": "Preclinical", "status": "Several programmes"},
        ],
        "recommended_actions": [
            "Position for anti-TNF refractory patients",
            "Conduct head-to-head biomarker analysis vs. JAK inhibitors",
            "Evaluate safety differentiation vs. tofacitinib/upadacitinib",
            "Consider combination with methotrexate as registration strategy",
        ],
        "key_biomarkers": ["CRP", "ESR", "RF", "Anti-CCP", "Synovial pRIPK1"],
    },
}

# Order for display
TOP_5_INDICATIONS = [
    "Amyotrophic Lateral Sclerosis",
    "Multiple Sclerosis", 
    "Alzheimer's Disease",
    "Ulcerative Colitis",
    "Rheumatoid Arthritis",
]


def render_indication_selector():
    """Render the indication selector for deep-dive analysis."""
    
    st.markdown("### Select Indication for Deep-Dive")
    
    selected = st.selectbox(
        "Choose from the top 5 validated indications:",
        options=TOP_5_INDICATIONS,
        index=0,
        key="phase2_indication_selector",
        help="Select an indication to view detailed analysis"
    )
    
    return selected


def render_dossier_header(indication: str, data: dict):
    """Render the dossier header with key metrics."""
    
    # Determine colours based on validation
    if data["validation_status"] == "Validated":
        status_color = VIOLET
    else:
        status_color = MAGENTA_PINK
    
    if data["unmet_need"] == "Very High":
        need_color = VIOLET
    elif data["unmet_need"] == "High":
        need_color = MAGENTA_PINK
    else:
        need_color = DEEP_BLUE
    
    st.markdown(f"""
<div style="background: linear-gradient(135deg, {DEEP_BLUE} 0%, {VIOLET} 100%); 
            border-radius: 16px; padding: 2rem; margin: 1.5rem 0; color: white; font-family: 'Poppins', sans-serif;">
<h2 style="margin: 0 0 0.5rem 0; font-size: 1.6rem; font-weight: 600;">{indication}</h2>
<p style="margin: 0; opacity: 0.9; font-size: 1rem;">{data["therapeutic_area"]} | RIPK1 Inhibitor Indication Dossier</p>
</div>
""", unsafe_allow_html=True)
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
<div style="background: {WHITE}; border: 1px solid {LIGHT_BLUE}; border-radius: 12px; padding: 1.25rem; 
            text-align: center; font-family: 'Poppins', sans-serif; height: 120px; display: flex; 
            flex-direction: column; justify-content: center;">
<div style="font-size: 2rem; font-weight: 700; color: {VIOLET};">{data["frequency_score"]}/9</div>
<div style="font-size: 0.85rem; color: {DEEP_BLUE}; margin-top: 0.25rem;">Evidence Score</div>
</div>
""", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
<div style="background: {WHITE}; border: 1px solid {LIGHT_BLUE}; border-radius: 12px; padding: 1.25rem; 
            text-align: center; font-family: 'Poppins', sans-serif; height: 120px; display: flex; 
            flex-direction: column; justify-content: center;">
<div style="font-size: 1.1rem; font-weight: 700; color: {status_color};">{data["validation_status"]}</div>
<div style="font-size: 0.85rem; color: {DEEP_BLUE}; margin-top: 0.25rem;">Validation Status</div>
</div>
""", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
<div style="background: {WHITE}; border: 1px solid {LIGHT_BLUE}; border-radius: 12px; padding: 1.25rem; 
            text-align: center; font-family: 'Poppins', sans-serif; height: 120px; display: flex; 
            flex-direction: column; justify-content: center;">
<div style="font-size: 1.1rem; font-weight: 700; color: {need_color};">{data["unmet_need"]}</div>
<div style="font-size: 0.85rem; color: {DEEP_BLUE}; margin-top: 0.25rem;">Unmet Need</div>
</div>
""", unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
<div style="background: {WHITE}; border: 1px solid {LIGHT_BLUE}; border-radius: 12px; padding: 1.25rem; 
            text-align: center; font-family: 'Poppins', sans-serif; height: 120px; display: flex; 
            flex-direction: column; justify-content: center;">
<div style="font-size: 1.1rem; font-weight: 700; color: {DEEP_BLUE};">{data["market_size"]}</div>
<div style="font-size: 0.85rem; color: {DEEP_BLUE}; margin-top: 0.25rem;">Market Size</div>
</div>
""", unsafe_allow_html=True)


def render_biological_rationale(data: dict):
    """Render the biological rationale section."""
    
    st.markdown("### Biological Rationale")
    
    st.markdown(f"""
<div style="background: linear-gradient(135deg, {LIGHT_BLUE}20 0%, {SOFT_LAVENDER}20 100%); 
            border-left: 4px solid {VIOLET}; border-radius: 0 12px 12px 0; padding: 1.5rem; 
            font-family: 'Poppins', sans-serif; line-height: 1.7;">
{data["biological_rationale"]}
</div>
""", unsafe_allow_html=True)


def render_evidence_summary(data: dict):
    """Render the evidence summary with confidence indicators."""
    
    st.markdown("### Evidence Summary")
    
    for item in data["key_evidence"]:
        # Confidence colour
        if item["confidence"] == "High":
            conf_color = VIOLET
            conf_bg = f"{VIOLET}22"
        elif item["confidence"] == "Medium":
            conf_color = MAGENTA_PINK
            conf_bg = f"{MAGENTA_PINK}22"
        else:
            conf_color = DEEP_BLUE
            conf_bg = f"{LIGHT_BLUE}"
        
        st.markdown(f"""
<div style="background: {WHITE}; border: 1px solid {LIGHT_BLUE}; border-radius: 10px; 
            padding: 1rem 1.25rem; margin-bottom: 0.75rem; font-family: 'Poppins', sans-serif;">
<div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem;">
<div style="flex: 1;">
<div style="font-weight: 600; color: {VIOLET}; font-size: 0.85rem; margin-bottom: 0.25rem;">
{item["source"]}
</div>
<div style="color: {DEEP_BLUE}; font-size: 0.95rem;">
{item["finding"]}
</div>
</div>
<div style="background: {conf_bg}; color: {conf_color}; padding: 0.25rem 0.75rem; 
            border-radius: 15px; font-size: 0.75rem; font-weight: 600; white-space: nowrap;">
{item["confidence"]} Confidence
</div>
</div>
</div>
""", unsafe_allow_html=True)


def render_competitive_landscape(data: dict, indication: str):
    """Render the competitive landscape for this indication."""
    
    st.markdown("### Competitive Landscape")
    
    if not data["competitive_context"]:
        st.info("No direct competitors identified for this indication.")
        return
    
    for item in data["competitive_context"]:
        # Phase colour
        if "Phase 2" in item["phase"]:
            phase_color = VIOLET
        elif "Phase 1" in item["phase"]:
            phase_color = MAGENTA_PINK
        else:
            phase_color = LIGHT_BLUE
        
        st.markdown(f"""
<div style="background: {WHITE}; border: 1px solid {LIGHT_BLUE}; border-left: 4px solid {phase_color}; 
            border-radius: 8px; padding: 1rem 1.25rem; margin-bottom: 0.75rem; font-family: 'Poppins', sans-serif;">
<div style="display: flex; justify-content: space-between; align-items: center;">
<div>
<div style="font-weight: 600; color: {DEEP_BLUE}; font-size: 1rem;">{item["company"]}</div>
<div style="color: #666; font-size: 0.9rem;">{item["drug"]}</div>
</div>
<div style="display: flex; align-items: center; gap: 0.75rem;">
<div style="background: {phase_color}; color: white; padding: 0.25rem 0.75rem; 
            border-radius: 15px; font-size: 0.8rem; font-weight: 600;">
{item["phase"]}
</div>
<div style="color: #888; font-size: 0.85rem;">{item["status"]}</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)


def render_biomarkers(data: dict):
    """Render key biomarkers for patient selection."""
    
    st.markdown("### Key Biomarkers")
    
    biomarker_html = ""
    for biomarker in data["key_biomarkers"]:
        biomarker_html += f"""
<span style="display: inline-block; background: {SOFT_LAVENDER}; color: {DEEP_BLUE}; 
             padding: 0.4rem 0.9rem; border-radius: 20px; font-size: 0.85rem; font-weight: 500;
             margin: 0.25rem 0.25rem 0.25rem 0; font-family: 'Poppins', sans-serif;">
{biomarker}
</span>
"""
    
    st.markdown(f"""
<div style="padding: 0.5rem 0;">
{biomarker_html}
</div>
""", unsafe_allow_html=True)


def render_recommended_actions(data: dict):
    """Render recommended next steps."""
    
    st.markdown("### Recommended Actions")
    
    for i, action in enumerate(data["recommended_actions"], 1):
        st.markdown(f"""
<div style="display: flex; align-items: flex-start; gap: 0.75rem; margin-bottom: 0.75rem; font-family: 'Poppins', sans-serif;">
<div style="background: linear-gradient(135deg, {VIOLET}, {MAGENTA_PINK}); color: white; 
            width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; 
            justify-content: center; font-weight: 600; font-size: 0.85rem; flex-shrink: 0;">
{i}
</div>
<div style="color: {DEEP_BLUE}; font-size: 0.95rem; padding-top: 0.2rem;">
{action}
</div>
</div>
""", unsafe_allow_html=True)


def render_evidence_radar(data: dict, indication: str):
    """Render a radar chart showing evidence across approaches."""
    
    # Evidence sources and scores (derived from key_evidence)
    sources = ["Literature", "Clinical", "Gene Expr.", "Disease Sig.", "GWAS", "Interactome"]
    
    # Map confidence to scores
    confidence_map = {"High": 3, "Medium": 2, "Low": 1}
    
    # Build scores from evidence
    scores = []
    evidence_dict = {e["source"]: e["confidence"] for e in data["key_evidence"]}
    
    source_mapping = {
        "Literature": "Literature Mining",
        "Clinical": "Clinical Trials", 
        "Gene Expr.": "Gene Expression",
        "Disease Sig.": "Disease-Gene Signature",
        "GWAS": "GWAS",
        "Interactome": "Interactome"
    }
    
    for source in sources:
        full_source = source_mapping.get(source, source)
        if full_source in evidence_dict:
            scores.append(confidence_map.get(evidence_dict[full_source], 1))
        else:
            scores.append(1)
    
    # Close the radar
    scores_closed = scores + [scores[0]]
    sources_closed = sources + [sources[0]]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores_closed,
        theta=sources_closed,
        fill='toself',
        fillcolor=f'rgba(162, 77, 190, 0.3)',
        line=dict(color=VIOLET, width=2),
        name=indication
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 3],
                tickvals=[1, 2, 3],
                ticktext=["Low", "Med", "High"],
                tickfont=dict(family='Poppins', size=10)
            ),
            angularaxis=dict(
                tickfont=dict(family='Poppins', size=11)
            )
        ),
        showlegend=False,
        margin=dict(l=60, r=60, t=40, b=40),
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins')
    )
    
    return fig


def render_network_visualization(indication: str, dossier_data: dict):
    """Render an interactive network visualization showing target-pathway-indication relationships."""
    
    st.markdown("### Biological Network")
    st.markdown(f"""
<p style="color: #666; font-size: 0.9rem; font-family: 'Poppins', sans-serif;">
Interactive network showing the relationship between RIPK1, key pathways, and {indication}.
</p>
""", unsafe_allow_html=True)
    
    # Define network nodes based on indication
    # Central node: RIPK1
    # Pathway nodes: Relevant biological pathways
    # Indication node: The target indication
    # Evidence nodes: Key evidence types
    
    pathway_data = {
        "Amyotrophic Lateral Sclerosis": {
            "pathways": ["Necroptosis", "Neuroinflammation", "TNF Signalling", "TDP-43 Aggregation"],
            "mechanisms": ["Motor Neuron Death", "Microglial Activation", "Astrogliosis"],
        },
        "Multiple Sclerosis": {
            "pathways": ["Necroptosis", "Neuroinflammation", "TNF Signalling", "Demyelination"],
            "mechanisms": ["Oligodendrocyte Death", "T-cell Infiltration", "BBB Disruption"],
        },
        "Alzheimer's Disease": {
            "pathways": ["Necroptosis", "Neuroinflammation", "Amyloid Cascade", "Tau Pathology"],
            "mechanisms": ["Microglial Activation", "Synaptic Loss", "Neuronal Death"],
        },
        "Ulcerative Colitis": {
            "pathways": ["Necroptosis", "Intestinal Inflammation", "TNF Signalling", "Barrier Dysfunction"],
            "mechanisms": ["Epithelial Cell Death", "Immune Infiltration", "Mucosal Damage"],
        },
        "Rheumatoid Arthritis": {
            "pathways": ["Necroptosis", "Synovial Inflammation", "TNF Signalling", "Joint Destruction"],
            "mechanisms": ["Synoviocyte Activation", "Pannus Formation", "Bone Erosion"],
        },
    }
    
    data = pathway_data.get(indication, {
        "pathways": ["Necroptosis", "Inflammation", "Cell Death"],
        "mechanisms": ["Target Mechanism 1", "Target Mechanism 2"],
    })
    
    # Create node positions
    nodes = []
    edges = []
    
    # Central node - RIPK1
    nodes.append({"id": "RIPK1", "x": 0, "y": 0, "size": 40, "color": VIOLET, "type": "target"})
    
    # Pathway nodes - arranged in a circle around RIPK1
    n_pathways = len(data["pathways"])
    for i, pathway in enumerate(data["pathways"]):
        angle = (2 * np.pi * i / n_pathways) - np.pi/2
        x = 2 * np.cos(angle)
        y = 2 * np.sin(angle)
        nodes.append({"id": pathway, "x": x, "y": y, "size": 25, "color": MAGENTA_PINK, "type": "pathway"})
        edges.append({"from": "RIPK1", "to": pathway})
    
    # Mechanism nodes - outer ring
    n_mechanisms = len(data["mechanisms"])
    for i, mechanism in enumerate(data["mechanisms"]):
        angle = (2 * np.pi * i / n_mechanisms) - np.pi/4
        x = 3.5 * np.cos(angle)
        y = 3.5 * np.sin(angle)
        nodes.append({"id": mechanism, "x": x, "y": y, "size": 20, "color": LIGHT_BLUE, "type": "mechanism"})
        # Connect to nearest pathway
        pathway_idx = i % n_pathways
        edges.append({"from": data["pathways"][pathway_idx], "to": mechanism})
    
    # Indication node - at the bottom
    nodes.append({"id": indication, "x": 0, "y": 4.5, "size": 35, "color": DEEP_BLUE, "type": "indication"})
    
    # Connect mechanisms to indication
    for mechanism in data["mechanisms"]:
        edges.append({"from": mechanism, "to": indication})
    
    # Create Plotly figure
    fig = go.Figure()
    
    # Add edges
    for edge in edges:
        from_node = next(n for n in nodes if n["id"] == edge["from"])
        to_node = next(n for n in nodes if n["id"] == edge["to"])
        
        fig.add_trace(go.Scatter(
            x=[from_node["x"], to_node["x"]],
            y=[from_node["y"], to_node["y"]],
            mode='lines',
            line=dict(color='#E3D9F2', width=2),
            hoverinfo='none',
            showlegend=False
        ))
    
    # Add nodes
    for node_type, color, name in [
        ("target", VIOLET, "Target"),
        ("pathway", MAGENTA_PINK, "Pathways"),
        ("mechanism", LIGHT_BLUE, "Mechanisms"),
        ("indication", DEEP_BLUE, "Indication")
    ]:
        type_nodes = [n for n in nodes if n["type"] == node_type]
        if type_nodes:
            fig.add_trace(go.Scatter(
                x=[n["x"] for n in type_nodes],
                y=[n["y"] for n in type_nodes],
                mode='markers+text',
                marker=dict(
                    size=[n["size"] for n in type_nodes],
                    color=color,
                    line=dict(color='white', width=2)
                ),
                text=[n["id"] for n in type_nodes],
                textposition="bottom center",
                textfont=dict(size=10, family='Poppins', color=DEEP_BLUE),
                name=name,
                hovertemplate='<b>%{text}</b><extra></extra>'
            ))
    
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(family='Poppins', size=11)
        ),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-5, 5]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.5, 6]),
        height=450,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Poppins')
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_request_analysis_form():
    """Render the request full analysis form."""
    
    st.markdown("### Request Full Analysis")
    
    st.markdown(f"""
<div style="background: {SOFT_LAVENDER}33; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; font-family: 'Poppins', sans-serif;">
<p style="margin: 0 0 1rem 0; color: {DEEP_BLUE}; font-size: 0.95rem;">
Interested in a comprehensive indication dossier? Complete the form below and our team will contact you 
to discuss your specific requirements.
</p>
</div>
""", unsafe_allow_html=True)
    
    with st.form("request_analysis_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name *", placeholder="Your name")
            company = st.text_input("Company *", placeholder="Your organisation")
        
        with col2:
            email = st.text_input("Email *", placeholder="your.email@company.com")
            role = st.selectbox(
                "Role",
                options=["", "VP/Head of Discovery", "Head of BD/Licensing", "CSO/CTO", "Principal Scientist", "Other"],
                key="request_role"
            )
        
        interest = st.multiselect(
            "Areas of Interest",
            options=[
                "Full Indication Dossier",
                "Competitive Intelligence",
                "Biomarker Strategy",
                "Clinical Development Plan",
                "Commercial Assessment",
                "GRIP Platform Demo"
            ],
            key="request_interest"
        )
        
        message = st.text_area(
            "Additional Comments",
            placeholder="Tell us about your specific requirements or questions...",
            height=100
        )
        
        submitted = st.form_submit_button("Submit Request", use_container_width=True)
        
        if submitted:
            if name and email and company:
                st.success("Thank you for your interest! Our team will contact you within 2 business days.")
                # In production, this would send to a CRM or email system
            else:
                st.warning("Please complete all required fields (Name, Email, Company).")


def render_export_section_phase2(indication: str, dossier_data: dict, target: str):
    """Render the export/download section for Phase 2."""
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
<div style="text-align: center; padding: 1rem 0;">
<p style="font-family: 'Poppins', sans-serif; color: {DEEP_BLUE}; margin-bottom: 0.5rem;">
Download a PDF dossier for this indication
</p>
</div>
""", unsafe_allow_html=True)
        
        if EXPORT_AVAILABLE:
            try:
                # Get logo path
                assets_path = Path(__file__).parent.parent / "assets"
                logo_path = str(assets_path / "logo.png") if (assets_path / "logo.png").exists() else None
                
                # Generate PDF
                pdf_bytes = generate_deep_dive_pdf(target, indication, dossier_data, logo_path)
                
                # Download button
                st.download_button(
                    label=f"Download {indication} Dossier (PDF)",
                    data=pdf_bytes,
                    file_name=f"{target}_{indication.replace(' ', '_')}_dossier_{pd.Timestamp.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    key="download_dossier_pdf"
                )
            except Exception as e:
                st.warning(f"PDF export unavailable: Install fpdf2 to enable downloads.")
        else:
            st.info("PDF export available with fpdf2 library. Run: pip install fpdf2")


def render_phase_2(target: str):
    """Main render function for Phase 2."""
    
    # Stage indicator
    st.markdown("""
<div style="display: inline-block;" class="stage-indicator stage-deepdive">
Deep-Dive Analysis
</div>
""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Intro text
    st.markdown(f"""
<div style="background: linear-gradient(135deg, {VIOLET}15 0%, {MAGENTA_PINK}15 100%); 
            padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid {VIOLET}; 
            font-family: 'Poppins', sans-serif;">
<p style="margin: 0; color: {DEEP_BLUE}; font-size: 0.95rem;">
<strong>Target:</strong> RIPK1 (Receptor-Interacting Serine/Threonine-Protein Kinase 1)<br><br>
Based on our indication discovery analysis, we have identified <strong>5 high-priority indications</strong> for detailed evaluation. 
Each indication dossier includes biological rationale, evidence summary, competitive landscape, and recommended next steps.
</p>
</div>
""", unsafe_allow_html=True)
    
    # Indication selector
    selected_indication = render_indication_selector()
    
    st.markdown("---")
    
    # Get dossier data
    dossier_data = INDICATION_DOSSIERS.get(selected_indication)
    
    if not dossier_data:
        st.error("Dossier data not found for this indication.")
        return
    
    # Render dossier header
    render_dossier_header(selected_indication, dossier_data)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Two column layout for main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_biological_rationale(dossier_data)
        st.markdown("<br>", unsafe_allow_html=True)
        render_evidence_summary(dossier_data)
    
    with col2:
        st.markdown("### Evidence Profile")
        fig = render_evidence_radar(dossier_data, selected_indication)
        st.plotly_chart(fig, use_container_width=True)
        
        render_biomarkers(dossier_data)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Full width sections
    col1, col2 = st.columns(2)
    
    with col1:
        render_competitive_landscape(dossier_data, selected_indication)
    
    with col2:
        render_recommended_actions(dossier_data)
    
    # Network visualization
    st.markdown("<br>", unsafe_allow_html=True)
    render_network_visualization(selected_indication, dossier_data)
    
    # Export section
    render_export_section_phase2(selected_indication, dossier_data, target)
    
    # Request Analysis Form
    st.markdown("<br>", unsafe_allow_html=True)
    render_request_analysis_form()
    
    # Final call to action
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
<div style="background: linear-gradient(135deg, {DEEP_BLUE} 0%, {VIOLET} 100%); 
            padding: 1.5rem 2rem; border-radius: 12px; text-align: center; font-family: 'Poppins', sans-serif;">
<p style="margin: 0; color: white; font-size: 1rem;">
<strong>Excelra — Where Data Means More</strong><br>
<span style="opacity: 0.9;">Accelerating drug discovery with integrated data, analytics, and scientific expertise.</span>
</p>
</div>
""", unsafe_allow_html=True)
