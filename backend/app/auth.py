# app/auth.py
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Utilisateur
from app.schemas import ConnexionRequest

router = APIRouter()

# JWT Config
SECRET_KEY = "ma-cle-ultra-secrete"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
security = HTTPBearer()


# --- Fonction pour activer le CORS dans l'app FastAPI ---
def configurer_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # exemple: ["http://localhost:5173"]
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# --- DB ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- JWT utils ---
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# --- Auth ---
@router.post("/connexion")
def connexion(data: ConnexionRequest, db: Session = Depends(get_db)):
    utilisateur = db.query(Utilisateur).filter_by(nom=data.nom).first()

    if not utilisateur or utilisateur.mot_de_passe != data.mot_de_passe:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom ou mot de passe invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = {
        "nom": utilisateur.nom,
        "role": utilisateur.role.value,
        "id": utilisateur.id,
    }
    token = create_access_token(token_data)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Connexion réussie",
            "nom": utilisateur.nom,
            "role": utilisateur.role.value,
            "token": token,
        },
    )


# --- Protéger des routes ---
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload
