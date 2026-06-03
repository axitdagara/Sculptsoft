import json

from sqlalchemy import select

from .config import ROUTE_ROLE_CACHE_PATH
from .db import get_session, get_transaction
from .db_models import DbRole, Permission, Post, RoutePermission, User


def get_user_with_roles(username: str) -> dict | None:
    with get_session() as session:
        user = session.scalar(select(User).where(User.username == username))
        if user is None:
            return None

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "hashed_password": user.hashed_password,
            "roles": sorted(role.name for role in user.roles),
        }


def list_posts() -> list[dict]:
    with get_session() as session:
        posts = session.scalars(select(Post).join(Post.author).order_by(Post.id)).all()
        return [
            {"id": post.id, "title": post.title, "body": post.body, "author": post.author.username}
            for post in posts
        ]


def get_post(post_id: int) -> dict | None:
    with get_session() as session:
        post = session.scalar(select(Post).where(Post.id == post_id))
        if post is None:
            return None
        return {"id": post.id, "title": post.title, "body": post.body, "author": post.author.username}


def create_post(title: str, body: str, author_username: str) -> dict:
    with get_transaction() as session:
        author = session.scalar(select(User).where(User.username == author_username))
        if author is None:
            raise ValueError("Author not found")

        post = Post(title=title, body=body, author=author)
        session.add(post)
        session.flush()
        post_id = post.id

    return get_post(post_id)


def delete_post(post_id: int) -> bool:
    with get_transaction() as session:
        post = session.get(Post, post_id)
        if post is None:
            return False
        session.delete(post)
        return True


def list_users() -> list[dict]:
    with get_session() as session:
        users = session.scalars(select(User).order_by(User.username)).all()
        return [
            {
                "username": user.username,
                "email": user.email,
                "roles": sorted(role.name for role in user.roles),
            }
            for user in users
        ]


def list_role_permissions() -> dict[str, list[str]]:
    with get_session() as session:
        rows = session.execute(
            select(DbRole.name, Permission.name)
            .join(DbRole.permissions)
            .order_by(DbRole.name, Permission.name)
        ).all()

    result: dict[str, list[str]] = {}
    for role_name, permission_name in rows:
        result.setdefault(role_name, []).append(permission_name)
    return result


def user_has_permission(username: str, permission: str) -> bool:
    with get_session() as session:
        row = session.execute(
            select(Permission.id)
            .join(Permission.roles)
            .join(DbRole.users)
            .where(User.username == username, Permission.name == permission)
            .limit(1)
        ).first()
        return row is not None


def get_route_role_cache() -> dict[str, dict[str, list[str]]]:
    with get_session() as session:
        rows = session.execute(
            select(RoutePermission.method, RoutePermission.path, DbRole.name)
            .join(RoutePermission.role)
            .order_by(RoutePermission.method, RoutePermission.path, DbRole.name)
        ).all()

    route_role_map: dict[str, dict[str, list[str]]] = {}
    for method, path, role_name in rows:
        route_role_map.setdefault(path, {}).setdefault(method, []).append(role_name)
    return route_role_map


def write_route_role_cache_file(route_role_map: dict[str, dict[str, list[str]]]) -> None:
    ROUTE_ROLE_CACHE_PATH.write_text(json.dumps(route_role_map, indent=2), encoding="utf-8")
