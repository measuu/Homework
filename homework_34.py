from fastapi import FastAPI

app = FastAPI()

tasks = []
task_id = 1


@app.post("/tasks")
def add_task(title: str):
    global task_id
    task = {
        "id": task_id,
        "title": title
    }
    tasks.append(task)
    task_id += 1
    return task


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return {"error": "Завдання не знайдено"}


@app.put("/tasks/{task_id}")
def update_task(task_id: int, title: str):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = title
            return task
    return {"error": "Завдання не знайдено"}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Завдання видалено"}
    return {"error": "Завдання не знайдено"}
