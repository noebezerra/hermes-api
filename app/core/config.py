from functools import lru_cache
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBConfig(BaseModel):
    engine: str # oracle | sqlserver | mysql
    host: str
    port: str
    user: str
    password: str
    database: str
    service_name: str | None = None # opcional
    client_lib_dir: str | None = None # oracle thick mode opicional

# Configurações de variáveis de ambiente
class Settings(BaseSettings):
    app_name: str
    app_version: str
    app_env: str
    app_host: str
    app_port: int
    dbs: dict[str, DBConfig] = {}

    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore", 
        env_nested_delimiter="__",
    )

@lru_cache
def get_settings():
    return Settings()
