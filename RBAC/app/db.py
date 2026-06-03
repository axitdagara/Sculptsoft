from collections.abc import Iterator
from contextlib import contextmanager

from passlib.context import CryptContext
from sqlalchemy import create_engine, event, select
from sqlalchemy.orm import Session

from .config import SQLALCHEMY_DATABASE_URL
from .db_models import Base, DbRole, Permission, Post, RoutePermission, User


pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {},
)


@event.listens_for(engine, "connect")
def _enable_sqlite_foreign_keys(dbapi_connection, _connection_record) -> None:
    if not SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
        return
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.close()


@contextmanager
def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


@contextmanager
def get_transaction() -> Iterator[Session]:
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise


def initialize_database() -> None:
    Base.metadata.create_all(engine)
    with get_transaction() as session:
        _seed_database(session)


def _seed_database(session: Session) -> None:
    roles = ["admin", "editor", "viewer", "manager", "employee"]
    permissions = ["posts:read", "posts:write", "posts:delete", "users:read"]
    users = [
        ("axit", "axit@example.com", "secret123", "admin"),
        ("harsh", "harsh@example.com", "secret123", "editor"),
        ("tirth", "tirth@example.com", "secret123", "viewer"),
        ("mansi", "mansi@example.com", "secret123", "manager"),
        ("employee1", "employee1@example.com", "secret123", "employee"),
    ]
    role_permissions = {
        "viewer": ["posts:read"],
        "editor": ["posts:read", "posts:write"],
        "manager": ["posts:read", "users:read"],
        "employee": ["posts:read"],
        "admin": ["posts:read", "posts:write", "posts:delete", "users:read"],
    }
    route_permissions = {
        ("GET", "/auth/me"): ["viewer", "editor", "manager", "admin"],
        ("GET", "/posts"): ["viewer", "editor", "manager", "admin"],
        ("GET", "/posts/{post_id}"): ["viewer", "editor", "manager", "admin"],
        ("POST", "/posts"): ["editor", "admin"],
        ("DELETE", "/posts/{post_id}"): ["admin"],
        ("GET", "/admin/users"): ["manager", "admin"],
        ("GET", "/admin/permissions"): ["admin"],
    }

    role_by_name: dict[str, DbRole] = {}
    for role in roles:
        db_role = session.scalar(select(DbRole).where(DbRole.name == role))
        if db_role is None:
            db_role = DbRole(name=role)
            session.add(db_role)
        role_by_name[role] = db_role

    permission_by_name: dict[str, Permission] = {}
    for permission in permissions:
        db_permission = session.scalar(select(Permission).where(Permission.name == permission))
        if db_permission is None:
            db_permission = Permission(name=permission)
            session.add(db_permission)
        permission_by_name[permission] = db_permission

    session.flush()

    for username, email, password, role in users:
        db_user = session.scalar(select(User).where(User.username == username))
        if db_user is None:
            db_user = User(username=username, email=email, hashed_password=pwd_ctx.hash(password))
            session.add(db_user)
        db_role = role_by_name[role]
        if db_role not in db_user.roles:
            db_user.roles.append(db_role)

    for role_name, permission_names in role_permissions.items():
        db_role = role_by_name[role_name]
        for permission_name in permission_names:
            db_permission = permission_by_name[permission_name]
            if db_permission not in db_role.permissions:
                db_role.permissions.append(db_permission)

    session.flush()

    for (method, path), route_roles in route_permissions.items():
        for role_name in route_roles:
            db_role = role_by_name[role_name]
            existing_route = session.scalar(
                select(RoutePermission).where(
                    RoutePermission.method == method,
                    RoutePermission.path == path,
                    RoutePermission.role_id == db_role.id,
                )
            )
            if existing_route is None:
                session.add(RoutePermission(method=method, path=path, role=db_role))

    existing_post = session.scalar(select(Post.id).limit(1))
    if existing_post is None:
        axit = session.scalar(select(User).where(User.username == "axit"))
        harsh = session.scalar(select(User).where(User.username == "harsh"))
        session.add_all(
            [
                Post(title="Hello World", body="First post!", author=axit),
                Post(title="FastAPI Tips", body="Use Depends().", author=harsh),
            ]
        )
