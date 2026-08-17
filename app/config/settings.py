import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    database_host = os.getenv("DATABASE_HOST")
    database_port = os.getenv("DATABASE_PORT")
    database_user = os.getenv("DATABASE_USER")
    database_password = os.getenv("DATABASE_PASSWORD")
    database_name = os.getenv("DATABASE_NAME")
    bucket_name = os.getenv("BUCKET_NAME")
    aws_profile = os.getenv("AWS_PROFILE")
    aws_region = os.getenv("AWS_REGION")
    front_url = os.getenv("FRONT_URL")


settings = Settings()
