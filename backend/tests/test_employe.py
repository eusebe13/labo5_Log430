import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

@patch("app.employe.r")
def test_consulter_produits(mock_redis):
    mock_redis.get.return_value = None
    mock_redis.set.return_value = True

    response = client.get("/api/v1/employe/produits")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@patch("app.employe.r")
def test_verifier_stock(mock_redis):
    mock_redis.get.return_value = None
    response = client.get("/api/v1/employe/stock/1/magasin/1")
    assert response.status_code in (200, 404)

@patch("app.employe.r")
def test_acheter_produits(mock_redis):
    mock_redis.get.return_value = None
    data = [{"produit_id": 1, "quantite": 1}]
    response = client.post("/api/v1/employe/acheter/1", json=data)
    assert response.status_code in (200, 400)
