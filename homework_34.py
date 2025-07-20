from http.client import HTTPException
from flask_login import UserMixin
from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from werkzeug.security import generate_password_hash
from pydantic import BaseModel, EmailStr, field_validator, Field
from settings import Base
import fastapi
from fastapi import FastAPI, Depends, Body, HTTPException
import uvicorn
from settings import get_db


class Participant(Base):
    __tablename__ = "participants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    event: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)

    def __str__(self):
        return f"Participant: name {self.name} with his id {self.id}. He's {self.age} years old"

def init_db():
    base = Base()
    base.drop_db()
    base.create_db()

    partic1= Participant(
        name="Kolya", email="ooo@gmail.com", event='smth', age=18
    )
    with Session() as conn:
        conn.add(partic1)
        conn.commit()

#---------------API---------------

app = FastAPI()

class Partic(BaseModel):
    id: int
    name: str
    email: EmailStr = Field(description="Завдання та можливо його опис")
    event: str
    age: int = Field(ge=12, le=120, description="Вік повинен бути від 12 до 120 років")

    @field_validator("name")
    @classmethod
    def name_must_not_contain_digits(cls, v):
        if any(char.isdigit() for char in v):
            raise ValueError("Ім’я не повинно містити цифр")
        return v

@app.get("/")
async def welcome():
    return "Hello, welcome to the app!!"

@app.post("/participants/")
async def participants(new: Partic):
    with Session() as conn:
        existing = select(Participant).where(Participant.email == new.email)
    if existing:
        raise HTTPException(status_code=422, detail="Учасник з таким email вже існує.")

    db_participant = Participant(
        name=new.name,
        email=new.email,
        event=new.event,
        age=new.age
    )
    with Session() as conn:
        conn.add(db_participant)
        conn.commit()
        conn.refresh(db_participant)

    return {"message": "Учасника створено успішно", "id": db_participant.id}

@app.get("/participants/event/{event_name}")
async def get_participants_by_event(event_name: str):
    with Session() as conn:
        result = conn.query(Participant).filter(Participant.event == event_name).all()
        if not result:
            return {"message": f"Немає учасників для події '{event_name}'", "participants": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(f"{__name__}:app", reload = 1, port = 5040)