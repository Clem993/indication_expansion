# KRAS Indication Expansion & Prioritisation Dashboard

## Excelra Sales Demonstration Prototype

This interactive Streamlit dashboard demonstrates Excelra's indication expansion and prioritisation capabilities, powered by the GRIP (Global Repurposing Integrated Platform) methodology.

---

## Features

### 1. Summary Counters
- Total indications identified
- Breakdown by prioritisation tier (Tier 1/2/3)
- Clinical evidence status

### 2. Frequency Table
- Interactive, sortable table showing all identified indications
- Colour-coded by tier priority
- Evidence source matrix (Literature, Clinical Trials, Adverse Events, Gene Expression, GWAS, Interactome, Pathway Similarity, Structure Similarity)
- Filterable by tier, therapeutic area, clinical status, and minimum score

### 3. Network Visualisation
- Interactive graph showing Target → Pathway → Indication relationships
- Colour-coded nodes by entity type
- Demonstrates biological rationale for indication prioritisation

### 4. Indication Deep Dive
- Detailed view of individual indications
- Scientific hypothesis
- Key pathways involved
- Supporting references (linked to PubMed/ClinicalTrials.gov)

---

## Installation

```bash
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Running the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your default browser at `http://localhost:8501`

---

## Sales Demo Usage

### Before the Call
- Launch the dashboard locally
- Ensure stable internet for any external links

### During the Call
1. **Start with Summary Counters** - Quick overview of analysis scope
2. **Show Frequency Table** - Demonstrate the systematic, data-driven approach
3. **Navigate Network** - Explain biological rationale visually
4. **Deep Dive** - Click on a high-priority indication to show detail

### Key Talking Points
- "This analysis identified X indications across multiple therapeutic areas"
- "Tier 1 indications have the strongest evidence convergence"
- "Each indication is scored based on 8 independent evidence sources"
- "The network shows the biological rationale connecting target to disease"
- "We can customise this for any target of interest"

---

## Customisation

### Changing the Target
The prototype currently uses KRAS as the example target. To adapt for other targets:

1. Update the `load_kras_indication_data()` function with target-specific data
2. Update the `get_network_data()` function with relevant pathways
3. Modify the title and branding as needed

### Adding New Evidence Sources
The evidence matrix can be extended by adding columns to the data structure in `load_kras_indication_data()`.

---

## Data Sources (Simulated)

This prototype uses simulated data based on publicly available KRAS biology. In a real engagement, data would be sourced from:

- **GRIP** - Excelra's Global Repurposing Integrated Database
- Literature mining from PubMed/MEDLINE
- ClinicalTrials.gov registry
- FDA FAERS adverse event database
- GEO/TCGA gene expression data
- GWAS Catalog
- Protein-protein interaction databases
- Chemical structure similarity analysis

---

## Technical Stack

- **Streamlit** - Web application framework
- **Pandas** - Data manipulation
- **Plotly** - Interactive visualisations
- **NetworkX** - Network graph construction

---

## Brand Guidelines

The dashboard follows Excelra brand guidelines:
- Primary colours: Deep Blue (#0A1E4A), Violet (#A24DBE), Magenta-Pink (#E04F8A)
- Typography: Poppins font family
- Visual style: Clean, professional, data-driven

---

## Support

For questions about this prototype or Excelra's indication expansion services, contact your Excelra representative.

**Excelra** | Where data means more
Boston | San Francisco | Ghent | Hyderabad
