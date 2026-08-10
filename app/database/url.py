from sqlalchemy import URL

from app.config.settings import settings

url_object = URL.create(
    "postgresql+psycopg",
    username=settings.database_user,
    password=settings.database_password,
    host=settings.database_host,
    port=int(settings.database_port),
    database=settings.database_name,
)
