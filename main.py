import time
from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import Counter, Histogram, generate_latest

from monolith import (
    user_router,
    products_router,
    carts_router,
    orders_router
)

app = FastAPI(title="Architecture Lab")

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status_code"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"]
)

@app.middleware("http")
async def prometheus_middleware(request, call_next):
    start_time = time.time()

    response = await call_next(request)

    endpoint = request.url.path
    method = request.method
    status_code = response.status_code

    REQUEST_COUNT.labels(
        method=method,
        endpoint=endpoint,
        status_code=status_code
    ).inc()

    REQUEST_LATENCY.labels(
        method=method,
        endpoint=endpoint
    ).observe(time.time() - start_time)

    return response


app.include_router(user_router)
app.include_router(products_router)
app.include_router(carts_router)
app.include_router(orders_router)


@app.get("/")
def cover_page():
    return "Welcome to Architecture Lab"

@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )