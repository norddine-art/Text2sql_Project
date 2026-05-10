import sqlite3
import pandas as pd
import os

DB_PATH = "backend/data.db"
EXPORT_DIR = "data_exports"

if not os.path.exists(EXPORT_DIR):
    os.makedirs(EXPORT_DIR)

def export_all():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    
    print(f"Exporting {len(tables)} tables from {DB_PATH} to {EXPORT_DIR}/...")
    
    for table in tables:
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        csv_path = os.path.join(EXPORT_DIR, f"{table}.csv")
        df.to_csv(csv_path, index=False)
        print(f"  - {table} -> {csv_path} ({len(df)} rows)")
    
    conn.close()
    print("\nExport complete! You can now open the .csv files in the 'data_exports' folder.")

if __name__ == "__main__":
    export_all()
