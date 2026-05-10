import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
from vanna_setup import vn

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

results = {}
for name, query in queries.items():
    try:
        df = vn.run_sql(query)
        if df is not None and not df.empty:
            results[name] = df.iloc[:, 0].dropna().unique().tolist()
        else:
            results[name] = []
    except Exception as e:
        print(f"Error for {name}: {e}")

print(results)
