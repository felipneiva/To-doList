from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models = models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.post("/todo", response_model=schemas.Todo, status_code=201, tags=["todo"])
def create_todo_item(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    response = crud.get_todo_by_title(db, title=todo.title)
    if response:
        raise HTTPException(status_code=400, detail=f'Todo with title {todo.title} already exists')
    return crud.create_todo_item(db=db, todo=todo)

@app.get("/todo", response_model=list[schemas.Todo], status_code=200 , tags=["todo"])
def get_todos(db: Session = Depends(get_db)):
    return crud.get_todos(db=db)

@app.get("/todo/done", response_model=list[schemas.Todo], status_code=200, tags=["todo"])
def get_done_todos(db: Session = Depends(get_db)):
    return crud.get_done_todos(db=db)

@app.get("/todo/undone", response_model=list[schemas.Todo], status_code=200, tags=["todo"])
def get_undone_todos(db: Session = Depends(get_db)):
    return crud.get_undone_todos(db=db)

@app.get("/todo/{title}", response_model=schemas.Todo, status_code=200, tags=["todo"])
def get_todo_by_title(title: str, db: Session = Depends(get_db)):
    response = crud.get_todo_by_title(db=db, title=title)
    if response:
        return response
    raise HTTPException(status_code=404, detail=f'Todo with title {title} not found')

@app.delete("/todo/{title}", status_code=204, tags=["todo"])
def delete_todo_by_title(title: str, db: Session = Depends(get_db)):
    response = crud.get_todo_by_title(db=db, title=title)
    if response:
        crud.delete_todo_by_title(db=db, title=title)
        return
    raise HTTPException(status_code=404, detail=f'Todo with title {title} not found')

@app.put("/todo/{title}", response_model=schemas.Todo, status_code=200, tags=["todo"])
def update_todo_by_title(title: str, description: str, db: Session = Depends(get_db)):
    response = crud.get_todo_by_title(db=db, title=title)
    if response:
        return crud.update_todo_by_title(db=db, title=title, description=description)
    raise HTTPException(status_code=404, detail=f'Todo with title {title} not found')

@app.put("/todo/{title}/toggle-status", response_model=schemas.Todo, status_code=200, tags=["todo"])
def toggle_todo_status(title: str, db: Session = Depends(get_db)):
    response = crud.get_todo_by_title(db=db, title=title)
    if response:
        return crud.toggle_todo_status(db=db, title=title)
    raise HTTPException(status_code=404, detail=f'Todo with title {title} not found')














'''fake_db = []

async def fetch_todo(title: str):
    for todo in fake_db:
        if todo.title == title:
            return todo
    return None

@app.post("/todo", response_model=Todo, status_code=201, tags=["todo"])
async def create_todo(todo: Todo):
    response = await fetch_todo(todo.title)
    if not response:
        fake_db.append(todo)
        return todo
    raise HTTPException(status_code=400, detail=f'Todo with title {todo.title} already exists')

@app.get("/todo", response_model=list[Todo], status_code=200 , tags=["todo"])
async def get_todos():
    return fake_db

@app.get("/todo/done", response_model=list[Todo], status_code=200, tags=["todo"])
async def get_done_todos():
    return [todo for todo in fake_db if todo.status]

@app.get("/todo/undone", response_model=list[Todo], status_code=200, tags=["todo"])
async def get_undone_todos():
    return [todo for todo in fake_db if not todo.status]

@app.get("/todo/{title}", response_model=Todo, status_code=200, tags=["todo"])
async def get_todo_by_title(title: str):
    response = await fetch_todo(title)
    if response:
        return response
    raise HTTPException(status_code=404, detail=f'Todo with title {title} not found')

@app.delete("/todo/{title}", status_code=204, tags=["todo"])
async def delete_todo_by_title(title: str):
    response = await fetch_todo(title)
    if response:
        fake_db.remove(response)
        return
    raise HTTPException(status_code=404, detail=f'Todo with title {title} not found')

@app.put("/todo/{title}", response_model=Todo, status_code=200, tags=["todo"])
async def update_todo_by_title(title: str, description: str):
    response = await fetch_todo(title)
    if response:
        response.description = description
        return response
    raise HTTPException(status_code=404, detail=f'Todo with title {title} not found')

@app.put("/todo/{title}/toggle-status", response_model=Todo, status_code=200, tags=["todo"])
async def toggle_todo_status(title: str):
    response = await fetch_todo(title)
    if response:
        response.status = not response.status
        return response
    raise HTTPException(status_code=404, detail=f'Todo with title {title} not found')'''