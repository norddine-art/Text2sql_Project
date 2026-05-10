import os
import sqlite3
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

@st.cache_data(ttl=3600)
def fetch_filter_options():
    """Fetch distinct values for all filters directly from the database."""
    db_path = os.getenv("DB_PATH")
    options = {}
    if not db_path or not os.path.exists(db_path):
        return options
        
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        queries = {
            "Secteur / Région": "SELECT DISTINCT region FROM SECTEUR UNION SELECT DISTINCT secteur_name FROM SECTEUR",
            "Agence": "SELECT DISTINCT agence_name FROM AGENCE",
            "Gamme": "SELECT DISTINCT gamme_name FROM GAMME",
            "Famille": "SELECT DISTINCT famille_name FROM FAMILLE",
            "Sous-famille": "SELECT DISTINCT sous_famille_name FROM SOUS_FAMILLE",
            "Article": "SELECT DISTINCT article_name FROM ARTICLE",
            "Année": "SELECT DISTINCT annee FROM DATE_DIM",
            "Mois": "SELECT DISTINCT mois FROM DATE_DIM",
            "Canal client": "SELECT DISTINCT canal FROM CLIENT"
        }
        
        for name, q in queries.items():
            cursor.execute(q)
            # Fetch all, convert to string, remove Nones, and sort
            res = sorted([str(r[0]) for r in cursor.fetchall() if r[0] is not None])
            options[name] = res
            
        conn.close()
    except Exception as e:
        print(f"Error fetching filter options: {e}")
        
    return options

FILTER_CONFIG = [
    {"label": "🏢 Secteur / Région",  "key": "Secteur / Région", "columns": ["region", "secteur_name", "secteur"]},
    {"label": "🏛️ Agence",            "key": "Agence",           "columns": ["agence_name", "agence", "ville"]},
    {"label": "🎯 Gamme",             "key": "Gamme",            "columns": ["gamme_name", "gamme"]},
    {"label": "📦 Famille",           "key": "Famille",          "columns": ["famille_name", "famille"]},
    {"label": "📂 Sous-famille",      "key": "Sous-famille",     "columns": ["sous_famille_name", "sous_famille"]},
    {"label": "🏷️ Article",           "key": "Article",          "columns": ["article_name", "article"]},
    {"label": "📅 Année",             "key": "Année",            "columns": ["annee", "année", "year"]},
    {"label": "📅 Mois",              "key": "Mois",             "columns": ["mois", "month"]},
    {"label": "👤 Canal client",      "key": "Canal client",     "columns": ["canal", "nom_client", "client"]},
]

def get_filter_context(active_filters):
    """
    Constructs a textual context to append to the LLM question 
    to force filtering at the SQL level with explicit column hints.
    """
    if not active_filters:
        return ""
    
    context_parts = []
    for filter_name, values in active_filters.items():
        if values:
            # Find matching config to get primary column
            primary_col = None
            for fconf in FILTER_CONFIG:
                if fconf["key"] == filter_name:
                    primary_col = fconf["columns"][0] # Use the first column as the primary hint
                    break
            
            val_str = ", ".join([f"'{v}'" if isinstance(v, str) else str(v) for v in values])
            if primary_col:
                context_parts.append(f"La colonne '{primary_col}' (ou équivalent) doit être filtrée avec les valeurs : ({val_str})")
            else:
                context_parts.append(f"{filter_name} est parmi ({val_str})")
    
    if context_parts:
        return "\n\nCRITICAL: Applique STRICTEMENT les filtres suivants dans ta requête SQL (clause WHERE) :\n- " + "\n- ".join(context_parts)
    return ""

def extract_filters_from_question(question):
    """
    Uses an LLM to extract potential filter values from the user's question.
    Returns a dictionary of {filter_key: [values]}.
    """
    import json
    from openai import OpenAI
    
    client = OpenAI(
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("BASE_URL")
    )
    
    # Prepare a summary of available filter options for the prompt (limited to avoid token bloat)
    # But actually, it's better to just give the keys and labels.
    filter_keys = [f["key"] for f in FILTER_CONFIG]
    
    prompt = f"""Tu es un extracteur de filtres pour un système Text-to-SQL.
L'utilisateur pose cette question : "{question}"

Identifie si l'utilisateur mentionne des valeurs correspondant à ces catégories de filtres :
{', '.join(filter_keys)}

IMPORTANT : 
- Retourne UNIQUEMENT un objet JSON.
- Les clés du JSON doivent être exactement parmi celles listées ci-dessus.
- Les valeurs doivent être des listes de chaînes.
- Si un filtre n'est pas mentionné, ne l'inclus pas dans le JSON.
- Sois intelligent : "en 2024" -> {{"Année": ["2024"]}}, "à Agadir" -> {{"Agence": ["Agadir"]}} ou {{"Secteur / Région": ["Agadir"]}}.

Exemple de réponse :
{{"Année": ["2024"], "Agence": ["AGADIR"]}}
"""

    try:
        response = client.chat.completions.create(
            model=os.getenv("MODEL", "llama-3.3-70b-versatile"),
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }, # Force JSON if supported
            temperature=0
        )
        content = response.choices[0].message.content.strip()
        # Clean potential markdown block if the model ignored response_format
        if content.startswith("```json"):
            content = content[7:-3].strip()
        
        extracted = json.loads(content)
        return extracted
    except Exception as e:
        print(f"Error extracting filters: {e}")
        return {}

def apply_pandas_filters(df, active_filters_config):
    # (Same as before, keeping it for completeness in the file)
    if df is None or df.empty or not active_filters_config:
        return df, []

    df_filtered = df.copy()
    applied_filters = []
    inapplicable_filters = []

    for f_key, values in active_filters_config.items():
        if not values:
            continue
            
        # Find which column in the DF matches this filter key
        matched_col = None
        for fconf in FILTER_CONFIG:
            if fconf["key"] == f_key:
                for col in fconf["columns"]:
                    if col in df_filtered.columns:
                        matched_col = col
                        break
                break
        
        if matched_col:
            try:
                # Convert both to string for robust comparison
                df_filtered = df_filtered[df_filtered[matched_col].astype(str).isin([str(v) for v in values])]
                applied_filters.append(f_key)
            except Exception:
                inapplicable_filters.append(f_key)
        else:
            inapplicable_filters.append(f_key)
            
    return df_filtered, inapplicable_filters
