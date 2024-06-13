import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Explicitly load the .env file
load_dotenv()


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = "../.env"


settings = Settings()

