"""
Indication Expansion & Prioritisation Dashboard
Excelra - Where data means more
"""

import streamlit as st
from pathlib import Path
import base64
import sys

# Add components to path
sys.path.insert(0, str(Path(__file__).parent))
from components.phase1 import render_phase_1
from components.phase2 import render_phase_2

# =============================================================================
# BRAND COLOURS (from Excelra Brand Guidelines)
# =============================================================================
DEEP_BLUE = "#0A1E4A"
VIOLET = "#A24DBE"
MAGENTA_PINK = "#E04F8A"
LIGHT_BLUE = "#B3E0F2"
SOFT_LAVENDER = "#E3D9F2"
WHITE = "#FFFFFF"

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Indication Expansion Dashboard | Excelra",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CUSTOM CSS STYLING
# =============================================================================
def load_custom_css():
    """Load custom CSS for Excelra branding."""
    st.markdown(f"""
    <style>
        /* Import Poppins font */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        /* Global font settings */
        html, body, [class*="css"], .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, span, div, label {{
            font-family: 'Poppins', sans-serif !important;
        }}
        
        /* Selectbox and other inputs */
        .stSelectbox label, .stMultiSelect label, .stSlider label, .stRadio label {{
            font-family: 'Poppins', sans-serif !important;
        }}
        
        .stSelectbox [data-baseweb="select"] {{
            font-family: 'Poppins', sans-serif !important;
        }}
        
        /* Main header styling */
        .main-header {{
            background: linear-gradient(135deg, {LIGHT_BLUE} 0%, {WHITE} 50%, {SOFT_LAVENDER} 100%);
            padding: 1.5rem 2rem;
            border-radius: 0 0 20px 20px;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
        }}
        
        .main-header h1 {{
            color: {DEEP_BLUE};
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600;
            margin: 0;
            font-size: 1.8rem;
        }}
        
        .main-header .subtitle {{
            color: {VIOLET};
            font-family: 'Poppins', sans-serif !important;
            font-weight: 400;
            font-size: 1rem;
            margin-top: 0.5rem;
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {WHITE} 0%, {SOFT_LAVENDER} 100%);
        }}
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
            font-family: 'Poppins', sans-serif !important;
        }}
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {{
            color: {DEEP_BLUE};
            font-family: 'Poppins', sans-serif !important;
        }}
        
        /* Card styling */
        .metric-card {{
            background: {WHITE};
            border: 1px solid {LIGHT_BLUE};
            border-radius: 12px;
            padding: 1.25rem;
            box-shadow: 0 2px 8px rgba(10, 30, 74, 0.08);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            font-family: 'Poppins', sans-serif !important;
            height: 130px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }}
        
        .metric-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(10, 30, 74, 0.12);
        }}
        
        .metric-card h3 {{
            color: {DEEP_BLUE};
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600;
            font-size: 0.85rem;
            margin: 0 0 auto 0;
            line-height: 1.3;
            height: 40px;
            display: flex;
            align-items: flex-start;
        }}
        
        .metric-card .value {{
            color: {VIOLET};
            font-family: 'Poppins', sans-serif !important;
            font-weight: 700;
            font-size: 2rem;
            margin-top: auto;
        }}
        
        /* Score badge styling */
        .score-high {{
            background: linear-gradient(135deg, {VIOLET} 0%, {MAGENTA_PINK} 100%);
            color: {WHITE};
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600;
            font-size: 0.875rem;
        }}
        
        .score-medium {{
            background: {LIGHT_BLUE};
            color: {DEEP_BLUE};
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600;
            font-size: 0.875rem;
        }}
        
        .score-low {{
            background: {SOFT_LAVENDER};
            color: {DEEP_BLUE};
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600;
            font-size: 0.875rem;
        }}
        
        /* Stage indicator styling */
        .stage-indicator {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            font-family: 'Poppins', sans-serif !important;
            font-weight: 500;
            font-size: 0.875rem;
        }}
        
        .stage-discovery {{
            background: linear-gradient(135deg, {LIGHT_BLUE} 0%, {SOFT_LAVENDER} 100%);
            color: {DEEP_BLUE};
            border: 2px solid {VIOLET};
        }}
        
        .stage-deepdive {{
            background: linear-gradient(135deg, {VIOLET} 0%, {MAGENTA_PINK} 100%);
            color: {WHITE};
        }}
        
        /* Table styling */
        .dataframe {{
            font-family: 'Poppins', sans-serif !important;
        }}
        
        /* Button styling */
        .stButton > button {{
            background: linear-gradient(135deg, {VIOLET} 0%, {MAGENTA_PINK} 100%);
            color: {WHITE};
            border: none;
            border-radius: 25px;
            padding: 0.5rem 2rem;
            font-weight: 600;
            font-family: 'Poppins', sans-serif !important;
            transition: all 0.3s ease;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(162, 77, 190, 0.4);
        }}
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background: {WHITE};
            border-radius: 8px 8px 0 0;
            border: 1px solid {LIGHT_BLUE};
            border-bottom: none;
            color: {DEEP_BLUE};
            font-family: 'Poppins', sans-serif !important;
            font-weight: 500;
            padding: 0.75rem 1.5rem !important;
            min-width: 160px;
            white-space: nowrap;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, {VIOLET} 0%, {MAGENTA_PINK} 100%);
            color: {WHITE};
        }}
        
        /* Expander styling */
        .streamlit-expanderHeader {{
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600;
            color: {DEEP_BLUE};
        }}
        
        /* Ensure expander labels don't overlap */
        .streamlit-expanderHeader p {{
            margin: 0 !important;
            padding: 0 !important;
        }}
        
        details summary {{
            font-family: 'Poppins', sans-serif !important;
        }}
        
        /* Footer styling */
        .footer {{
            text-align: center;
            padding: 2rem;
            color: {DEEP_BLUE};
            font-family: 'Poppins', sans-serif !important;
            font-size: 0.875rem;
            margin-top: 3rem;
            border-top: 1px solid {LIGHT_BLUE};
        }}
        
        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        
        /* Override Streamlit accent colors - Radio buttons */
        .stRadio > div[role="radiogroup"] > label > div:first-child {{
            background-color: {DEEP_BLUE} !important;
        }}
        
        .stRadio > div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {{
            border-color: {DEEP_BLUE} !important;
        }}
        
        div[data-baseweb="radio"] > div:first-child {{
            background-color: {DEEP_BLUE} !important;
        }}
        
        /* Override Streamlit accent colors - Slider */
        .stSlider > div > div > div > div {{
            background-color: {DEEP_BLUE} !important;
        }}
        
        .stSlider [data-baseweb="slider"] > div:first-child {{
            background: linear-gradient(to right, {DEEP_BLUE} var(--slider-progress), {LIGHT_BLUE} var(--slider-progress)) !important;
        }}
        
        .stSlider [data-baseweb="slider"] > div > div {{
            background-color: {DEEP_BLUE} !important;
        }}
        
        .stSlider [data-baseweb="slider"] > div > div > div {{
            background-color: {DEEP_BLUE} !important;
        }}
        
        .stSlider div[data-testid="stTickBar"] > div {{
            background-color: {DEEP_BLUE} !important;
        }}
        
        /* Slider thumb */
        .stSlider [data-baseweb="slider"] [role="slider"] {{
            background-color: {DEEP_BLUE} !important;
            border-color: {DEEP_BLUE} !important;
        }}
        
        /* Slider track fill */
        .stSlider [data-testid="stSliderTrackFill"] {{
            background-color: {DEEP_BLUE} !important;
        }}
        
        /* Slider value text */
        .stSlider [data-testid="stThumbValue"] {{
            color: {MAGENTA_PINK} !important;
        }}
        
        .stSlider div[data-testid="stTickBarMin"],
        .stSlider div[data-testid="stTickBarMax"] {{
            color: {DEEP_BLUE} !important;
        }}
        
        /* Override tab highlight/underline */
        .stTabs [data-baseweb="tab-highlight"] {{
            background-color: {DEEP_BLUE} !important;
        }}
        
        .stTabs [data-baseweb="tab-border"] {{
            background-color: {DEEP_BLUE} !important;
        }}
        
    </style>
    """, unsafe_allow_html=True)


