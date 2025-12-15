from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field, validator
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()

DATABASE_URL = "sqlite:///./participants.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    event = Column(String)
    age = Column(Integer)


Base.metadata.create_all(bind=engine)


class ParticipantCreate(BaseModel):
    name: str
    email: EmailStr
    event: str
    age: int = Field(..., ge=12, le=120)

    @validator("name")
    def name_must_not_have_digits(cls, value):
        if any(char.isdigit() for char in value):
            raise ValueError("Ім'я не повинно містити цифр")
        return value


@app.post("/participants/")
def add_participant(participant: ParticipantCreate):
    db = SessionLocal()

    existing = db.query(Participant).filter(Participant.email == participant.email).first()
    if existing:
        raise HTTPException(
            status_code=422,
            detail="Учасник з таким email вже існує"
        )

    new_participant = Participant(
        name=participant.name,
        email=participant.email,
        event=participant.event,
        age=participant.age
    )

    db.add(new_participant)
    db.commit()
    db.refresh(new_participant)
    db.close()

    return new_participant


@app.get("/participants/event/{event_name}")
def get_participants_by_event(event_name: str):
    db = SessionLocal()

    participants = db.query(Participant).filter(
        Participant.event == event_name
    ).all()

    db.close()

    if not participants:
        return []

    return participants