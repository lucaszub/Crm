from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Informations de connexion
server = "sqlserver-lucas.database.windows.net"
database = "sqldb-lucas"
username = "lucaszub"
password = "Medard44?"
driver = "ODBC+Driver+18+for+SQL+Server"

# Formatage correct de l'URL de connexion
SQLALCHEMY_DATABASE_URL = (
    f"mssql+pyodbc://{username}:{password}@{server}:1433/{database}"
    f"?driver={driver}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()