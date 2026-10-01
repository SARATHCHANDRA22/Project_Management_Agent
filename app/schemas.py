from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    description: str
    deadline: str


class TaskCreate(BaseModel):
    project_id: int
    title: str
    description: str
    deadline: str
    priority: str = "Medium"
class TaskUpdate(BaseModel):
    status: str
    progress: int