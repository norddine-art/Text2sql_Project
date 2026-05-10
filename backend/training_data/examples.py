TRAINING_EXAMPLES = [

    # BLOC 1 — VENTES GLOBALES
    {
        "question": "Quel est le chiffre d'affaires total toutes années confondues ?",
        "sql": "SELECT SUM(f.qty_unite * f.prix_vente) AS chiffre_affaires_total FROM FACT_SALES f"
    },
    {
        "question": "Quel est le chiffre d'affaires total par année ?",
        "sql": """SELECT d.annee, SUM(f.qty_unite * f.prix_vente) AS chiffre_affaires
FROM FACT_SALES f JOIN DATE_DIM d ON f.date_id = d.id_date
GROUP BY d.annee ORDER BY d.annee"""
    },
    {
        "question": "Quel est le chiffre d'affaires par mois pour l'année 2024 ?",
        "sql": """SELECT d.mois, SUM(f.qty_unite * f.prix_vente) AS chiffre_affaires
FROM FACT_SALES f JOIN DATE_DIM d ON f.date_id = d.id_date
WHERE d.annee = 2024 GROUP BY d.mois ORDER BY d.mois"""
    },
    {
        "question": "Combien de transactions de vente ont été enregistrées au total ?",
        "sql": "SELECT COUNT(f.id_fact) AS nombre_transactions FROM FACT_SALES f"
    },
    {
        "question": "Quelle est la quantité totale d'articles vendus par année ?",
        "sql": """SELECT d.annee, SUM(f.qty_unite) AS quantite_totale_vendue
FROM FACT_SALES f JOIN DATE_DIM d ON f.date_id = d.id_date
GROUP BY d.annee ORDER BY d.annee"""
    },

    # BLOC 2 — ARTICLES ET PRODUITS
    {
        "question": "Quels sont les 10 articles les plus vendus en quantité ?",
        "sql": """SELECT a.article_name, SUM(f.qty_unite) AS quantite_vendue
FROM FACT_SALES f JOIN ARTICLE a ON f.article_id = a.id_article
GROUP BY a.article_name ORDER BY quantite_vendue DESC LIMIT 10"""
    },
    {
        "question": "Quels sont les 10 articles qui génèrent le plus de chiffre d'affaires ?",
        "sql": """SELECT a.article_name, SUM(f.qty_unite * f.prix_vente) AS chiffre_affaires
FROM FACT_SALES f JOIN ARTICLE a ON f.article_id = a.id_article
GROUP BY a.article_name ORDER BY chiffre_affaires DESC LIMIT 10"""
    },
    {
        "question": "Quel est le chiffre d'affaires par gamme de produits ?",
        "sql": """SELECT g.gamme_name, SUM(f.qty_unite * f.prix_vente) AS chiffre_affaires
FROM FACT_SALES f
JOIN ARTICLE a ON f.article_id = a.id_article
JOIN SOUS_FAMILLE sf ON a.sous_famille_id = sf.id_sous_famille
JOIN FAMILLE fa ON sf.famille_id = fa.id_famille
JOIN GAMME g ON fa.gamme_id = g.id_gamme
GROUP BY g.gamme_name ORDER BY chiffre_affaires DESC"""
    },
    {
        "question": "Quel est le chiffre d'affaires par famille de produits ?",
        "sql": """SELECT fa.famille_name, SUM(f.qty_unite * f.prix_vente) AS chiffre_affaires
FROM FACT_SALES f
JOIN ARTICLE a ON f.article_id = a.id_article
JOIN SOUS_FAMILLE sf ON a.sous_famille_id = sf.id_sous_famille
JOIN FAMILLE fa ON sf.famille_id = fa.id_famille
GROUP BY fa.famille_name ORDER BY chiffre_affaires DESC"""
    },
    {
        "question": "Quel est le chiffre d'affaires par sous-famille de produits ?",
        "sql": """SELECT sf.sous_famille_name, SUM(f.qty_unite * f.prix_vente) AS chiffre_affaires
FROM FACT_SALES f
JOIN ARTICLE a ON f.article_id = a.id_article
JOIN SOUS_FAMILLE sf ON a.sous_famille_id = sf.id_sous_famille
GROUP BY sf.sous_famille_name ORDER BY chiffre_affaires DESC"""
    },
    {
        "question": "Quel est le prix de vente moyen par article ?",
        "sql": """SELECT a.article_name, AVG(f.prix_vente) AS prix_moyen
FROM FACT_SALES f JOIN ARTICLE a ON f.article_id = a.id_article
GROUP BY a.article_name ORDER BY prix_moyen DESC"""
    },
    {
        "question": "Quels articles ont un taux de retour supérieur à 10% ?",
        "sql": """SELECT a.article_name,
    SUM(f.qty_unite) AS quantite_vendue,
    SUM(f.qty_rendu) AS quantite_retournee,
    ROUND(100.0 * SUM(f.qty_rendu) / NULLIF(SUM(f.qty_unite), 0), 2) AS taux_retour_pct
FROM FACT_SALES f JOIN ARTICLE a ON f.article_id = a.id_article
GROUP BY a.article_name
HAVING taux_retour_pct > 10 ORDER BY taux_retour_pct DESC"""
    },

    # BLOC 3 — GÉOGRAPHIE
    {
        "question": "Quel est le chiffre d'affaires par région ?",
        "sql": """SELECT s.region, SUM(f.qty_unite * f.prix_vente) AS chiffre_affaires
FROM FACT_SALES f JOIN SECTEUR s ON f.secteur_id = s.id_secteur
GROUP BY s.region ORDER BY chiffre_affaires DESC"""
    },
    {
        "question": "Quel est le chiffre d'affaires par secteur commercial ?",
        "sql": """SELECT s.secteur_name, s.region, SUM(f.qty_unite * f.prix_vente) AS chiffre_affaires
FROM FACT_SALES f JOIN SECTEUR s ON f.secteur_id = s.id_secteur
GROUP BY s.secteur_name, s.region ORDER BY chiffre_affaires DESC"""
    },
    {
        "question": "Quel est le chiffre d'affaires par agence ?",
        "sql": """SELECT ag.agence_name, ag.ville, SUM(f.qty_unite * f.prix_vente) AS chiffre_affaires
FROM FACT_SALES f
JOIN SECTEUR s ON f.secteur_id = s.id_secteur
JOIN AGENCE ag ON s.agence_id = ag.id_agence
GROUP BY ag.agence_name, ag.ville ORDER BY chiffre_affaires DESC"""
    },
    {
        "question": "Quelles sont les 5 villes avec le plus grand volume de ventes ?",
        "sql": """SELECT ag.ville, SUM(f.qty_unite) AS quantite_totale, SUM(f.qty_unite * f.prix_vente) AS chiffre_affaires
FROM FACT_SALES f
JOIN SECTEUR s ON f.secteur_id = s.id_secteur
JOIN AGENCE ag ON s.agence_id = ag.id_agence
GROUP BY ag.ville ORDER BY chiffre_affaires DESC LIMIT 5"""
    },
    {
        "question": "Quel est le chiffre d'affaires par région et par année ?",
        "sql": """SELECT d.annee, s.region, SUM(f.qty_unite * f.prix_vente) AS chiffre_affaires
FROM FACT_SALES f
JOIN SECTEUR s ON f.secteur_id = s.id_secteur
JOIN DATE_DIM d ON f.date_id = d.id_date
GROUP BY d.annee, s.region ORDER BY d.annee, chiffre_affaires DESC"""
    },
    {
        "question": "Quelle région a le taux d'invendus le plus élevé ?",
        "sql": """SELECT s.region,
    SUM(f.qty_invendu) AS total_invendus,
    SUM(f.qty_unite) AS total_vendu,
    ROUND(100.0 * SUM(f.qty_invendu) / NULLIF(SUM(f.qty_unite), 0), 2) AS taux_invendu_pct
FROM FACT_SALES f JOIN SECTEUR s ON f.secteur_id = s.id_secteur
GROUP BY s.region ORDER BY taux_invendu_pct DESC"""
    },

    # BLOC 4 — CLIENTS
    {
        "question": "Quel est le chiffre d'affaires par canal de distribution ?",
        "sql": """SELECT c.canal, SUM(f.qty_unite * f.prix_vente) AS chiffre_affaires,
    COUNT(DISTINCT f.client_id) AS nombre_clients
FROM FACT_SALES f JOIN CLIENT c ON f.client_id = c.id_client
GROUP BY c.canal ORDER BY chiffre_affaires DESC"""
    },
    {
        "question": "Quels sont les 10 clients qui génèrent le plus de chiffre d'affaires ?",
        "sql": """SELECT c.nom_client, c.canal, SUM(f.qty_unite * f.prix_vente) AS chiffre_affaires
FROM FACT_SALES f JOIN CLIENT c ON f.client_id = c.id_client
GROUP BY c.nom_client, c.canal ORDER BY chiffre_affaires DESC LIMIT 10"""
    },
    {
        "question": "Combien de clients distincts ont acheté par canal ?",
        "sql": """SELECT c.canal, COUNT(DISTINCT f.client_id) AS nombre_clients_actifs
FROM FACT_SALES f JOIN CLIENT c ON f.client_id = c.id_client
GROUP BY c.canal ORDER BY nombre_clients_actifs DESC"""
    },
    {
        "question": "Quel est le panier moyen par canal ?",
        "sql": """SELECT c.canal, ROUND(AVG(f.qty_unite * f.prix_vente), 2) AS panier_moyen
FROM FACT_SALES f JOIN CLIENT c ON f.client_id = c.id_client
GROUP BY c.canal ORDER BY panier_moyen DESC"""
    },

    # BLOC 5 — PROMOTIONS ET RETOURS
    {
        "question": "Quelle est la quantité totale vendue en promotion par article ?",
        "sql": """SELECT a.article_name, SUM(f.qty_promo) AS quantite_promo, SUM(f.qty_unite) AS quantite_totale,
    ROUND(100.0 * SUM(f.qty_promo) / NULLIF(SUM(f.qty_unite), 0), 2) AS taux_promo_pct
FROM FACT_SALES f JOIN ARTICLE a ON f.article_id = a.id_article
GROUP BY a.article_name ORDER BY quantite_promo DESC"""
    },
    {
        "question": "Quel est le total des retours par région ?",
        "sql": """SELECT s.region, SUM(f.qty_rendu) AS total_retours, SUM(f.qty_unite) AS total_vendu,
    ROUND(100.0 * SUM(f.qty_rendu) / NULLIF(SUM(f.qty_unite), 0), 2) AS taux_retour_pct
FROM FACT_SALES f JOIN SECTEUR s ON f.secteur_id = s.id_secteur
GROUP BY s.region ORDER BY total_retours DESC"""
    },
    {
        "question": "Quel est le chiffre d'affaires net après déduction des retours par année ?",
        "sql": """SELECT d.annee,
    SUM(f.qty_unite * f.prix_vente) AS ca_brut,
    SUM(f.qty_rendu * f.prix_vente) AS montant_retours,
    SUM((f.qty_unite - f.qty_rendu) * f.prix_vente) AS ca_net
FROM FACT_SALES f JOIN DATE_DIM d ON f.date_id = d.id_date
GROUP BY d.annee ORDER BY d.annee"""
    },
    {
        "question": "Quels articles ont le plus de quantités invendues ?",
        "sql": """SELECT a.article_name, SUM(f.qty_invendu) AS total_invendus
FROM FACT_SALES f JOIN ARTICLE a ON f.article_id = a.id_article
GROUP BY a.article_name ORDER BY total_invendus DESC LIMIT 10"""
    },
    {
        "question": "Quel est le rapport entre ventes promotionnelles et ventes normales par gamme ?",
        "sql": """SELECT g.gamme_name,
    SUM(f.qty_promo) AS ventes_promo,
    SUM(f.qty_unite - f.qty_promo) AS ventes_normales,
    ROUND(100.0 * SUM(f.qty_promo) / NULLIF(SUM(f.qty_unite), 0), 2) AS pct_promo
FROM FACT_SALES f
JOIN ARTICLE a ON f.article_id = a.id_article
JOIN SOUS_FAMILLE sf ON a.sous_famille_id = sf.id_sous_famille
JOIN FAMILLE fa ON sf.famille_id = fa.id_famille
JOIN GAMME g ON fa.gamme_id = g.id_gamme
GROUP BY g.gamme_name ORDER BY pct_promo DESC"""
    },

    # BLOC 6 — ANALYSES CROISÉES AVANCÉES
    {
        "question": "Quel est le chiffre d'affaires par gamme et par année ?",
        "sql": """SELECT d.annee, g.gamme_name, SUM(f.qty_unite * f.prix_vente) AS chiffre_affaires
FROM FACT_SALES f
JOIN DATE_DIM d ON f.date_id = d.id_date
JOIN ARTICLE a ON f.article_id = a.id_article
JOIN SOUS_FAMILLE sf ON a.sous_famille_id = sf.id_sous_famille
JOIN FAMILLE fa ON sf.famille_id = fa.id_famille
JOIN GAMME g ON fa.gamme_id = g.id_gamme
GROUP BY d.annee, g.gamme_name ORDER BY d.annee, chiffre_affaires DESC"""
    },
    {
        "question": "Quel est le chiffre d'affaires par région et par gamme de produits ?",
        "sql": """SELECT s.region, g.gamme_name, SUM(f.qty_unite * f.prix_vente) AS chiffre_affaires
FROM FACT_SALES f
JOIN SECTEUR s ON f.secteur_id = s.id_secteur
JOIN ARTICLE a ON f.article_id = a.id_article
JOIN SOUS_FAMILLE sf ON a.sous_famille_id = sf.id_sous_famille
JOIN FAMILLE fa ON sf.famille_id = fa.id_famille
JOIN GAMME g ON fa.gamme_id = g.id_gamme
GROUP BY s.region, g.gamme_name ORDER BY s.region, chiffre_affaires DESC"""
    },
    {
        "question": "Quelle est l'évolution mensuelle du chiffre d'affaires pour chaque agence ?",
        "sql": """SELECT ag.agence_name, d.annee, d.mois, SUM(f.qty_unite * f.prix_vente) AS chiffre_affaires
FROM FACT_SALES f
JOIN SECTEUR s ON f.secteur_id = s.id_secteur
JOIN AGENCE ag ON s.agence_id = ag.id_agence
JOIN DATE_DIM d ON f.date_id = d.id_date
GROUP BY ag.agence_name, d.annee, d.mois ORDER BY ag.agence_name, d.annee, d.mois"""
    },
    {
        "question": "Quel est le chiffre d'affaires par canal et par gamme ?",
        "sql": """SELECT c.canal, g.gamme_name, SUM(f.qty_unite * f.prix_vente) AS chiffre_affaires
FROM FACT_SALES f
JOIN CLIENT c ON f.client_id = c.id_client
JOIN ARTICLE a ON f.article_id = a.id_article
JOIN SOUS_FAMILLE sf ON a.sous_famille_id = sf.id_sous_famille
JOIN FAMILLE fa ON sf.famille_id = fa.id_famille
JOIN GAMME g ON fa.gamme_id = g.id_gamme
GROUP BY c.canal, g.gamme_name ORDER BY c.canal, chiffre_affaires DESC"""
    },
    {
        "question": "Comparer le chiffre d'affaires du premier semestre vs deuxième semestre par année",
        "sql": """SELECT d.annee,
    SUM(CASE WHEN d.mois <= 6 THEN f.qty_unite * f.prix_vente ELSE 0 END) AS ca_s1,
    SUM(CASE WHEN d.mois >  6 THEN f.qty_unite * f.prix_vente ELSE 0 END) AS ca_s2
FROM FACT_SALES f JOIN DATE_DIM d ON f.date_id = d.id_date
GROUP BY d.annee ORDER BY d.annee"""
    },
    {
        "question": "Quel secteur a la meilleure performance par rapport à son nombre de transactions ?",
        "sql": """SELECT s.secteur_name, s.region,
    COUNT(f.id_fact) AS nombre_transactions,
    SUM(f.qty_unite * f.prix_vente) AS chiffre_affaires,
    ROUND(SUM(f.qty_unite * f.prix_vente) / NULLIF(COUNT(f.id_fact), 0), 2) AS ca_par_transaction
FROM FACT_SALES f JOIN SECTEUR s ON f.secteur_id = s.id_secteur
GROUP BY s.secteur_name, s.region ORDER BY ca_par_transaction DESC"""
    },
    {
        "question": "Quelle est la part de marché de chaque gamme sur le chiffre d'affaires total ?",
        "sql": """SELECT g.gamme_name,
    SUM(f.qty_unite * f.prix_vente) AS ca_gamme,
    ROUND(100.0 * SUM(f.qty_unite * f.prix_vente) /
        SUM(SUM(f.qty_unite * f.prix_vente)) OVER (), 2) AS part_marche_pct
FROM FACT_SALES f
JOIN ARTICLE a ON f.article_id = a.id_article
JOIN SOUS_FAMILLE sf ON a.sous_famille_id = sf.id_sous_famille
JOIN FAMILLE fa ON sf.famille_id = fa.id_famille
JOIN GAMME g ON fa.gamme_id = g.id_gamme
GROUP BY g.gamme_name ORDER BY ca_gamme DESC"""
    },
    {
        "question": "Quels sont les articles les plus vendus dans chaque région ?",
        "sql": """SELECT s.region, a.article_name, SUM(f.qty_unite) AS quantite_vendue
FROM FACT_SALES f
JOIN SECTEUR s ON f.secteur_id = s.id_secteur
JOIN ARTICLE a ON f.article_id = a.id_article
GROUP BY s.region, a.article_name
QUALIFY ROW_NUMBER() OVER (PARTITION BY s.region ORDER BY SUM(f.qty_unite) DESC) = 1
ORDER BY s.region"""
    },
]
