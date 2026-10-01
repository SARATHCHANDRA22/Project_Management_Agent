from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database.database import engine, Base, get_db
from app.models.models import Project, Task
from app.schemas import ProjectCreate, TaskCreate, TaskUpdate
from app.tools.risk_tools import detect_task_risk
from pydantic import BaseModel
from app.agents.project_agent import run_agent


Base.metadata.create_all(bind=engine)


app = FastAPI(title="Project Management Agent")


@app.get("/")
def home():
    return {
        "message": "Project Management Agent is running!"
    }


@app.post("/projects")
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    new_project = Project(
        name=project.name,
        description=project.description,
        deadline=project.deadline
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)
@app.post("/tasks")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == task.project_id
    ).first()

    if not project:
        return {
            "error": "Project not found"
        }

    new_task = Task(
        project_id=task.project_id,
        title=task.title,
        description=task.description,
        deadline=task.deadline,
        priority=task.priority
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        return {
            "error": "Task not found"
        }

    task.status = task_update.status
    task.progress = task_update.progress

    db.commit()
    db.refresh(task)
@app.get("/projects/{project_id}/status")
def get_project_status(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        return {
            "error": "Project not found"
        }

    tasks = db.query(Task).filter(
        Task.project_id == project_id
    ).all()

    task_list = []

    for task in tasks:
        task_list.append({
            "task_id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "progress": task.progress,
            "deadline": task.deadline,
            "priority": task.priority
        })

    return {
        "project_id": project.id,
        "project_name": project.name,
        "description": project.description,
        "deadline": project.deadline,
        "tasks": task_list
    }

    return {
        "message": "Task updated successfully",
        "task_id": task.id,
        "title": task.title,
        "status": task.status,
        "progress": task.progress
    }

    return {
        "message": "Task created successfully",
        "task_id": new_task.id,
        "project_id": new_task.project_id,
        "title": new_task.title,
        "status": new_task.status,
        "progress": new_task.progress,
        "deadline": new_task.deadline,
        "priority": new_task.priority
    }

    return {
        "message": "Project created successfully",
        "project_id": new_project.id,
        "name": new_project.name,
        "description": new_project.description,
        "deadline": new_project.deadline
    }
@app.get("/projects/{project_id}/risks")
def get_project_risks(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        return {
            "error": "Project not found"
        }

    tasks = db.query(Task).filter(
        Task.project_id == project_id
    ).all()

    risk_list = []

    for task in tasks:
        risks = detect_task_risk(task)

        if risks:
            risk_list.append({
                "task_id": task.id,
                "task_title": task.title,
                "risks": risks
            })

    return {
        "project_id": project.id,
        "project_name": project.name,
        "risks": risk_list
    }
class AgentRequest(BaseModel):
    request: str


@app.post("/agent")
def project_management_agent(data: AgentRequest):
    result = run_agent(data.request)

    return {
        "response": result
    }
@app.get("/projects/{project_id}/report")
def get_project_report(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        return {
            "error": "Project not found"
        }

    tasks = db.query(Task).filter(
        Task.project_id == project_id
    ).all()

    total_tasks = len(tasks)

    completed_tasks = sum(
        1 for task in tasks
        if task.progress == 100
    )

    average_progress = (
        sum(task.progress for task in tasks) / total_tasks
        if total_tasks > 0
        else 0
    )

    task_reports = []
    risks = []

    for task in tasks:
        task_risks = detect_task_risk(task)

        task_reports.append({
            "task_id": task.id,
            "title": task.title,
            "status": task.status,
            "progress": task.progress,
            "deadline": task.deadline,
            "priority": task.priority,
            "risks": task_risks
        })

        if task_risks:
            risks.append({
                "task_id": task.id,
                "task_title": task.title,
                "risks": task_risks
            })

    return {
        "project_name": project.name,
        "project_deadline": project.deadline,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "average_progress": round(average_progress, 2),
        "tasks": task_reports,
        "risks": risks
    }