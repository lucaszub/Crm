from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import client
from app.database import engine, Base

app = FastAPI()

# Configuration des origines autorisées pour CORS
origins = [
    "http://localhost:5173",
    "https://proud-coast-05dac3f03.6.azurestaticapps.net",
    "https://witty-river-06f071903.6.azurestaticapps.net"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Include the client router
app.include_router(client.router)