"""
Page Visualisation — Graphiques interactifs Plotly
basés sur les données de la dernière requête SQL.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from filter_utils import fetch_filter_options, FILTER_CONFIG, apply_pandas_filters

st.set_page_config(
    page_title="COPAG — Visualisation",
    page_icon="📊",
    layout="wide"
)

# Logo COPAG Officiel (Placé en haut)
logo_path = os.path.join(os.path.dirname(__file__), "..", "logos", "logo.png")
if os.path.exists(logo_path):
    with st.sidebar:
        col_logo_1, col_logo_2, col_logo_3 = st.columns([1, 4, 1])
        with col_logo_2:
            st.image(logo_path, use_container_width=True)

# CSS partagé pour cohérence
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    /* Style "Dashboard User" */
    [data-testid="stSidebar"] [data-testid="stImage"] {
        padding-top: 20px;
    }
    [data-testid="stSidebarNav"] {
        padding-top: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Visualisation Analytique")
st.caption("Explorez les résultats de votre dernière requête avec des graphiques interactifs.")

# ============================================================
# Vérifier qu'il y a des données disponibles
# ============================================================
if "history" not in st.session_state or not st.session_state.history:
    st.info("💡 Aucune donnée à visualiser. Retournez sur la page **COPAG SQL ASSISTANT** et posez une question d'abord.")
    st.stop()

# Trouver la dernière requête réussie avec des données
last_result = None
for item in st.session_state.history:
    if item.get("ok") and item.get("df") is not None and not item["df"].empty:
        last_result = item
        break

if last_result is None:
    st.info("💡 Aucune requête avec des résultats trouvée.")
    st.stop()

df = last_result["df"].copy()
question = last_result["question"]
global_filters = last_result.get("active_filters", {})

# ============================================================
# SIDEBAR — Filtres & Affinage
# ============================================================
with st.sidebar:
    st.header("🔎 Affinage des Filtres")
    st.caption("Modifiez les filtres pour mettre à jour les graphiques en temps réel.")
    
    filter_options = fetch_filter_options()
    current_filters = {}
    
    for fconf in FILTER_CONFIG:
        # Utiliser la valeur globale comme défaut si disponible
        default_val = global_filters.get(fconf["key"], [])
        
        selected = st.multiselect(
            fconf["label"],
            options=filter_options.get(fconf["key"], []),
            default=default_val,
            key=f"viz_filter_{fconf['key']}"
        )
        if selected:
            current_filters[fconf["key"]] = selected

    if st.button("🔄 Réinitialiser la vue", use_container_width=True):
        st.rerun()

# ============================================================
# APPLIQUER LES FILTRES (Pandas)
# ============================================================
df_filtered, inapplicable = apply_pandas_filters(df, current_filters)

if inapplicable:
    st.warning(f"⚠️ Note : Certains filtres ({', '.join(inapplicable)}) ne peuvent pas être appliqués car ces colonnes ne sont pas présentes dans le résultat SQL actuel.")

if df_filtered.empty:
    st.error("⚠️ Aucun résultat pour cette combinaison de filtres. Veuillez les ajuster.")
    st.stop()

# ============================================================
# Header d'info
# ============================================================
st.markdown(f"**Question source :** *{question}*")
col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("Lignes totales", df.shape[0])
col_m2.metric("Lignes filtrées", df_filtered.shape[0])
col_m3.metric("Colonnes", df_filtered.shape[1])

st.divider()

# ============================================================
# Logique de visualisation
# ============================================================
num_cols = df_filtered.select_dtypes(include=["number"]).columns.tolist()
cat_cols = df_filtered.select_dtypes(exclude=["number"]).columns.tolist()

COLORS = ["#2ECC71", "#3498DB", "#F39C12", "#E74C3C", "#9B59B6", "#1ABC9C"]

if cat_cols and num_cols:
    with st.sidebar:
        st.divider()
        st.header("⚙️ Configuration Axes")
        selected_cat = st.selectbox("Axe X (Catégorie)", cat_cols)
        selected_num = st.selectbox("Axe Y (Valeur)", num_cols)

    # Détection de catégorie pour graphiques intelligents
    try:
        from category_detector import detect_category
        _, cat_conf = detect_category(question, df_filtered)
        charts_to_show = cat_conf["charts"]
    except Exception:
        charts_to_show = ["bar", "donut", "line"]

    # Affichage en grille
    c1, c2 = st.columns(2)
    for i, chart_type in enumerate(charts_to_show[:4]): # Limiter à 4 graphiques max
        target_col = c1 if i % 2 == 0 else c2
        with target_col:
            if chart_type == "bar":
                st.subheader("📊 Performance")
                fig = px.bar(df_filtered, x=selected_cat, y=selected_num, color=selected_cat, color_discrete_sequence=COLORS)
                st.plotly_chart(fig, use_container_width=True)
            elif chart_type == "donut" or chart_type == "pie":
                st.subheader("🥧 Répartition")
                fig = px.pie(df_filtered, names=selected_cat, values=selected_num, hole=0.4, color_discrete_sequence=COLORS)
                st.plotly_chart(fig, use_container_width=True)
            elif chart_type == "line":
                st.subheader("📈 Tendance")
                fig = px.line(df_filtered, x=selected_cat, y=selected_num, markers=True)
                st.plotly_chart(fig, use_container_width=True)
            elif chart_type == "hbar_rank":
                st.subheader("🏆 Classement")
                fig = px.bar(df_filtered.sort_values(selected_num), x=selected_num, y=selected_cat, orientation='h')
                st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Structure de données simple — Affichage tableau uniquement.")
    st.dataframe(df_filtered, use_container_width=True)

st.divider()
with st.expander("📋 Données détaillées"):
    st.dataframe(df_filtered, use_container_width=True)
