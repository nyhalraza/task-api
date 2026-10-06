from fastapi import FastAPI, Path, HTTPException, Response
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

tasks = {
    1: {"title": "Make Notes", "done": False},
    2: {"title": "Prepare Quiz", "done": False},
    3: {"title": "Complete Assignment", "done": True}
}

class Task(BaseModel):
    title: str
    done: bool = False

class UpdateTask(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None
    

@app.get("/")
def index():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/tasks/{id}"]
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def get_all_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int = Path(..., gt=0, description="Task ID")):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return tasks[task_id]



@app.post("/tasks", status_code=201)
def create_task(task: Task):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    new_id = max(tasks.keys(), default=0)+1
    tasks[new_id] = task.dict()
    return {"id": new_id, **tasks[new_id]}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: UpdateTask):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task {task_id} not found")

    if task.title is not None:
        if not task.title.strip():
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        tasks[task_id]["title"] = task.title

    if task.done is not None:
        tasks[task_id]["done"] = task.done
    return tasks[task_id]

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    del tasks[task_id]
    return Response(status_code=204)