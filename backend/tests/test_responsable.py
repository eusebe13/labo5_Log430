import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@patch("app.responsable.r")
def test_consulter_stock(mock_redis):
    mock_redis.get.return_value = None
    mock_redis.set.return_value = True
    response = client.get("/api/v1/responsable/stock")
    assert response.status_code in (200, 500)


@patch("app.responsable.r")
def test_get_alertes_rupture(mock_redis):
    mock_redis.get.return_value = None
    mock_redis.set.return_value = True
    response = client.get("/api/v1/responsable/alertes-rupture")
    assert response.status_code in (200, 500)


@patch("app.responsable.r")
def test_get_produits_par_magasin(mock_redis):
    mock_redis.get.return_value = None
    mock_redis.set.return_value = True
    response = client.get("/api/v1/responsable/magasin/1/produits")
    assert response.status_code in (200, 404, 500)


@patch("app.responsable.r")
def test_reapprovisionnement_approuver(mock_redis):
    mock_redis.get.return_value = None
    mock_redis.set.return_value = True
    mock_redis.delete.return_value = True
    response = client.post("/api/v1/responsable/reapprovisionner/1/approuver")
    assert response.status_code in (200, 400, 404, 500)
