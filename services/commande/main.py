# main.py
from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter
from router import router as commande_router

app = FastAPI(
    title="Service Commande",
    description="Microservice pour la validation et traitement des commandes",
    version="1.0.0",
)

# Compteur personnalisé pour le nombre total de requêtes HTTP reçues
REQUEST_COUNT = Counter("commande_request_count", "Nombre total de requêtes reçues par le service commande")

@app.middleware("http")
async def count_requests(request, call_next):
    REQUEST_COUNT.inc()
    response = await call_next(request)
    return response

# Endpoint /metrics exposant les métriques Prometheus
@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

app.include_router(commande_router, prefix="/api/v1/commande", tags=["commandes"])
