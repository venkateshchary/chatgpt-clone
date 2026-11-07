from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str = "postgresql+asyncpg://chat:chat@localhost:5432/chatdb"
    ollama_url: str = "http://localhost:11434"
    default_model: str = "llama3.2:3b"
    history_limit: int = 20          # last N messages sent to the model
    cors_origins: list[str] = ["http://localhost:5173"]


settings = Settings()
