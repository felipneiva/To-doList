from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models = models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# configurar o CORS para permitir requisições do frontend

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

# obter a sessão do banco de dados

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# rota para criar um novo "to-do"

@app.post("/todo", response_model=schemas.Todo, status_code=201, tags=["todo"])
def create_todo_item(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    response = crud.get_todo_by_title(db, title=todo.title)
    if response:
        raise HTTPException(status_code=400, detail=f'Todo with title {todo.title} already exists')
    return crud.create_todo_item(db=db, todo=todo)

# rota para obter todos os "to-dos"

@app.get("/todo", response_model=list[schemas.Todo], status_code=200 , tags=["todo"])
def get_todos(db: Session = Depends(get_db)):
    return crud.get_todos(db=db)

# rota para obter "to-dos" concluídos

@app.get("/todo/done", response_model=list[schemas.Todo], status_code=200, tags=["todo"])
def get_done_todos(db: Session = Depends(get_db)):
    return crud.get_done_todos(db=db)

# rota para obter "to-dos" não concluídos

@app.get("/todo/undone", response_model=list[schemas.Todo], status_code=200, tags=["todo"])
def get_undone_todos(db: Session = Depends(get_db)):
    return crud.get_undone_todos(db=db)

# rota para obter um "to-do" pelo título

@app.get("/todo/{title}", response_model=schemas.Todo, status_code=200, tags=["todo"])
def get_todo_by_title(title: str, db: Session = Depends(get_db)):
    response = crud.get_todo_by_title(db=db, title=title)
    if response:
        return response
    raise HTTPException(status_code=404, detail=f'Todo with title {title} not found')

# rota para apagar um "to-do" pelo título

@app.delete("/todo/{title}", status_code=204, tags=["todo"])
def delete_todo_by_title(title: str, db: Session = Depends(get_db)):
    response = crud.get_todo_by_title(db=db, title=title)
    if response:
        crud.delete_todo_by_title(db=db, title=title)
        return
    raise HTTPException(status_code=404, detail=f'Todo with title {title} not found')

# rota para atualizar um "to-do" pelo título e nova descrição

@app.put("/todo/{title}", response_model=schemas.Todo, status_code=200, tags=["todo"])
def update_todo_by_title(title: str, description: str, db: Session = Depends(get_db)):
    response = crud.get_todo_by_title(db=db, title=title)
    if response:
        return crud.update_todo_by_title(db=db, title=title, description=description)
    raise HTTPException(status_code=404, detail=f'Todo with title {title} not found')

# rota para atualizar o status de um "to-do" pelo título 

@app.put("/todo/{title}/toggle-status", response_model=schemas.Todo, status_code=200, tags=["todo"])
def toggle_todo_status(title: str, db: Session = Depends(get_db)):
    response = crud.get_todo_by_title(db=db, title=title)
    if response:
        return crud.toggle_todo_status(db=db, title=title)
    raise HTTPException(status_code=404, detail=f'Todo with title {title} not found')
