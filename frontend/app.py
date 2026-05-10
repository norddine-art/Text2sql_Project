"""
Interface Dashboard COPAG — Text-to-SQL avec Vanna (Design Tailwind)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import streamlit as st
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from vanna_setup import vn
from filter_utils import fetch_filter_options, FILTER_CONFIG, get_filter_context, apply_pandas_filters, extract_filters_from_question

load_dotenv()

st.set_page_config(
    page_title="COPAG SQL ASSISTANT",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

import json

TAILWIND_CONFIG_DICT = {
  "darkMode": "class",
  "theme": {
    "extend": {
      "colors": {
              "primary": "#00342b",
              "primary-container": "#004d40",
              "on-primary-container": "#7ebdac",
              "on-primary": "#ffffff",
              "surface": "#f7f9fb",
              "surface-bright": "#f7f9fb",
              "on-surface": "#191c1e",
              "on-surface-variant": "#3f4945",
              "outline-variant": "#bfc9c4",
              "background": "#f7f9fb",
              "on-background": "#191c1e",
              "secondary-container": "#1257a3",
              "error": "#ba1a1a",
              "error-container": "#ffdad6",
              "surface-variant": "#e0e3e5",
      },
      "borderRadius": {
              "DEFAULT": "0.25rem",
              "lg": "0.5rem",
              "xl": "0.75rem",
              "full": "9999px"
      },
      "fontFamily": {
              "headline-md": ["Geist"],
              "body-md": ["Inter"],
              "body-lg": ["Inter"],
              "data-mono": ["Geist"],
              "label-caps": ["Geist"],
      }
    }
  }
}

tailwind_config_str = "tailwind.config = " + json.dumps(TAILWIND_CONFIG_DICT)

js_code = f"""
    if (!window.tailwindLoaded) {{
        window.tailwindLoaded = true;
        const link1 = document.createElement('link'); link1.href = 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap'; link1.rel = 'stylesheet'; document.head.appendChild(link1);
        const link2 = document.createElement('link'); link2.href = 'https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Inter:wght@400;500&display=swap'; link2.rel = 'stylesheet'; document.head.appendChild(link2);
        const config = document.createElement('script'); config.innerHTML = `{tailwind_config_str}`; document.head.appendChild(config);
        const script = document.createElement('script'); script.src = 'https://cdn.tailwindcss.com?plugins=forms,container-queries'; document.head.appendChild(script);
    }}
"""
onerror_attr = js_code.replace('"', '&quot;')

st.markdown(f'<img src="x" onerror="{onerror_attr}" style="display:none;">', unsafe_allow_html=True)

st.markdown("""
<style>
/* Masquer UI Streamlit par défaut */
#MainMenu {{visibility: hidden;}}
header {{visibility: hidden;}}
footer {{visibility: hidden;}}
.stDeployButton {{display:none;}}

/* Remapping fonts */
html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background-color: #f7f9fb;
    color: #191c1e;
}}

/* Custom Sidebar */
[data-testid="stSidebar"] {{
    background-color: #f7f9fb !important;
    border-right: 1px solid rgba(191, 201, 196, 0.3) !important;
    min-width: 280px !important;
    max-width: 280px !important;
}}
[data-testid="stSidebar"] > div:first-child {{
    padding: 0 !important;
}}

/* Custom Main Area */
.main .block-container {{
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
    max-width: 1280px;
}}

/* Custom Text Input (Search bar) */
div[data-testid="stTextInput"] > div > div > input {{
    background-color: rgba(255, 255, 255, 0.8) !important;
    border: 1px solid rgba(191, 201, 196, 0.5) !important;
    border-radius: 0.75rem !important;
    padding: 1.25rem 1rem 1.25rem 3rem !important;
    font-size: 1.125rem !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.04) !important;
    color: #191c1e !important;
}}
div[data-testid="stTextInput"] > div > div > input:focus {{
    border-color: #00342b !important;
    box-shadow: 0 0 0 1px #00342b !important;
}}

