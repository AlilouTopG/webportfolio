"""
Streamlit Cloud wrapper — serves the same OLED cyberpunk portfolio.
Keeps a single codebase deployable to GitHub Pages (static) AND Streamlit Cloud.
"""
import streamlit as st
from pathlib import Path
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Industrial & Systems Engineer — Portfolio",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Streamlit Cloud injects this wrapper; we embed the static site inside an iframe-friendly component.
# Simpler: read index.html + inline CSS/JS and render as HTML.

ROOT = Path(__file__).parent
html_path = ROOT / "index.html"
css_path = ROOT / "css" / "style.css"
js_path = ROOT / "js" / "main.js"

html = html_path.read_text(encoding="utf-8")
css = css_path.read_text(encoding="utf-8")
js = js_path.read_text(encoding="utf-8")

# Inline assets for Streamlit (which can't serve relative css/js reliably)
html = html.replace('<link rel="stylesheet" href="css/style.css">', f"<style>{css}</style>")
html = html.replace('<script src="js/main.js"></script>', f"<script>{js}</script>")

# Hide Streamlit chrome for a clean portfolio look
st.markdown("""
<style>
  #MainMenu, header[data-testid="stHeader"], footer { visibility: hidden; }
  .block-container { padding: 0 !important; max-width: 100% !important; }
  [data-testid="stAppViewContainer"] { background: #0A0A0A; }
  iframe { border: none; }
</style>
""", unsafe_allow_html=True)

components.html(html, height=4200, scrolling=True)
