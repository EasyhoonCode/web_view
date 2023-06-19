from sqlalchemy import create_engine, Column, Integer, String, Sequence, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///D:\project\project\output\students.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True,
                       connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建 metadata
metadata = MetaData()

# 创建 Base 类
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
metadata.clear()
Base.metadata.create_all(engine)  # recreate all tables



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

