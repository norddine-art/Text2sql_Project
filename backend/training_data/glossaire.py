DOCUMENTATION_METIER = [
    "FACT_SALES est la table centrale. Chaque ligne est une transaction de vente d'un article à un client via un secteur.",
    "qty_unite = quantité vendue. qty_rendu = retours client. qty_invendu = stock non vendu. qty_promo = quantité en promotion. Le CA net = (qty_unite - qty_rendu) * prix_vente.",
    "Hiérarchie produit : GAMME → FAMILLE → SOUS_FAMILLE → ARTICLE. Pour analyser par gamme, joindre ARTICLE, SOUS_FAMILLE, FAMILLE, GAMME.",
    "Hiérarchie géographique : AGENCE → SECTEUR. Un secteur appartient à une agence, une agence est dans une ville.",
    "DATE_DIM contient : date, jour, mois, annee. Filtrer par année avec DATE_DIM.annee, par mois avec DATE_DIM.mois (1=Janvier, 12=Décembre).",
    "CLIENT.canal : représente le canal de distribution du client (ex: GMS, Grossiste, Détaillant, CHR, Export). Remplace l'ancien concept de 'type de client'.",
    "CLIENT.nom_client : le nom ou la raison sociale de l'entreprise/client.",
    "CLIENT.code_client : l'identifiant métier unique du client (ex: CLI-0001).",
    "ARTICLE.prix_vente_ref : le prix de vente de référence par défaut de l'article avant toute négociation ou remise.",
    "FACT_SALES.prix_vente est en dirhams marocains (DH/MAD). ARTICLE.tva est le taux de TVA en pourcentage (ex: 0.20 = 20%).",
]
