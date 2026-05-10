"""
Tests unitaires de la génération SQL.
Lance : python tests/test_generation.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
from vanna_setup import vn

TEST_CASES = [
    {
        "question": "CA par région",
        "expected_tables": ["FACT_SALES", "SECTEUR"],
        "expected_keywords": ["region", "SUM"],
    },
    {
        "question": "Top 10 articles les plus vendus",
        "expected_tables": ["FACT_SALES", "ARTICLE"],
        "expected_keywords": ["article_name", "LIMIT"],
    },
    {
        "question": "Chiffre d'affaires par gamme",
        "expected_tables": ["GAMME", "FAMILLE", "SOUS_FAMILLE"],
        "expected_keywords": ["gamme_name"],
    },
    {
        "question": "Retours par région",
        "expected_tables": ["FACT_SALES", "SECTEUR"],
        "expected_keywords": ["qty_rendu", "region"],
    },
    {
        "question": "CA par type de client",
        "expected_tables": ["CLIENT"],
        "expected_keywords": ["client_type"],
    },
]

def run_tests():
    print("🧪 Lancement des tests...\n")
    passed = 0
    for i, tc in enumerate(TEST_CASES):
        try:
            sql = vn.generate_sql(tc["question"])
            sql_upper = sql.upper()
            errors = []
            for table in tc["expected_tables"]:
                if table.upper() not in sql_upper:
                    errors.append(f"table manquante: {table}")
            for kw in tc["expected_keywords"]:
                if kw.upper() not in sql_upper:
                    errors.append(f"mot-clé manquant: {kw}")
            if not errors:
                print(f"✅ Test {i+1}: {tc['question']}")
                passed += 1
            else:
                print(f"⚠  Test {i+1}: {tc['question']}")
                for e in errors:
                    print(f"     → {e}")
        except Exception as e:
            print(f"❌ Test {i+1}: {tc['question']} — ERREUR: {e}")
    print(f"\nRésultat : {passed}/{len(TEST_CASES)} tests réussis")

if __name__ == "__main__":
    run_tests()
