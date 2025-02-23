import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import pyodbc
import os

# Configuration du logging
logging.basicConfig(level=logging.INFO)

# Initialisation de l'application FastAPI
app = FastAPI()

# Configuration des CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URL de votre Azure Key Vault (stocké dans une variable d'environnement)
key_vault_name = os.getenv("AZURE_KEY_VAULT_NAME", "secret-crm")
KVUri = f"https://{key_vault_name}.vault.azure.net"

def get_secret(secret_name: str) -> str:
    """Récupère un secret depuis Azure Key Vault en utilisant DefaultAzureCredential."""
    try:
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=KVUri, credential=credential)
        secret = client.get_secret(secret_name)
        return secret.value
    except Exception as e:
        logging.error(f"Erreur lors de la récupération du secret {secret_name}: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/db-credentials")
async def get_db_credentials():
    """Endpoint pour récupérer les identifiants de la base de données."""
    try:
        server = get_secret("server-db")
        database = get_secret("database")
        username = get_secret("username")
        password = get_secret("password-db")
        return {
            "server": server,
            "database": database,
            "username": username,
            "password": password
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des identifiants: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@app.get("/test-connection")
async def test_connection():
    """Endpoint pour tester la connexion à la base de données."""
    try:
        server = get_secret("server-db")
        database = get_secret("database")
        username = get_secret("username")
        password = get_secret("password-db")
        driver = '{ODBC Driver 18 for SQL Server}'
        connection_string = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}"
        with pyodbc.connect(connection_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM dbo.Clients")
                result = cursor.fetchone()
                return {"message": "Connexion réussie", "result": result[0]}
    except pyodbc.Error as e:
        logging.error(f"Erreur de connexion à la base de données: {e}")
        raise HTTPException(status_code=500, detail="Erreur de connexion à la base de données")
    except Exception as e:
        logging.error(f"Erreur inattendue: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")
