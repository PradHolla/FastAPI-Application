from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", database="fastapiApp", user="postgres", password="cnhpnhcnh", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Connected to the database!")
#         break
#     except Exception as e:
#         print("Unable to connect to the database")
#         print(e)
#         time.sleep(3)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()