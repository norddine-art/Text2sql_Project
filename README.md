# 🔍 COPAG SQL Insight Assistant

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Vanna.ai](https://img.shields.io/badge/Vanna.ai-FFD700?style=for-the-badge&logo=ai&logoColor=black)
![Groq](https://img.shields.io/badge/LLM-Groq-orange?style=for-the-badge)

**COPAG SQL Insight Assistant** est une application d'intelligence d'affaires (BI) de nouvelle génération conçue pour transformer la manière dont les utilisateurs interagissent avec les données de COPAG. En utilisant le langage naturel, n'importe quel utilisateur peut poser des questions complexes sur les ventes, les stocks ou les opérations et obtenir instantanément des résultats SQL, des analyses approfondies et des visualisations interactives.

---

## 🌟 Idée Générale

L'objectif principal est de démocratiser l'accès aux données au sein de COPAG. Au lieu d'attendre des rapports manuels ou de maîtriser le langage SQL, les décideurs peuvent "discuter" directement avec la base de données. L'assistant comprend l'intention de l'utilisateur, génère la requête SQL appropriée, l'exécute, et fournit une interprétation métier des résultats.

---

## 🏗️ Architecture du Projet

Le projet repose sur une architecture moderne alliant **RAG (Retrieval Augmented Generation)** pour le SQL et une interface utilisateur haut de gamme.

### 1. Backend (Le Cerveau)
*   **Vanna.ai** : Framework central utilisé pour le Text-to-SQL. Il utilise une base de données vectorielle pour stocker la connaissance du domaine.
*   **ChromaDB** : Base de données vectorielle locale stockant les schémas DDL, les glossaires métiers et des exemples de requêtes SQL.
*   **Groq (LLM)** : Utilisation de modèles de pointe (Llama 3) via Groq pour une génération de code SQL ultra-rapide et précise.
*   **SQLite** : Base de données relationnelle pour l'exécution des requêtes (remplaçable par SQL Server/PostgreSQL en production).

### 2. Frontend (L'Expérience Utilisateur)
*   **Streamlit** : Framework de base pour l'interface web.
*   **Tailwind CSS** : Injecté dynamiquement pour un design premium, moderne et réactif.
*   **Plotly** : Utilisé pour générer des graphiques interactifs et dynamiques sur la page de visualisation.

---

## 🚀 Fonctionnalités Clés

*   **🔍 Requêtes en Langage Naturel** : Posez des questions comme *"Quels sont les 10 meilleurs clients par chiffre d'affaires en 2023 ?"*.
*   **💡 AI Insight** : Une analyse textuelle générée par l'IA accompagne chaque résultat pour expliquer les tendances et les points clés.
*   **📊 Visualisation Automatique** : Détection intelligente du type de graphique idéal (Barres, Donut, Lignes, Classement) selon les données extraites.
*   **🎛️ Filtres Globaux Persistants** : Un panneau latéral permettant d'affiner les résultats par Agence, Secteur, Gamme, Famille, etc., qui restent actifs à travers toute l'application.
*   **💬 Historique des Conversations** : Gardez une trace de vos analyses précédentes pour une comparaison rapide.
*   **💻 Transparence SQL** : Accès au code SQL généré pour vérification par les experts techniques.

---

## 📁 Structure des Dossiers

```text
.
├── backend/
│   ├── training_data/      # Connaissance métier (DDL, SQL, Glossaire)
│   ├── vanna_setup.py      # Configuration de Vanna et du LLM
│   └── run_training.py     # Script pour entraîner l'IA sur le domaine COPAG
├── frontend/
│   ├── app.py              # Interface principale (Chat & Résultats)
│   ├── pages/              # Pages secondaires (Visualisation)
│   ├── filter_utils.py     # Logique des filtres globaux
│   └── logos/              # Actifs visuels de la marque
├── chroma_db/              # Base vectorielle persistante
├── requirements.txt        # Dépendances du projet
└── run_app.sh              # Script de lancement rapide
```

---

## 🛠️ Installation et Lancement

### Prérequis
*   Python 3.10+
*   Une clé API Groq (ou OpenAI compatible)

### Étapes
1.  **Cloner le dépôt**
2.  **Installer les dépendances** :
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configurer les variables d'environnement** (`.env`) :
    ```env
    API_KEY=votre_cle_groq
    BASE_URL=https://api.groq.com/openai/v1
    MODEL=llama-3.3-70b-versatile
    DB_PATH=backend/data.db
    ```
4.  **Lancer l'application** :
    ```bash
    streamlit run frontend/app.py
    ```

---

## 🛡️ Sécurité et Précision
L'assistant utilise une approche de **"Self-Correction"** et de **"Context Augmentation"**. Les métadonnées de la base de données sont soigneusement préparées dans `backend/training_data/` pour garantir que l'IA respecte les règles métiers spécifiques à COPAG (ex: calcul du CA, regroupement par gamme).

---

© 2024 COPAG — Développé pour l'excellence opérationnelle.