def get_image_base64(image_path: str) -> str:
    """Convert image to base64 for embedding in HTML."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def render_header():
    """Render the branded header with logo and wave."""
    assets_path = Path(__file__).parent / "assets"
    
    logo_b64 = get_image_base64(assets_path / "logo.png")
    wave_b64 = get_image_base64(assets_path / "wave2.png")
    slogan_b64 = get_image_base64(assets_path / "slogan.png")
    
    # Centred logo above the header - larger and more padding
    st.markdown(f"""
<div style="text-align: center; padding: 0.5rem 0 1rem 0; margin-top: -1rem;">
<img src="data:image/png;base64,{logo_b64}" alt="Excelra" style="height: 60px;">
</div>
""", unsafe_allow_html=True)
    
    # Main header box with wave spanning full width
    st.markdown(f"""
<div class="main-header">
<div style="display: flex; justify-content: space-between; align-items: center; position: relative; z-index: 2;">
<div>
<h1>Indication Expansion & Prioritisation</h1>
<p class="subtitle">Data-driven identification of therapeutic opportunities</p>
</div>
<div style="opacity: 0.6;">
<img src="data:image/png;base64,{slogan_b64}" alt="Where data means more" style="height: 30px;">
</div>
</div>
<img src="data:image/png;base64,{wave_b64}" alt="" 
     style="position: absolute; bottom: 0; left: 0; width: 100%; height: auto; opacity: 0.4; pointer-events: none; z-index: 1;">
