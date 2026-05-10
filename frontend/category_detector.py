"""
Module de détection de catégorie et mapping des graphiques.
Détecte automatiquement la catégorie d'une question et renvoie
les types de graphiques compatibles.
"""

# ============================================================
# CATÉGORIES ET MOTS-CLÉS DE DÉTECTION
# ============================================================
CATEGORIES = {
    "TENDANCE_TEMPORELLE": {
        "label": "📈 Évolution temporelle",
        "keywords": ["par mois", "par année", "par annee", "évolution", "evolution",
                     "tendance", "mensuel", "annuel", "trimestre", "semestre",
                     "s1 vs s2", "s1 vs", "vs s2", "historique", "croissance",
                     "par date", "par jour", "période", "periode"],
        "columns": ["mois", "annee", "année", "date", "jour", "month", "year"],
        "charts": ["line", "area", "bar_group"],
        "description": "Évolution dans le temps — courbes et tendances"
    },
    "CLASSEMENT_PRODUIT": {
        "label": "🏆 Classement produits",
        "keywords": ["top 10", "top 5", "top 20", "les plus vendus", "les plus",
                     "meilleur", "classement", "ranking", "par article",
                     "par produit", "le plus vendu", "les moins"],
        "columns": ["article_name", "article"],
        "charts": ["hbar_rank", "bar", "treemap"],
        "description": "Classement et performance des produits"
    },
    "REPARTITION_PRODUIT": {
        "label": "📦 Répartition par gamme/famille",
        "keywords": ["par gamme", "par famille", "par sous-famille", "par sous_famille",
                     "part de marché", "part de marche", "répartition", "repartition",
                     "par catégorie", "par categorie"],
        "columns": ["gamme_name", "gamme", "famille_name", "famille",
                     "sous_famille_name", "sous_famille"],
        "charts": ["donut", "bar", "treemap"],
        "description": "Distribution par gamme, famille ou sous-famille"
    },
    "ANALYSE_GEOGRAPHIQUE": {
        "label": "🗺️ Analyse géographique",
        "keywords": ["par région", "par region", "par secteur", "par agence",
                     "par ville", "géographique", "geographique", "zone",
                     "territoriale"],
        "columns": ["region", "secteur_name", "secteur", "agence_name",
                     "agence", "ville"],
        "charts": ["bar", "hbar_rank", "donut"],
        "description": "Performance par zone géographique"
    },
    "ANALYSE_CLIENT": {
        "label": "👤 Analyse clients / canaux",
        "keywords": ["par canal", "par client", "type de client", "canal de distribution",
                     "nombre de clients", "panier moyen", "clients actifs",
                     "fidélité", "fidelite"],
        "columns": ["canal", "nom_client", "code_client"],
        "charts": ["donut", "bar", "hbar_rank"],
        "description": "Segmentation et analyse des clients et canaux"
    },
    "RETOURS_INVENDUS": {
        "label": "↩️ Retours et invendus",
        "keywords": ["retour", "rendu", "invendu", "taux de retour",
                     "taux d'invendu", "retourné", "retourne", "perte"],
        "columns": ["qty_rendu", "qty_invendu", "taux_retour", "taux_invendu",
                     "total_retours", "total_invendus"],
        "charts": ["bar_compare", "hbar_rank", "indicator"],
        "description": "Analyse des retours, invendus et pertes"
    },
    "PROMOTIONS": {
        "label": "🎯 Promotions",
        "keywords": ["promo", "promotion", "promotionnel", "qty_promo",
                     "taux de promo", "ventes promo"],
        "columns": ["qty_promo", "taux_promo", "ventes_promo", "pct_promo"],
        "charts": ["stacked_bar", "donut", "bar"],
        "description": "Impact des promotions sur les ventes"
    },
    "COMPARAISON": {
        "label": "⚖️ Comparaison",
        "keywords": ["comparer", "comparaison", "versus", " vs ", "différence",
                     "difference", "rapport entre", "par rapport"],
        "columns": ["ca_s1", "ca_s2", "ca_brut", "ca_net"],
        "charts": ["bar_group", "line", "bar_compare"],
        "description": "Comparaison entre plusieurs métriques"
    },
    "VUE_GLOBALE": {
        "label": "📊 Vue globale",
        "keywords": ["total", "combien", "nombre de", "quantité totale",
                     "chiffre d'affaires total", "ca total"],
        "columns": [],
        "charts": ["indicator", "bar", "donut"],
        "description": "Indicateurs clés et vue d'ensemble"
    },
}


def detect_category(question, df):
    """
    Détecte la catégorie de la question en combinant :
    1. Analyse des mots-clés dans la question
    2. Analyse des colonnes du DataFrame
    Retourne (category_key, category_config)
    """
    question_lower = question.lower().strip()
    scores = {}

    for cat_key, cat_conf in CATEGORIES.items():
        score = 0

        # Score par mots-clés (poids 2 par match)
        for kw in cat_conf["keywords"]:
            if kw in question_lower:
                score += 2

        # Score par colonnes présentes dans le DataFrame (poids 1 par match)
        if df is not None:
            df_cols_lower = [c.lower() for c in df.columns.tolist()]
            for col in cat_conf["columns"]:
                if col.lower() in df_cols_lower:
                    score += 1

        scores[cat_key] = score

    # Prendre la catégorie avec le score le plus élevé
    best_cat = max(scores, key=scores.get)

    # Si aucun score > 0, fallback vers VUE_GLOBALE
    if scores[best_cat] == 0:
        best_cat = "VUE_GLOBALE"

    return best_cat, CATEGORIES[best_cat]
