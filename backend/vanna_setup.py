import os
from openai import OpenAI
from dotenv import load_dotenv
from vanna.legacy.openai.openai_chat import OpenAI_Chat
from vanna.legacy.chromadb.chromadb_vector import ChromaDB_VectorStore

load_dotenv()

# Client API (Compatible OpenAI pour Groq)
custom_client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)

class MonVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, client=None, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, client=client, config=config)

vn = MonVanna(
    client=custom_client,
    config={
        'model': os.getenv("MODEL"),
        'path': './chroma_db'
    }
)

# Connexion à la base de données SQLite pour l'exécution
db_path = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "data.db"))
vn.connect_to_sqlite(db_path)

def get_vanna():
    return vn
