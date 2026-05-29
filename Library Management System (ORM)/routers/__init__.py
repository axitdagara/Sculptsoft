from .auth import protected_router as auth_protected_router
from .auth import public_router as auth_public_router
from .books import protected_router as books_router
from .borrow import protected_router as borrow_router
from .users import protected_router as users_protected_router
from .users import public_router as users_public_router

__all__ = [
    "auth_public_router",
    "auth_protected_router",
    "users_public_router",
    "users_protected_router",
    "books_router",
    "borrow_router",
]