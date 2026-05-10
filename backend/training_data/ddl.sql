-- ============================================================
-- SCHÉMA COPAG MAROC — DDL uniquement
-- Table CLIENT mise à jour avec canal, nom_client, code_client
-- ============================================================

PRAGMA foreign_keys = ON;

-- ============================================================
-- TABLE CLIENT (mise à jour)
-- ============================================================
CREATE TABLE IF NOT EXISTS CLIENT (
    id_client   INTEGER PRIMARY KEY AUTOINCREMENT,
    canal       TEXT NOT NULL,
    nom_client  TEXT NOT NULL,
    code_client TEXT NOT NULL
);

-- ============================================================
-- TABLE AGENCE
-- ============================================================
CREATE TABLE IF NOT EXISTS AGENCE (
    id_agence   INTEGER PRIMARY KEY AUTOINCREMENT,
    agence_name TEXT NOT NULL,
    ville       TEXT NOT NULL
);

-- ============================================================
-- TABLE SECTEUR
-- ============================================================
CREATE TABLE IF NOT EXISTS SECTEUR (
    id_secteur   INTEGER PRIMARY KEY AUTOINCREMENT,
    secteur_name TEXT NOT NULL,
    region       TEXT NOT NULL,
    agence_id    INTEGER REFERENCES AGENCE(id_agence)
);

-- ============================================================
-- TABLE GAMME
-- ============================================================
CREATE TABLE IF NOT EXISTS GAMME (
    id_gamme   INTEGER PRIMARY KEY AUTOINCREMENT,
    gamme_name TEXT NOT NULL
);

-- ============================================================
-- TABLE FAMILLE
-- ============================================================
CREATE TABLE IF NOT EXISTS FAMILLE (
    id_famille   INTEGER PRIMARY KEY AUTOINCREMENT,
    famille_name TEXT NOT NULL,
    gamme_id     INTEGER REFERENCES GAMME(id_gamme)
);

-- ============================================================
-- TABLE SOUS_FAMILLE
-- ============================================================
CREATE TABLE IF NOT EXISTS SOUS_FAMILLE (
    id_sous_famille   INTEGER PRIMARY KEY AUTOINCREMENT,
    sous_famille_name TEXT NOT NULL,
    famille_id        INTEGER REFERENCES FAMILLE(id_famille)
);

-- ============================================================
-- TABLE ARTICLE
-- ============================================================
CREATE TABLE IF NOT EXISTS ARTICLE (
    id_article       INTEGER PRIMARY KEY AUTOINCREMENT,
    article_name     TEXT NOT NULL,
    poids            REAL,
    tva              REAL,
    prix_vente_ref   REAL NOT NULL,
    sous_famille_id  INTEGER REFERENCES SOUS_FAMILLE(id_sous_famille)
);

-- ============================================================
-- TABLE DATE_DIM (Dimension Temps)
-- ============================================================
CREATE TABLE IF NOT EXISTS DATE_DIM (
    id_date INTEGER PRIMARY KEY AUTOINCREMENT,
    date    TEXT NOT NULL,
    jour    INTEGER,
    mois    INTEGER,
    annee   INTEGER
);

-- ============================================================
-- TABLE FACT_SALES (Table de faits)
-- ============================================================
CREATE TABLE IF NOT EXISTS FACT_SALES (
    id_fact     INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id   INTEGER REFERENCES CLIENT(id_client),
    secteur_id  INTEGER REFERENCES SECTEUR(id_secteur),
    article_id  INTEGER REFERENCES ARTICLE(id_article),
    date_id     INTEGER REFERENCES DATE_DIM(id_date),
    qty_unite   INTEGER,
    prix_vente  REAL,
    qty_rendu   INTEGER DEFAULT 0,
    qty_invendu INTEGER DEFAULT 0,
    qty_promo   INTEGER DEFAULT 0
);