</div>
""", unsafe_allow_html=True)


def render_sidebar():
    """Render the sidebar with navigation and target selection."""
    
    with st.sidebar:
        # Target selection (no duplicate logo, no icon)
        st.markdown("### Target Selection")
        
        # For now, just RIPK1 as our demo target
        selected_target = st.selectbox(
            "Select Target",
            options=["RIPK1"],
            index=0,
            help="Select a target to explore indication expansion opportunities",
            key="sidebar_target_select"
        )
        
        st.markdown(f"""
<div style="background: {LIGHT_BLUE}; padding: 1rem; border-radius: 8px; margin-top: 1rem; font-family: 'Poppins', sans-serif;">
<p style="margin: 0; font-size: 0.85rem; color: {DEEP_BLUE}; font-family: 'Poppins', sans-serif;">
<strong>RIPK1</strong><br>
Receptor-Interacting Serine/Threonine-Protein Kinase 1<br><br>
<em>Regulates cell death (necroptosis) and inflammatory signalling pathways.</em>
</p>
</div>
""", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation (no phase terminology)
        st.markdown("### Analysis Stage")
        
        phase = st.radio(
            "Select Stage",
            options=["Indication Discovery", "Deep-Dive Analysis"],
            index=0,
            label_visibility="collapsed",
            key="sidebar_phase_select"
        )
        
        st.markdown("---")
        
        # Info box
        st.markdown(f"""
<div style="background: {WHITE}; padding: 1rem; border-radius: 8px; border-left: 4px solid {VIOLET}; font-family: 'Poppins', sans-serif;">
<p style="margin: 0; font-size: 0.8rem; color: {DEEP_BLUE}; font-family: 'Poppins', sans-serif;">
<strong>About this demo</strong><br>
This interactive prototype demonstrates Excelra's indication expansion 
capabilities using RIPK1 as an example target.
</p>
</div>
""", unsafe_allow_html=True)
        
        return selected_target, phase


def render_footer():
    """Render the branded footer."""
    assets_path = Path(__file__).parent / "assets"
    slogan_b64 = get_image_base64(assets_path / "slogan.png")
    
    st.markdown(f"""
<div class="footer">
<img src="data:image/png;base64,{slogan_b64}" alt="Where data means more" style="height: 25px; margin-bottom: 0.5rem;"><br>
<span style="color: {VIOLET};">www.excelra.com</span> | 
Boston • San Francisco • Ghent • Hyderabad
</div>
""", unsafe_allow_html=True)


# =============================================================================
# MAIN APPLICATION
# =============================================================================
def main():
    """Main application entry point."""
    
    # Load custom styling
    load_custom_css()
    
    # Render header
    render_header()
    
    # Render sidebar and get selections
    selected_target, selected_phase = render_sidebar()
    
    # Main content area
    if "Indication Discovery" in selected_phase:
        render_phase_1(selected_target)
    else:
        render_phase_2(selected_target)
    
    # Render footer
    render_footer()


if __name__ == "__main__":
    main()
