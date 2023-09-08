from pydantic import BaseModel

class TodoBase(BaseModel):
    title: str
    description: str
    status: bool = False

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    class Config:
        orm_mode = True