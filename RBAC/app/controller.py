from .data import (
    create_post,
    delete_post,
    get_post,
    get_route_role_cache,
    get_user_with_roles,
    list_posts,
    list_role_permissions,
    list_users,
)
from .models import PostCreate, PostOut, Token, UserOut
from .security import create_access_token


def build_token_response(username: str, roles: list[str]) -> Token:
    token = create_access_token(username, roles)
    return Token(access_token=token, token_type="bearer", roles=roles)


def get_current_user_profile(username: str) -> UserOut:
    db_user = get_user_with_roles(username)
    if db_user is None:
        raise ValueError("User not found")
    return UserOut(
        username=db_user["username"],
        email=db_user["email"],
        roles=db_user["roles"],
    )


def list_posts_data() -> list[dict]:
    return list_posts()


def get_post_data(post_id: int) -> dict | None:
    return get_post(post_id)


def create_post_data(post: PostCreate, username: str) -> PostOut:
    return create_post(post.title, post.body, username)


def delete_post_data(post_id: int) -> bool:
    return delete_post(post_id)


def list_users_data() -> list[dict]:
    return list_users()


def list_permissions_data() -> dict[str, list[str]]:
    return list_role_permissions()


def root_data() -> dict:
    return {
        "message": "Simple RBAC demo",
        "docs": "/docs",
        "route_role_cache_file": "route_roles_cache.json",
        "users": {
            "axit": {"role": "admin", "password": "secret123"},
            "harsh": {"role": "editor", "password": "secret123"},
            "tirth": {"role": "viewer", "password": "secret123"},
            "mansi": {"role": "manager", "password": "secret123"},
        },
        "route_roles": get_route_role_cache(),
    }
