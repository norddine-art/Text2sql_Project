"""
Script d'entraînement Vanna — à exécuter une seule fois.
Lance : python backend/run_training.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from vanna_setup import vn
from training_data.glossaire import DOCUMENTATION_METIER
from training_data.examples import TRAINING_EXAMPLES

def step1_train_ddl():
    print("\n📋 ÉTAPE 1 — Entraînement sur le schéma DDL...")
    ddl_path = os.path.join(os.path.dirname(__file__), "training_data/ddl.sql")
    with open(ddl_path, "r", encoding="utf-8") as f:
        ddl_content = f.read()
    tables = [t.strip() for t in ddl_content.split(";") if "CREATE TABLE" in t]
    for table_ddl in tables:
        table_name = table_ddl.split("TABLE")[1].split("(")[0].strip()
        vn.train(ddl=table_ddl + ";")
        print(f"   ✅ {table_name}")
    print(f"   → {len(tables)} tables entraînées")

def step2_train_docs():
    print("\n📚 ÉTAPE 2 — Entraînement sur la documentation métier...")
    for i, doc in enumerate(DOCUMENTATION_METIER):
        vn.train(documentation=doc)
        print(f"   ✅ Doc {i+1}/{len(DOCUMENTATION_METIER)}")

def step3_train_examples():
    print(f"\n💡 ÉTAPE 3 — Entraînement sur les {len(TRAINING_EXAMPLES)} exemples Q→SQL...")
    for i, ex in enumerate(TRAINING_EXAMPLES):
        vn.train(question=ex["question"], sql=ex["sql"])
        print(f"   ✅ [{i+1:02d}/{len(TRAINING_EXAMPLES)}] {ex['question'][:65]}...")

def step4_verify():
    print("\n🔍 ÉTAPE 4 — Vérification du training data...")
    try:
        training_data = vn.get_training_data()
        print(f"   ✅ Total éléments entraînés : {len(training_data)}")
    except Exception as e:
        print(f"   ⚠ Impossible de récupérer le training data : {e}")

def step5_test():
    print("\n🧪 ÉTAPE 5 — Test de génération SQL...")
    questions_test = [
        "Quel est le chiffre d'affaires total par année ?",
        "Quels sont les 10 articles les plus vendus ?",
        "Quel est le chiffre d'affaires par région ?",
    ]
    all_ok = True
    for q in questions_test:
        try:
            sql = vn.generate_sql(q)
            has_select = "SELECT" in sql.upper()
            has_from = "FROM" in sql.upper()
            status = "✅" if (has_select and has_from) else "⚠"
            if not (has_select and has_from):
                all_ok = False
            print(f"   {status} Q: {q[:50]}...")
            print(f"        SQL: {sql[:80].strip()}...")
        except Exception as e:
            print(f"   ❌ Erreur sur : {q}")
            print(f"        {e}")
            all_ok = False
    return all_ok

if __name__ == "__main__":
    print("🚀 Démarrage de l'entraînement Vanna...")
    step1_train_ddl()
    step2_train_docs()
    step3_train_examples()
    step4_verify()
    ok = step5_test()
    if ok:
        print("\n🎉 Entraînement terminé avec succès ! Lance maintenant : streamlit run frontend/app.py")
    else:
        print("\n⚠ Entraînement terminé avec des avertissements. Vérifie ta clé DEEPSEEK_API_KEY dans le .env et assure-toi d'avoir des crédits.")
