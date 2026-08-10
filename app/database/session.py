from sqlalchemy.orm import sessionmaker

from app.database.engine import engine

sessionFactory = sessionmaker(bind=engine, expire_on_commit=False)
