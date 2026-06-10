from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

from config.logger import get_logger
from config.security import rbac_middleware, redis_client
from routers import (
    auth_protected_router,
    auth_public_router,
    books_router,
    borrow_router,
    reports_public_router,
    users_protected_router,
    users_public_router,
)


logger = get_logger(__name__)


app = FastAPI(
    title="Library Management API",
    description="CRUD API built with FastAPI, SQLAlchemy ORM and Alembic migrations.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


app.middleware("http")(rbac_middleware)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if redis_client and request.url.path.startswith("/api/v1/"):
        client_ip = request.client.host if request.client else "127.0.0.1"
        key = f"rate_limit:{client_ip}"
        try:
            requests = redis_client.incr(key)
            if requests == 1:
                redis_client.expire(key, 60)
            if requests > 100:  # 100 requests per minute limit
                return JSONResponse(status_code=429, content={"detail": "Too many requests"})
        except Exception:
            pass
    return await call_next(request)

app.include_router(auth_public_router)
app.include_router(auth_protected_router)
app.include_router(users_public_router)
app.include_router(users_protected_router)
app.include_router(books_router)
app.include_router(borrow_router)
app.include_router(reports_public_router)


if __name__ == "__main__":
    logger.info("Starting FastAPI app on http://127.0.0.1:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
