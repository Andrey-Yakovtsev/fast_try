from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///./db.sqlite3"
    # echo: bool = False
    echo: bool = True
    echo_pool: bool = True


settings = Settings()
