import asyncio
from fastapi import FastAPI, HTTPException, Response
import httpx
from fastapi import status
import uvicorn


app = FastAPI(debug=True)

users = ['Dima', 'Kolya', 'Misha']


@app.get("/get_users/")
async def get_all_users():
    return {"users": users}


@app.post("/add_users/{name}")
async def add_user(name: str):
    if name in users:
        raise HTTPException(status_code=400, detail=f"Ім'я {name} існує")
    users.append(name)
    return {"name": name}

@app.delete("/delete_name/{name}")
async def delete_users(name:str):
    for i in users:
        if name == i:
            users.remove(i)
            return users
        else:
            raise HTTPException(status_code=400, detail=f"Ім'я {name} не існує")

if __name__ == "__main__":
    uvicorn.run("homework_34:app", reload=True)