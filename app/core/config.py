from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str = "61901c6b942d6538c80535d6c7573e738e83d329f7a64fb3b48f2374a9194d16"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    MASTER_DATABASE_URL: str = "sqlite:///./master.db"

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

settings = Settings()