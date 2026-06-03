from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .controller import (
    build_token_response,
    create_post_data,
    delete_post_data,
    get_current_user_profile,
    get_post_data,
    list_permissions_data,
    list_posts_data,
    list_users_data,
    root_data,
)
from .models import Permission, PostCreate, PostOut, Role, Token, UserOut
from .security import authenticate_user, get_current_user, require_permission, require_role


router = APIRouter()


@router.post("/auth/login", response_model=Token, tags=["Auth"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login and get a token."""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong username or password",
        )
    roles = user["roles"]
    return build_token_response(user["username"], roles)


@router.get("/auth/me", response_model=UserOut, tags=["Auth"])
async def me(user: dict = Depends(get_current_user)):
    """Get the current user."""
    return get_current_user_profile(user["username"])


@router.get("/posts", response_model=list[PostOut], tags=["Posts"])
async def list_posts(_: dict = Depends(require_permission(Permission.READ))):
    return list_posts_data()


@router.get("/posts/{post_id}", response_model=PostOut, tags=["Posts"])
async def get_post(post_id: int, _: dict = Depends(require_permission(Permission.READ))):
    post = get_post_data(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/posts", response_model=PostOut, status_code=201, tags=["Posts"])
async def create_post(post: PostCreate, user: dict = Depends(require_permission(Permission.WRITE))):
    return create_post_data(post, user["username"])


@router.delete("/posts/{post_id}", tags=["Posts"])
async def delete_post(post_id: int, user: dict = Depends(require_permission(Permission.DELETE))):
    deleted = delete_post_data(post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": f"Post {post_id} deleted by {user['username']}"}


@router.get("/admin/users", tags=["Admin"])
async def list_users(_: dict = Depends(require_role(Role.ADMIN, Role.MANAGER))):
    return list_users_data()


@router.get("/admin/permissions", tags=["Admin"])
async def list_permissions(_: dict = Depends(require_role(Role.ADMIN))):
    return list_permissions_data()


@router.get("/", tags=["Info"])
async def root():
    return root_data()
