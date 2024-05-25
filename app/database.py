# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base

DATABASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
DATABASE_FILE = 'new_db.sqlite'  # Обновленное имя файла базы данных
DATABASE_PATH = os.path.join(DATABASE_DIR, DATABASE_FILE)
DATABASE_URI = f'sqlite:///{DATABASE_PATH}'

if not os.path.exists(DATABASE_DIR):
    os.makedirs(DATABASE_DIR)

engine = create_engine(DATABASE_URI, connect_args={'check_same_thread': False})
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
    print("Done!")
