
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.router import router as api_router
from .database import engine
from .models import database

database.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Recally API",
    description="API for Recally, a cross-platform app for capturing and organizing information.",
    version="0.1.0",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Recally API"}
