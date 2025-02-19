import os
import pyodbc
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Initialisation de la connexion à Azure Key Vault
key_vault_name = "secret-crm"
KVUri = f"https://{key_vault_name}.vault.azure.net"

# Configurer FastAPI
app = FastAPI()

# Configurer CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplace "*" par les origines que tu veux autoriser
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/testkeyvault")  # Ajout du slash ici
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
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des secrets")
