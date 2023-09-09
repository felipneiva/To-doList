from sqlalchemy.orm import Session

from . import models, schemas

# criar um novo "to-do"

def create_todo_item(db: Session, todo: schemas.TodoCreate): 
    db_todo = models.Todo(title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# obter todos os "to-dos"

def get_todos(db: Session):
    return db.query(models.Todo).all()

# obter "to-dos" concluídos

def get_done_todos(db: Session):
    return db.query(models.Todo).filter(models.Todo.status == True).all()

# obter "to-dos" não concluídos

def get_undone_todos(db: Session):
    return db.query(models.Todo).filter(models.Todo.status == False).all()

# obter um "to-do" pelo título

def get_todo_by_title(db: Session, title: str):
    return db.query(models.Todo).filter(models.Todo.title == title).first()

# apagar um "to-do" pelo título

def delete_todo_by_title(db: Session, title: str):
    db.query(models.Todo).filter(models.Todo.title == title).delete()
    db.commit()

# atualizar um "to-do" pelo título e nova descrição

def update_todo_by_title(db: Session, title: str, description: str):
    db_todo = db.query(models.Todo).filter(models.Todo.title == title).first()
    db_todo.description = description
    db.commit()
    db.refresh(db_todo)
    return db_todo

# atualizar o status de um "to-do" pelo título

def toggle_todo_status(db: Session, title: str):
    db_todo = db.query(models.Todo).filter(models.Todo.title == title).first()
    db_todo.status = not db_todo.status
    db.commit()
    db.refresh(db_todo)
    return db_todo