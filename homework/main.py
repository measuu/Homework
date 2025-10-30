from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import os
import uuid
from datetime import datetime
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import timedelta

app = FastAPI()

UPLOAD_DIR = "photos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

extension = ["image/jpeg", "image/png"]

photos = []

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake = {
    "username": "admin",
    "password": "$2b$12$uZ7CZ7uDdtuZrF6erRrSIu7hkZLh9h72oOGbWBHY5p3k3PEnFYVFe"
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/photos/upload")
async def upload_photo(file: UploadFile = File(...)):
    if file.content_type not in extension:
        raise HTTPException(status_code=400, detail="Дозволені файли JPEG або PNG ")

    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Файл не повинен бути більше ніж 5 мб!")

    ext = file.filename.split(".")[-1]
    unique_name = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as f:
        f.write(contents)

    photos.append({
        "filename": unique_name,
        "upload_time": datetime.now().isoformat()
    })

    return {"message": "Фото завантажено успішно!", "filename": unique_name}

@app.get("/photos/list")
async def list_photos():
    sorted_photos = sorted(photos, key=lambda x: x["upload_time"], reverse=True)
    urls = [f"/photos/{p['filename']}" for p in sorted_photos]
    return {"photos": urls}

@app.get("/photos/{filename}")
async def get_photo(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Фото не знайдено")

    return FileResponse(file_path)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != fake["username"] or not verify_password(form_data.password, fake["password"]):
        raise HTTPException(status_code=401, detail="Невірний логін або пароль")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/me")
async def read_users_me(username: str = Depends(get_current_user)):
    return {"user": username}