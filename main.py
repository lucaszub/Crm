import pyodbc
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

# Initialisation de la connexion à Azure Key Vault
key_vault_name = "secret-crm"
KVUri = f"https://{key_vault_name}.vault.azure.net"

try:
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KVUri, credential=credential)

    # Récupération des secrets stockés
    server = client.get_secret("server-db").value
    database = client.get_secret("database").value
    username = client.get_secret("username").value
    # password = client.get_secret("password").value
    password = client.get_secret("password-db").value

    if not all([server, database, username, password]):
        raise ValueError("Un ou plusieurs secrets sont vides ou non récupérés.")

except Exception as e:
    print(f"❌ Erreur lors de la récupération des secrets Azure Key Vault : {e}")
    raise

# Vérification des valeurs récupérées (sans afficher le mot de passe)
print(f"✅ Connexion à SQL Server avec :")
print(f"- Server: {server}")
print(f"- Database: {database}")
print(f"- Username: {username}")

# Définition du driver ODBC
driver = "{ODBC Driver 18 for SQL Server}"  # Assure-toi qu'il est bien installé

# Fonction de connexion à la base de données SQL Server
def get_db_connection():
    try:
        conn = pyodbc.connect(
            f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}"
        )
        return conn
    except pyodbc.Error as e:
        print(f"❌ Erreur de connexion à la base de données : {e}")
        raise HTTPException(status_code=500, detail="Impossible de se connecter à la base de données")

# Création de l'application FastAPI
app = FastAPI()

# Modèle Pydantic pour la réponse des clients
class Client(BaseModel):
    ClientID: int
    FirstName: str
    LastName: str
    Email: str
    Phone: str
    Address: str

# Route pour récupérer tous les clients
@app.get("/clients", response_model=List[Client])
async def get_clients():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ClientID, FirstName, LastName, Email, Phone, Address FROM Clients")
            rows = cursor.fetchall()

            # Transformation des résultats en liste d'objets Client
            clients = [
                Client(
                    ClientID=row.ClientID,
                    FirstName=row.FirstName,
                    LastName=row.LastName,
                    Email=row.Email,
                    Phone=row.Phone,
                    Address=row.Address
                ) for row in rows
            ]

        return clients

    except pyodbc.Error as e:
        print(f"❌ Erreur lors de la récupération des clients : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des clients")

# Lancement du serveur avec Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
