# tests/test_auth.py
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

@patch("app.auth.get_db")
def test_connexion_valide(mock_get_db):
    # Création d'un mock utilisateur avec les bons attributs
    mock_user = MagicMock()
    mock_user.nom = "Bob"
    mock_user.mot_de_passe = "1234"
    mock_user.role.value = "employe"
    mock_user.id = 1

    # Création d'une session mockée avec la méthode chainée query().filter_by().first()
    mock_session = MagicMock()
    mock_query = mock_session.query.return_value
    mock_filter = mock_query.filter_by.return_value
    mock_filter.first.return_value = mock_user

    # get_db() doit renvoyer un générateur, donc on fait un tuple ici
    mock_get_db.return_value = iter([mock_session])


    response = client.post("/api/v1/connexion", json={"nom": "Bob", "mot_de_passe": "1234"})
    assert response.status_code == 200
    assert "token" in response.json()


@patch("app.auth.get_db")
def test_connexion_invalide(mock_get_db):
    mock_session = MagicMock()
    mock_query = mock_session.query.return_value
    mock_filter = mock_query.filter_by.return_value
    mock_filter.first.return_value = None  # Pas d'utilisateur trouvé

    mock_get_db.return_value = iter([mock_session])


    response = client.post("/api/v1/connexion", json={"nom": "fake", "mot_de_passe": "wrong"})
    assert response.status_code == 401
