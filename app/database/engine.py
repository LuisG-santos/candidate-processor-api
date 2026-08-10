from sqlalchemy import create_engine
from app.database.url import url_object

engine = create_engine(url_object)