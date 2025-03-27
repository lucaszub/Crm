# filepath: /c:/Projet/Backend-crm/app/schemas/client.py
from pydantic import BaseModel
from datetime import date

class ClientBase(BaseModel):
    name: str
    entreprise: str
    role: str
    status: str
    email: str
    numero: str
    avatarUrl: str
    interaction: str
    note: str

class ClientCreate(ClientBase):
    pass  # Supprimer l'ID ici

class ClientUpdate(ClientBase):
    pass

class Client(ClientBase):
    id: str

    class Config:
        orm_mode = True