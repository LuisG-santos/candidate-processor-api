import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    database_host = os.getenv("DATABASE_HOST")
    database_port = os.getenv("DATABASE_PORT")
    database_user = os.getenv("DATABASE_USER")
    database_password = os.getenv("DATABASE_PASSWORD")
    database_name = os.getenv("DATABASE_NAME")


settings = Settings()
