from typing import Annotated

import models
from database import engine, session_local
from fastapi import Depends, FastAPI, HTTPException, status, Path
from models import Todos
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

app = FastAPI()
models.base.metadata.create_all(bind=engine)
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class todo_request(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool = False

@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()

@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="todo id not found")

@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: todo_request):
    todo_model = Todos(**todo_request.model_dump())

    db.add(todo_model)
    db.commit()

@app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, todo_request: todo_request, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="todo id not found")
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

@app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db:db_dependency, todo_id:int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id==todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="todo id not found")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()