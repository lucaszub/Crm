# filepath: /c:/Projet/Backend-crm/app/models/client.py
from sqlalchemy import Column, String, Date
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
import uuid
from app.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, index=True)
    entreprise = Column(String)
    role = Column(String)
    status = Column(String)
    email = Column(String, unique=True, index=True)
    numero = Column(String)
    avatarUrl = Column(String)
    interaction = Column(String)
    note = Column(String)
    