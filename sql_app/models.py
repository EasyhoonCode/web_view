from sqlalchemy import Column, Integer, String, Float
from database import Base
from pydantic import BaseModel
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False)
    age = Column(Integer, nullable=False)
    classname = Column(String(64), nullable=False)
    course_a = Column(Integer, nullable=False)
    course_b = Column(Integer, nullable=False)
    course_c = Column(Integer, nullable=False)
    average_score = Column(Float, nullable=False)
    max_score = Column(Integer, nullable=False)
    min_score = Column(Integer, nullable=False)

class StudentUpdate(BaseModel):
    name: str = None
    age: int = None
    classname: str = None
    course_a: int = None
    course_b: int = None
    course_c: int = None
    average_score :float = None
    max_score : int = None
    min_score : int = None

    class Config:
        orm_mode = True

class StudentCreate(BaseModel):
    name: str
    age: int
    classname: str
    course_a: int
    course_b: int
    course_c: int
    average_score : float
    max_score : int
    min_score : int

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: str = None
    password: str = None

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class UserIn(BaseModel):
    username: str
    password: str

class SignIn(BaseModel):
    username: str
    password: str
    once_password:str