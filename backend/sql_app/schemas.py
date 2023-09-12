from pydantic import BaseModel, validator

# modelo do "to-do"

class TodoBase(BaseModel):
    title: str
    description: str
    status: bool = False

    @validator("title")
    def title_must_be_not_empty(cls, v):
        if not v:
            raise ValueError('title must be not empty')
        return v

# modelo do "to-do" para criação

class TodoCreate(TodoBase):
    pass

# modelo do "to-do" para configurar operações com banco de dados

class Todo(TodoBase):
    class Config:
        orm_mode = True