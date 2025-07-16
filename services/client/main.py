from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter
from router import router as client_router

app = FastAPI(
    title="Service Client",
    description="Microservice pour la création et gestion des comptes clients",
    version="1.0.0",
)

# Compteur personnalisé pour le nombre total de requêtes HTTP reçues
REQUEST_COUNT = Counter("client_request_count", "Nombre total de requêtes reçues par le service client")

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

app.include_router(client_router, prefix="/api/v1/clients", tags=["clients"])
