from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore[call-arg]  # values come from env vars at runtime
