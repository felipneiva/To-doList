from sqlalchemy import Boolean, Column, String
from .database import Base

class Todo(Base):
    __tablename__ = "todos"

    title = Column(String, primary_key=True, index=True)
    description = Column(String)
    status = Column(Boolean, default=False)
    