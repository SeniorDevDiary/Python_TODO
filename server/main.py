from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# -------------------------------
# Pydantic Models
# -------------------------------
class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = ""
    completed: bool = False

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = ""

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# -------------------------------
# In-Memory Storage
# -------------------------------
todos: List[Todo] = []
current_id = 0

# -------------------------------
# Helper
# -------------------------------
def get_todo(todo_id: int) -> Optional[Todo]:
    return next((todo for todo in todos if todo.id == todo_id), None)



# -------------------------------
# API Routes
# -------------------------------
@app.get("/")
def read_root():
    return "Hello world"

@app.post("/todos/", response_model=Todo)
def create_todo(todo: TodoCreate):
    global current_id
    current_id += 1
    new_todo = Todo(id=current_id, **todo.dict())
    todos.append(new_todo)
    return new_todo

@app.get("/todos/", response_model=List[Todo])
def read_todos():
    return todos

@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int):
    todo = get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, update: TodoUpdate):
    todo = get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if update.title is not None:
        todo.title = update.title
    if update.description is not None:
        todo.description = update.description
    if update.completed is not None:
        todo.completed = update.completed
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    global todos
    todo = get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos = [t for t in todos if t.id != todo_id]
    return {"message": "Todo deleted"}
