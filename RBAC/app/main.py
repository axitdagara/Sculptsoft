from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import initialize_database
from .router import router
from .security import initialize_route_role_cache, rbac_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    initialize_route_role_cache()
    yield


app = FastAPI(
    title="Simple RBAC Demo",
    description="Simple role based access control app",
    version="1.0.0",
    lifespan=lifespan,
)


app.middleware("http")(rbac_middleware)

app.include_router(router)

