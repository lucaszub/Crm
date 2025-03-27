# filepath: /c:/Projet/Backend-crm/app/crud/client.py
from sqlalchemy.orm import Session
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate
import uuid

def get_client(db: Session, client_id: str):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client:
        client.id = str(client.id)
    return client

def get_clients(db: Session, skip: int = 0, limit: int = 10):
    clients = db.query(Client).order_by(Client.id).offset(skip).limit(limit).all()
    for client in clients:
        client.id = str(client.id)
    return clients

def create_client(db: Session, client: ClientCreate):
    db_client = Client(id=uuid.uuid4(), **client.dict())  # Générer un UUID pour l'ID
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    db_client.id = str(db_client.id)
    return db_client

def update_client(db: Session, client_id: str, client: ClientUpdate):
    db_client = get_client(db, client_id)
    if db_client:
        for key, value in client.dict().items():
            setattr(db_client, key, value)
        db.commit()
        db.refresh(db_client)
        db_client.id = str(db_client.id)
    return db_client

def delete_client(db: Session, client_id: str):
    db_client = get_client(db, client_id)
    if db_client:
        db.delete(db_client)
        db.commit()
        db_client.id = str(db_client.id)
    return db_client