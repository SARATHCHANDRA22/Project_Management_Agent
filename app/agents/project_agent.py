from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from app.config import GEMINI_API_KEY
from app.database.database import SessionLocal
from app.models.models import Project, Task
from app.tools.risk_tools import detect_task_risk


llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=GEMINI_API_KEY
)


@tool
def get_project_status(project_id: int):
    """Get the current status and tasks of a project."""

    db = SessionLocal()

    try:
        project = db.query(Project).filter(
            Project.id == project_id
        ).first()

        if not project:
            return {"error": "Project not found"}

        tasks = db.query(Task).filter(
            Task.project_id == project_id
        ).all()

        return {
            "project_id": project.id,
            "project_name": project.name,
            "description": project.description,
            "deadline": project.deadline,
            "tasks": [
                {
                    "task_id": task.id,
                    "title": task.title,
                    "status": task.status,
                    "progress": task.progress,
                    "deadline": task.deadline,
                    "priority": task.priority
                }
                for task in tasks
            ]
        }

    finally:
        db.close()

@tool
def list_project_tasks(project_id: int):
    """List all tasks belonging to a project."""

    db = SessionLocal()

    try:
        project = db.query(Project).filter(
            Project.id == project_id
        ).first()

        if not project:
            return {"error": "Project not found"}

        tasks = db.query(Task).filter(
            Task.project_id == project_id
        ).all()

        if not tasks:
            return {
                "project_id": project_id,
                "message": "No tasks found for this project."
            }

        return {
            "project_id": project_id,
            "project_name": project.name,
            "tasks": [
                {
                    "task_id": task.id,
                    "title": task.title,
                    "status": task.status,
                    "progress": task.progress,
                    "deadline": task.deadline,
                    "priority": task.priority
                }
                for task in tasks
            ]
        }

    finally:
        db.close()


@tool
def get_project_risks(project_id: int):
    """Detect risks in the tasks of a project."""

    db = SessionLocal()

    try:
        tasks = db.query(Task).filter(
            Task.project_id == project_id
        ).all()

        if not tasks:
            return {"message": "No tasks found for this project."}

        risks = []

        for task in tasks:
            task_risks = detect_task_risk(task)

            if task_risks:
                risks.append({
                    "task_id": task.id,
                    "task_title": task.title,
                    "risks": task_risks
                })

        return {
            "project_id": project_id,
            "risks": risks
        }

    finally:
        db.close()


@tool
def create_project_task(
    project_id: int,
    title: str,
    description: str,
    deadline: str,
    priority: str = "Medium"
):
    """Create a new task for an existing project."""

    db = SessionLocal()

    try:
        project = db.query(Project).filter(
            Project.id == project_id
        ).first()

        if not project:
            return {"error": "Project not found"}

        new_task = Task(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline,
            priority=priority
        )

        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        return {
            "message": "Task created successfully",
            "task_id": new_task.id,
            "project_id": new_task.project_id,
            "title": new_task.title,
            "description": new_task.description,
            "status": new_task.status,
            "progress": new_task.progress,
            "deadline": new_task.deadline,
            "priority": new_task.priority
        }

    finally:
        db.close()


@tool
def update_project_task(
    task_id: int,
    status: str,
    progress: int
):
    """Update the status and progress of an existing task."""

    db = SessionLocal()

    try:
        task = db.query(Task).filter(
            Task.id == task_id
        ).first()

        if not task:
            return {"error": "Task not found"}

        allowed_statuses = [
            "Pending",
            "In Progress",
            "Completed",
            "Delayed"
        ]

        if status not in allowed_statuses:
            return {
                "error": (
                    "Invalid status. Use one of: "
                    "Pending, In Progress, Completed, Delayed."
                )
            }

        if progress < 0 or progress > 100:
            return {
                "error": "Progress must be between 0 and 100."
            }

        task.status = status
        task.progress = progress

        db.commit()
        db.refresh(task)

        return {
            "message": "Task updated successfully",
            "task_id": task.id,
            "title": task.title,
            "status": task.status,
            "progress": task.progress
        }

    finally:
        db.close()

@tool
def prepare_project_report(project_id: int):
    """Collect complete project information for preparing a status report."""

    db = SessionLocal()

    try:
        project = db.query(Project).filter(
            Project.id == project_id
        ).first()

        if not project:
            return {"error": "Project not found"}

        tasks = db.query(Task).filter(
            Task.project_id == project_id
        ).all()

        task_details = []
        all_risks = []

        for task in tasks:
            task_risks = detect_task_risk(task)

            task_details.append({
                "task_id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "progress": task.progress,
                "deadline": task.deadline,
                "priority": task.priority,
                "risks": task_risks
            })

            if task_risks:
                all_risks.append({
                    "task_id": task.id,
                    "task_title": task.title,
                    "risks": task_risks
                })

        if tasks:
            average_progress = sum(
                task.progress for task in tasks
            ) / len(tasks)
        else:
            average_progress = 0

        completed_tasks = sum(
            1 for task in tasks
            if task.progress == 100
        )

        return {
            "project_id": project.id,
            "project_name": project.name,
            "description": project.description,
            "project_deadline": project.deadline,
            "total_tasks": len(tasks),
            "completed_tasks": completed_tasks,
            "average_progress": round(average_progress, 2),
            "tasks": task_details,
            "risks": all_risks
        }

    finally:
        db.close()


tools = [
    get_project_status,
    list_project_tasks,
    get_project_risks,
    create_project_task,
    update_project_task,
    prepare_project_report
]


agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt="""
You are a Project Management Agent.

Your job is to help manage projects using the available tools.

Follow these rules:

1. For requests about the current project status, use get_project_status.
2. For requests to list or show project tasks, use list_project_tasks.
3. For requests about risks or delays, use get_project_risks.
4. For requests to create a new task, use create_project_task.
5. For requests to update a task's status or progress, use update_project_task.
6. For requests to prepare a project status report, use prepare_project_report.

Always use the appropriate tool when project data is required.
Do not invent project information.
After receiving tool results, give the user a clear and concise response.
"""
)


def run_agent(user_request: str):
    """Run the project management agent."""

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_request
                }
            ]
        }
    )

    content = response["messages"][-1].content

    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                return item.get("text", "")

    return content