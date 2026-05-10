import sqlite3
import os
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('fr_FR')

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")
DDL_PATH = os.path.join(os.path.dirname(__file__), "training_data/ddl.sql")

def populate():
    # Connect to SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Read and execute DDL
    print(f"Creating schema from {DDL_PATH}...")
    with open(DDL_PATH, 'r') as f:
        ddl = f.read()
    
    # Split by semicolon and execute each statement
    for statement in ddl.split(';'):
        if statement.strip():
            cursor.execute(statement)
    
    print("Populating tables...")

    # 1. CLIENT (id_client, canal, nom_client, code_client)
    print("  - CLIENT...")
    canaux = ['GMS', 'Détaillant', 'Grossiste', 'CHR', 'Export']
    clients = []
    for i in range(1, 1001):
        clients.append((
            i, 
            random.choice(canaux), 
            f"Client {fake.company()}", 
            f"CLI-{i:04d}"
        ))
    cursor.executemany("INSERT INTO CLIENT (id_client, canal, nom_client, code_client) VALUES (?, ?, ?, ?)", clients)

    # 2. AGENCE (id_agence, agence_name, ville)
    print("  - AGENCE...")
    agences = []
    villes = [fake.city() for _ in range(20)]
    for i in range(1, 21):
        agences.append((i, f"Agence {fake.company()}", villes[i-1]))
    cursor.executemany("INSERT INTO AGENCE (id_agence, agence_name, ville) VALUES (?, ?, ?)", agences)

    # 3. SECTEUR (id_secteur, secteur_name, region, agence_id)
    print("  - SECTEUR...")
    secteurs = []
    regions = ['Nord', 'Sud', 'Est', 'Ouest', 'Centre']
    for i in range(1, 101):
        secteurs.append((i, f"Secteur {fake.word().capitalize()}", random.choice(regions), random.randint(1, 20)))
    cursor.executemany("INSERT INTO SECTEUR (id_secteur, secteur_name, region, agence_id) VALUES (?, ?, ?, ?)", secteurs)

    # 4. GAMME (id_gamme, gamme_name)
    print("  - GAMME...")
    gammes = []
    gamme_names = ['Laitage', 'Fromage', 'Jus', 'Viande', 'Charcuterie', 'Beurre', 'Dessert', 'Surgelé', 'Épicerie', 'Boisson']
    for i in range(1, 11):
        gammes.append((i, gamme_names[i-1]))
    cursor.executemany("INSERT INTO GAMME (id_gamme, gamme_name) VALUES (?, ?)", gammes)

    # 5. FAMILLE (id_famille, famille_name, gamme_id)
    print("  - FAMILLE...")
    familles = []
    for i in range(1, 51):
        familles.append((i, f"Famille {fake.word().capitalize()}", random.randint(1, 10)))
    cursor.executemany("INSERT INTO FAMILLE (id_famille, famille_name, gamme_id) VALUES (?, ?, ?)", familles)

    # 6. SOUS_FAMILLE (id_sous_famille, sous_famille_name, famille_id)
    print("  - SOUS_FAMILLE...")
    sous_familles = []
    for i in range(1, 201):
        sous_familles.append((i, f"Sous-Famille {fake.word().capitalize()}", random.randint(1, 50)))
    cursor.executemany("INSERT INTO SOUS_FAMILLE (id_sous_famille, sous_famille_name, famille_id) VALUES (?, ?, ?)", sous_familles)

    # 7. ARTICLE (id_article, article_name, poids, tva, prix_vente_ref, sous_famille_id)
    print("  - ARTICLE...")
    articles = []
    for i in range(1, 1001):
        articles.append((
            i, 
            f"Article {fake.catch_phrase()}", 
            round(random.uniform(0.1, 5.0), 2), 
            random.choice([0.07, 0.14, 0.20]), 
            round(random.uniform(10.0, 500.0), 2), # prix_vente_ref
            random.randint(1, 200)
        ))
    cursor.executemany("INSERT INTO ARTICLE (id_article, article_name, poids, tva, prix_vente_ref, sous_famille_id) VALUES (?, ?, ?, ?, ?, ?)", articles)

    # 8. DATE_DIM (id_date, date, jour, mois, annee)
    print("  - DATE_DIM...")
    dates = []
    start_date = datetime(2023, 1, 1)
    for i in range(1, 731): # 2 years
        current_date = start_date + timedelta(days=i-1)
        dates.append((i, current_date.strftime('%Y-%m-%d'), current_date.day, current_date.month, current_date.year))
    cursor.executemany("INSERT INTO DATE_DIM (id_date, date, jour, mois, annee) VALUES (?, ?, ?, ?, ?)", dates)

    # 9. FACT_SALES (id_fact, client_id, secteur_id, article_id, date_id, qty_unite, prix_vente, qty_rendu, qty_invendu, qty_promo)
    print("  - FACT_SALES...")
    fact_sales = []
    for i in range(1, 5001):
        qty = random.randint(1, 50)
        fact_sales.append((
            i, 
            random.randint(1, 1000), # client
            random.randint(1, 100),  # secteur
            random.randint(1, 1000), # article
            random.randint(1, 730),  # date
            qty, 
            round(random.uniform(10.0, 500.0), 2), # prix_vente
            random.randint(0, max(0, qty // 10)), # qty_rendu
            random.randint(0, max(0, qty // 5)),  # qty_invendu
            random.randint(0, qty // 2) if random.random() > 0.8 else 0 # qty_promo
        ))
    cursor.executemany("INSERT INTO FACT_SALES (id_fact, client_id, secteur_id, article_id, date_id, qty_unite, prix_vente, qty_rendu, qty_invendu, qty_promo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", fact_sales)

    conn.commit()
    conn.close()
    print(f"Database populated successfully at {DB_PATH}")

if __name__ == "__main__":
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    populate()
