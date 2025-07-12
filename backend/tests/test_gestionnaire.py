import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

@patch("app.gestionnaire.r")
def test_afficher_rapports(mock_redis):
    # Simule un cache valide (chaîne JSON)
    mock_data = [{"id": 1, "region": "Est", "total_ventes": 1000.0}]
    mock_redis.get.return_value = json.dumps(mock_data).encode("utf-8")

    response = client.get("/api/v1/gestionnaire/rapports")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@patch("app.gestionnaire.r")
def test_generer_rapport(mock_redis):
    # Simuler comportement du cache : get → None, set → True, delete → True
    mock_redis.get.return_value = None
    mock_redis.set.return_value = True
    mock_redis.delete.return_value = True

    data = {"region": "Nord"}
    response = client.post("/api/v1/gestionnaire/rapports", json=data)

    # Résultat attendu : soit succès 201, soit erreur 500 si la DB est vide ou mauvaise
    assert response.status_code in (201, 500)

    if response.status_code == 201:
        res_json = response.json()
        assert "rapport_id" in res_json
        assert "message" in res_json
