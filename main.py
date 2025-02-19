import os
import pyodbc
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import logging
from fastapi import FastAPI, HTTPException

# Initialisation de la connexion à Azure Key Vault
key_vault_name = "secret-crm"
KVUri = f"https://{key_vault_name}.vault.azure.net"

# Configurer FastAPI
app = FastAPI()

# Configurer le logging
logging.basicConfig(level=logging.DEBUG)

# Route de test pour vérifier que l'application est accessible
@app.get("/")
async def read_root():
    return {"message": "Hello World"}

# Récupérer les secrets stockés dans Azure Key Vault
def get_secret_from_keyvault(secret_name: str):
    try:
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=KVUri, credential=credential)
        secret = client.get_secret(secret_name).value
        logging.debug(f"Secret récupéré pour {secret_name}: {secret}")
        return secret
    except Exception as e:
        logging.error(f"Erreur lors de la récupération du secret {secret_name} depuis Azure Key Vault : {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de récupération du secret {secret_name}")

# Récupération des secrets nécessaires pour la connexion à la base de données
# server = get_secret_from_keyvault("server-db")
# database = get_secret_from_keyvault("database")
# username = get_secret_from_keyvault("username")
# password = get_secret_from_keyvault("password-db")

# Définir le driver ODBC pour SQL Server
# driver = "{ODBC Driver 18 for SQL Server}"

# Fonction de connexion à la base de données SQL Server
# def get_db_connection():
#     try:
#         conn = pyodbc.connect(
#             f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}"
#         )
#         logging.debug("Connexion à la base de données réussie to SQL Server")
#         return conn
#     except pyodbc.Error as e:
#         logging.error(f"Erreur de connexion à la base de données : {e}")
#         raise HTTPException(status_code=500, detail="Erreur de connexion à la base de données")

@app.get("testkeyvault")
def test_keyvault():
    try:
        server = get_secret_from_keyvault("server-db")
        database = get_secret_from_keyvault("database")
        username = get_secret_from_keyvault("username") 
        password = get_secret_from_keyvault("password-db")
        return {
            "server": server,
            "database": database,
            "username": username,
            "password": password
        }
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des secrets : {e}")
# Route principale pour récupérer les données des clients
# @app.get("/clients")
# async def get_clients():
#     try:
#         with get_db_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM dbo.Clients")
#             rows = cursor.fetchall()
#             clients = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
#             return {"clients": clients}
#     except Exception as e:
#         logging.error(f"Erreur lors de la récupération des clients : {e}")
#         raise HTTPException(status_code=500, detail="Erreur lors de la récupération des clients")
