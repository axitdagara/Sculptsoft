try:
    # pydantic v1
    from pydantic import BaseSettings
    _PYDANTIC_V2 = False
except Exception:
    # pydantic v2 splits settings into pydantic-settings package
    from pydantic_settings import BaseSettings
    _PYDANTIC_V2 = True


if _PYDANTIC_V2:
    class Settings(BaseSettings):
        database_url: str
        borrow_limit: int = 5
        fine_per_day: float = 0.50

        model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "allow"}
else:
    class Settings(BaseSettings):
        database_url: str
        borrow_limit: int = 5
        fine_per_day: float = 0.50

        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"
            extra = "allow"


settings = Settings()
