import logging
import os

import redis
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.auth import router as auth_router
from app.database import engine
from app.employe import router as employe_router
from app.gestionnaire import router as gestionnaire_router
from app.models import Base
from app.responsable import router as responsable_router

# Configuration Redis
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

# Création des tables si nécessaire
Base.metadata.create_all(bind=engine)

# Configuration du logging structuré
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI()

# Ajout du middleware Prometheus
Instrumentator().instrument(app).expose(app)

# Logging de chaque requête HTTP
@app.middleware("http")  # ← correction ici, il faut utiliser un décorateur
async def log_requests(request: Request, call_next):
    logger.info(f"Requête: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Réponse: {response.status_code}")
    return response

# Middleware CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:9090",
    "http://localhost:5173",
    "http://backend1:8000",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routers modulaires
app.include_router(auth_router, prefix="/api/v1", tags=["Authentification"])
app.include_router(employe_router, prefix="/api/v1/employe", tags=["Employe"])
app.include_router(responsable_router, prefix="/api/v1/responsable", tags=["Responsable"])
app.include_router(gestionnaire_router, prefix="/api/v1/gestionnaire", tags=["Gestionnaire"])
