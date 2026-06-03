from fastapi import FastAPI
import uvicorn

from config.logger import get_logger
from config.security import rbac_middleware
from routers import auth_protected_router, auth_public_router, books_router, borrow_router, users_protected_router, users_public_router


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

app.include_router(auth_public_router)
app.include_router(auth_protected_router)
app.include_router(users_public_router)
app.include_router(users_protected_router)
app.include_router(books_router)
app.include_router(borrow_router)


if __name__ == "__main__":
    logger.info("Starting FastAPI app on http://127.0.0.1:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
