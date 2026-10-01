from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime

from app.database.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    deadline = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="Pending")
    progress = Column(Integer, default=0)
    deadline = Column(String)
    priority = Column(String, default="Medium")
    created_at = Column(DateTime, default=datetime.utcnow)