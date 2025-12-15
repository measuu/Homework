from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean
)
from sqlalchemy.orm import declarative_base, sessionmaker
import logging


app = FastAPI()
logging.basicConfig(level=logging.ERROR)

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

Base = declarative_base()


class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    adopted = Column(Boolean)
    health_status = Column(String)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    completed = Column(Boolean)


Base.metadata.create_all(engine)


class AnimalResponse(BaseModel):
    id: int
    name: str
    age: int
    adopted: bool
    health_status: str | None

    class Config:
        orm_mode = True


class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        orm_mode = True


@app.get("/animals/{animal_id}", response_model=AnimalResponse)
def get_animal(animal_id: int):
    animal = db.query(Animal).filter(Animal.id == animal_id).first()

    if not animal:
        logging.error(f"Animal {animal_id} not found")
        raise HTTPException(status_code=404, detail="Тварину не знайдено")

    if animal.age < 0:
        logging.error(f"Negative age for animal {animal_id}")
        raise HTTPException(
            status_code=400,
            detail="Вік не може бути від’ємним"
        )

    return animal


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    if task_id > 1000:
        logging.error(f"Task id too large: {task_id}")
        raise HTTPException(
            status_code=422,
            detail="task_id не може бути більшим за 1000"
        )

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        logging.error(f"Task {task_id} not found")
        raise HTTPException(
            status_code=404,
            detail="Задачу не знайдено"
        )

    return task