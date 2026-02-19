from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST : str
    DB_PORT : int
    DB_USER : str
    DB_PASS : str
    DB_NAME : str
    DB_DRIVER : str
    DATABASE_URL : str
    
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRES_MINUTES: int
    
    SMTP_MAIL_HOST: str
    SMTP_EMAIL: str
    SMTP_PWD: str
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()