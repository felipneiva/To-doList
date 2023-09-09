from pydantic import BaseModel

# modelo do "to-do"

class TodoBase(BaseModel):
    title: str
    description: str
    status: bool = False

# modelo do "to-do" para criação

class TodoCreate(TodoBase):
    pass

# modelo do "to-do" para configurar operações com banco de dados

class Todo(TodoBase):
    class Config:
        orm_mode = True