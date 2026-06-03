import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SQLITE_DB_PATH = BASE_DIR / "rbac.sqlite3"
ROUTE_ROLE_CACHE_PATH = BASE_DIR / "route_roles_cache.json"
ENV_FILE_PATH = BASE_DIR / ".env"


def _load_env_file() -> None:
	if not ENV_FILE_PATH.exists():
		return

	for raw_line in ENV_FILE_PATH.read_text(encoding="utf-8").splitlines():
		line = raw_line.strip()
		if not line or line.startswith("#") or "=" not in line:
			continue

		key, value = line.split("=", 1)
		os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env_file()

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-change-in-prod")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", "60"))
TOKEN_EXPIRE_DELTA = timedelta(minutes=TOKEN_EXPIRE_MINUTES)

SQLITE_DB_PATH = Path(os.getenv("SQLITE_DB_PATH", str(SQLITE_DB_PATH)))
SQLALCHEMY_DATABASE_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URL",
    f"sqlite:///{SQLITE_DB_PATH.as_posix()}",
)
ROUTE_ROLE_CACHE_PATH = Path(os.getenv("ROUTE_ROLE_CACHE_PATH", str(ROUTE_ROLE_CACHE_PATH)))
