from sqlalchemy.orm import Session
from models import Todo
from schemas import TodoCreate, TodoUpdate

def get_all_todos(db: Session):
    return db.query(Todo).all()

def get_todo_by_id(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()

def create_todo(db: Session, todo: TodoCreate):
    db_todo = Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, todo_id: int, update_data: TodoUpdate):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        return None
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(db_todo, field, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
        return True
    return False
