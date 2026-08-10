from app.database.engine import engine
from sqlalchemy.orm import sessionmaker

sessionFactory = sessionmaker(bind=engine, expire_on_commit=False)