/* Custom Primary Button */
div[data-testid="stButton"] > button[kind="primary"] {{
    background-color: #00342b !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 0.5rem !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}}
div[data-testid="stButton"] > button[kind="primary"]:hover {{
    background-color: #004d40 !important;
    transform: translateY(-1px);
}}

/* Secondary Button */
div[data-testid="stButton"] > button[kind="secondary"] {{
    background-color: transparent !important;
    color: #3f4945 !important;
    border: 1px solid rgba(191, 201, 196, 0.5) !important;
    border-radius: 0.5rem !important;
}}
div[data-testid="stButton"] > button[kind="secondary"]:hover {{
    border-color: #00342b !important;
    color: #00342b !important;
}}

/* Multiselect Filters */
[data-baseweb="select"] {{
    border-radius: 0.5rem;
}}

/* Custom Cards */
.glass-panel {{
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(0, 52, 43, 0.08);
    border-radius: 0.75rem;
    padding: 1.5rem;
}}
.glass-panel-heavy {{
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(0, 52, 43, 0.12);
    border-radius: 0.75rem;
    padding: 1.5rem;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}}
</style>
""", unsafe_allow_html=True)

# Client Groq pour la description IA
desc_client = OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))

def generate_description(question, sql, df):
    if df is None or df.empty: return None
    try:
        data_preview = df.head(10).to_string(index=False)
        prompt = f"Tu es un analyste chez COPAG. Question : '{question}'. SQL : '{sql}'. Données : {data_preview}. Rédige une analyse claire en français (3-4 phrases)."
        response = desc_client.chat.completions.create(
            model=os.getenv("MODEL", "llama-3.3-70b-versatile"),
            messages=[{"role": "user", "content": prompt}], max_tokens=300, temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e: return f"⚠️ Erreur IA : {e}"

# --- LOGIQUE D'EXTRACTION PRÉVENTIVE ---
if "question_input" in st.session_state and st.session_state.question_input:
    q = st.session_state.question_input
    if st.session_state.get("last_extracted_q") != q:
        extracted = extract_filters_from_question(q)
        if extracted:
            for f_key, f_vals in extracted.items():
                st.session_state[f"global_filter_{f_key}"] = f_vals
            st.session_state["last_extracted_q"] = q

# --- SIDEBAR EXACT DESIGN ---
with st.sidebar:
    # Top Header (Logo + Title) HTML
    import base64
    logo_path = os.path.join(os.path.dirname(__file__), "logos", "logo.png")
    logo_b64 = ""
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
    
    st.markdown(f"""
    <div class="flex items-center gap-2 p-6 mb-2">
        <img src="data:image/png;base64,{logo_b64}" class="w-10 h-10 object-contain bg-white rounded-lg p-1 border border-outline-variant/30" />
        <div>
            <h1 class="font-bold text-[#00342b] leading-none text-xl" style="font-family:'Geist'">COPAG SQL</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='px-6'>", unsafe_allow_html=True)
    if st.button("➕ New Query", use_container_width=True, type="primary"):
        st.session_state.history = []
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='px-6 mt-8 mb-4 font-bold text-xs text-[#3f4945] uppercase tracking-wider' style='font-family:Geist;'>Filtres Globaux</div>", unsafe_allow_html=True)
    
    # Streamlit Widgets styled via CSS
    filter_options = fetch_filter_options()
    active_filters = {}
    
    st.markdown("<div class='px-4'>", unsafe_allow_html=True)
    for fconf in FILTER_CONFIG:
        opts = filter_options.get(fconf["key"], [])
        selected = st.multiselect(
            fconf["label"],
            options=opts,
            default=[],
            key=f"global_filter_{fconf['key']}"
        )
        if selected:
            active_filters[fconf["key"]] = selected
    
    if active_filters:
        st.markdown("<div class='mt-6'>", unsafe_allow_html=True)
        if st.button("🔄 Réinitialiser", use_container_width=True):
            for fconf in FILTER_CONFIG:
                if f"global_filter_{fconf['key']}" in st.session_state:
                    st.session_state[f"global_filter_{fconf['key']}"] = []
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- MAIN APP ---
if "history" not in st.session_state:
    st.session_state.history = []

# Top Navbar HTML (Fake just for design)
st.markdown("""
<header class="fixed top-0 right-0 w-[calc(100%-280px)] z-40 backdrop-blur-md border-b border-[#bfc9c4]/30 flex justify-between items-center h-16 px-8 bg-[#f7f9fb]/80">
    <div class="flex items-center gap-6">
    </div>
</header>
<div style="margin-top: 4rem;"></div>
""", unsafe_allow_html=True)

# App State Control
if not st.session_state.history:
    # ETAT INITIAL
    st.markdown("""
    <div class="flex flex-col items-center justify-center mt-24 mb-8 text-center">
        <h2 class="text-4xl font-bold text-[#00342b] mb-4 tracking-tight" style="font-family:'Geist'">Bonjour, comment puis-je vous aider ?</h2>
        <p class="text-lg text-[#3f4945]">Interrogez la base de données COPAG en langage naturel.</p>
    </div>
    """, unsafe_allow_html=True)

    col_empty, col_search, col_btn, col_empty2 = st.columns([1, 6, 2, 1])
    with col_search:
        # We rely on CSS to style this input
        question = st.text_input("Recherche", label_visibility="collapsed", placeholder="Ex: Montre-moi les ventes du secteur Laitier pour 2023...", key="question_input")
    with col_btn:
        st.write("") # padding
        submit = st.button("Analyser ➔", use_container_width=True, type="primary")
    

else:
    # ETAT RESULTATS
    # Show search bar at the top, smaller
    col1, col2 = st.columns([8, 2])
    with col1:
        question = st.text_input("Nouvelle question", label_visibility="collapsed", placeholder="Posez une autre question...", key="question_input")
    with col2:
        submit = st.button("Analyser", use_container_width=True, type="primary")

if submit and question.strip():
    filter_context = get_filter_context(active_filters)
    augmented_question = question + filter_context
    
    with st.spinner("Analyse des données en cours..."):
        try:
            sql = vn.generate_sql(augmented_question)
            df_raw = vn.run_sql(sql)
            df, _ = apply_pandas_filters(df_raw, active_filters)
            description = generate_description(question, sql, df)
            st.session_state.history.insert(0, {
                "question": question, "sql": sql, "df": df, "description": description, "ok": True
            })
            st.rerun() # Refresh to show results
        except Exception as e:
            st.session_state.history.insert(0, {
                "question": question, "sql": str(e), "df": None, "description": None, "ok": False
            })
            st.rerun()

# Affichage de l'historique
if st.session_state.history:
    st.markdown("<div class='mt-8'></div>", unsafe_allow_html=True)
    for i, item in enumerate(st.session_state.history):
        if i == 0:
            # Latest result (Expanded View matching exactly the HTML Dashboard Results)
            if item["ok"]:
                df = item["df"]
                
                # Header
                st.markdown(f"""
                <div class="mb-6">
                    <div class="flex items-center gap-2 mb-2">
                        <span class="material-symbols-outlined text-[#00342b] text-sm">chat_bubble</span>
                        <span class="text-xs font-bold text-[#00342b] uppercase tracking-wider" style="font-family:'Geist'">Requête</span>
                    </div>
                    <h2 class="text-2xl font-bold text-[#191c1e] mb-4">"{item['question']}"</h2>
                </div>
                """, unsafe_allow_html=True)
                
                # Cards
                if df is not None and not df.empty:
                    # Dynamically calculate some stats if possible (just for show based on REAL data)
                    cols = df.select_dtypes(include=['number']).columns
                    stat1_val = f"{len(df)}"
                    stat1_label = "Lignes extraites"
                    stat2_val = "-"
                    stat2_label = "Total"
                    if len(cols) > 0:
                        sum_val = df[cols[0]].sum()
                        if sum_val > 1000000:
                            stat2_val = f"{sum_val/1000000:.1f}M"
                        else:
                            stat2_val = f"{sum_val:,.0f}"
                        stat2_label = f"Total {cols[0]}"
                        
                    st.markdown(f"""
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8">
                        <div class="glass-panel-heavy flex flex-col justify-between hover:shadow-md transition-shadow">
                            <span class="text-xs font-bold text-[#3f4945] uppercase tracking-wider" style="font-family:'Geist'">{stat1_label}</span>
                            <div class="mt-2"><span class="text-3xl font-bold text-[#00342b]">{stat1_val}</span></div>
                        </div>
                        <div class="glass-panel-heavy flex flex-col justify-between hover:shadow-md transition-shadow">
                            <span class="text-xs font-bold text-[#3f4945] uppercase tracking-wider" style="font-family:'Geist'">{stat2_label}</span>
                            <div class="mt-2"><span class="text-3xl font-bold text-[#00342b]">{stat2_val}</span></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Split AI Insight & Data
                st.markdown(f"""
                <div class="glass-panel-heavy rounded-xl p-6 border-l-4 border-l-[#1257a3] flex flex-col mb-8">
                    <div class="flex items-center gap-2 mb-4">
                        <span class="material-symbols-outlined text-[#1257a3]">auto_awesome</span>
                        <h3 class="text-xl font-semibold text-[#191c1e]" style="font-family:'Geist'">AI Insight</h3>
                    </div>
                    <p class="text-[#3f4945] text-lg">{item.get('description', 'Aucune description disponible.')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Data Table Container
                st.markdown('<div class="glass-panel p-0 overflow-hidden mb-8 border border-[#bfc9c4]/30 shadow-sm">', unsafe_allow_html=True)
                st.markdown('<div class="p-4 border-b border-[#bfc9c4]/30 bg-white/50"><h3 class="text-lg font-semibold text-[#191c1e]" style="font-family:\'Geist\'">Données Détaillées</h3></div>', unsafe_allow_html=True)
                if df is not None and not df.empty:
                    # Injecting a bit of padding for the dataframe
                    st.markdown('<div class="p-4">', unsafe_allow_html=True)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.warning("Aucune donnée trouvée.")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # SQL Code Expandable
                with st.expander("💻 Voir le code SQL"):
                    st.code(item["sql"], language="sql")
            else:
                st.error(f"Erreur : {item['sql']}")
        else:
            # Previous queries collapsed
            with st.expander(f"🕒 Historique : {item['question']}"):
                if item["ok"] and item["df"] is not None:
                    st.dataframe(item["df"].head(5))
                    st.code(item["sql"], language="sql")
                else:
                    st.error(item['sql'])
