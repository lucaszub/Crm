from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas
from app.database import get_db

router = APIRouter()

@router.get("/clients", response_model=List[schemas.Client])
def read_clients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    clients = crud.get_clients(db, skip=skip, limit=limit)
    return clients

@router.get("/clients/{client_id}", response_model=schemas.Client)
def read_client(client_id: str, db: Session = Depends(get_db)):
    client = crud.get_client(db, client_id=client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.post("/clients", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    return crud.create_client(db=db, client=client)

@router.put("/clients/{client_id}", response_model=schemas.Client)
def update_client(client_id: str, client: schemas.ClientUpdate, db: Session = Depends(get_db)):
    return crud.update_client(db=db, client_id=client_id, client=client)

@router.delete("/clients/{client_id}", response_model=schemas.Client)
def delete_client(client_id: str, db: Session = Depends(get_db)):
    return crud.delete_client(db=db, client_id=client_id)