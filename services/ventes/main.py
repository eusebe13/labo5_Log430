from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter
from router import router as ventes_router

app = FastAPI(
    title="Service Ventes",
    description="Microservice pour la gestion des ventes",
)

# Compteur personnalisé pour le nombre total de requêtes HTTP reçues
REQUEST_COUNT = Counter("ventes_request_count", "Nombre total de requêtes reçues par le service ventes")

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

app.include_router(ventes_router, prefix="/api/v1/ventes", tags=["ventes"])
