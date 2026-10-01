# Project Management Agent

An Agentic AI-based project management system that helps create tasks, track project progress, identify risks, and prepare project status reports.

## Project Overview

The Project Management Agent combines an LLM with tools, a workflow agent, and a persistent database.

The agent can understand natural-language project management requests and use the appropriate tool to perform the required action.

## Features

* Create projects
* Create project tasks
* Update task status and progress
* View project status
* List project tasks
* Detect project risks
* Prepare project status reports
* Store project and task information in SQLite
* Use LangGraph for agent orchestration
* Use Gemini as the LLM

## Technologies Used

* Python
* FastAPI
* SQLite
* SQLAlchemy
* LangGraph
* LangChain
* Google Gemini API
* Pydantic
* Uvicorn

## Project Structure

```text
Project_Management_Agent/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   │
│   ├── agents/
│   │   ├── project_agent.py
│   │   └── __init__.py
│   │
│   ├── database/
│   │   ├── database.py
│   │   └── __init__.py
│   │
│   ├── models/
│   │   ├── models.py
│   │   └── __init__.py
│   │
│   └── tools/
│       ├── risk_tools.py
│       └── __init__.py
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── project_management.db
```

## Agent Tools

The LangGraph agent has the following tools:

### 1. Get Project Status

Retrieves the current project information and task progress.

### 2. List Project Tasks

Retrieves all tasks belonging to a project.

### 3. Get Project Risks

Checks project tasks for possible risks such as approaching deadlines and low progress.

### 4. Create Project Task

Creates a new task in the SQLite database.

### 5. Update Project Task

Updates the status and progress of an existing task.

### 6. Prepare Project Report

Collects project information, task details, progress, and identified risks for preparing a project status report.

## Architecture

```text
User Request
     │
     ▼
FastAPI
     │
     ▼
LangGraph Agent
     │
     ▼
Gemini LLM
     │
     ▼
Select Appropriate Tool
     │
     ├── Project Status
     ├── List Tasks
     ├── Create Task
     ├── Update Task
     ├── Detect Risks
     └── Prepare Report
     │
     ▼
SQLite Database
     │
     ▼
Tool Result
     │
     ▼
Agent Response
```

## Running the Project

### 1. Activate the virtual environment

Windows PowerShell:

```powershell
venv\Scripts\activate
```

### 2. Start the FastAPI application

```powershell
uvicorn app.main:app --reload
```

### 3. Open Swagger

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger provides an interactive interface for testing the API endpoints.

## API Endpoints

### Create Project

```text
POST /projects
```

### Create Task

```text
POST /tasks
```

### Update Task

```text
PUT /tasks/{task_id}
```

### Get Project Status

```text
GET /projects/{project_id}/status
```

### Get Project Risks

```text
GET /projects/{project_id}/risks
```

### Get Project Report

```text
GET /projects/{project_id}/report
```

### AI Agent

```text
POST /agent
```

Example request:

```json
{
    "request": "Show me the tasks for project 1."
}
```

## Example Project

The project used during development was:

**College Attendance Management System**

Current example tasks include:

* Gather Requirements
* Design Database

The system tracks their status, progress, deadlines, priorities, and risks.

## Risk Detection

The system checks task information and identifies conditions such as:

* Overdue tasks
* Approaching deadlines with low progress
* Tasks marked as delayed
* Low-progress tasks with limited time remaining

## Agentic AI Workflow

The system follows an agentic workflow:

1. The user provides a natural-language request.
2. The LangGraph agent interprets the request.
3. The agent selects an appropriate tool.
4. The selected tool interacts with the database or performs the required analysis.
5. The result is returned to the agent.
6. Gemini generates a natural-language response.

## Security

The Gemini API key is stored in a `.env` file and should not be committed to GitHub.

The `.gitignore` file excludes:

```text
.env
venv/
__pycache__/
*.pyc
project_management.db
```

## Future Improvements

Possible future improvements include:

* Web-based project management dashboard
* User authentication
* Project progress charts
* Email notifications
* Calendar integration
* More advanced risk prediction
* Persistent conversation memory
* Deployment to a cloud platform

## Project Goal

The main goal of this project is to demonstrate how Agentic AI can be used to automate common project management activities by combining an LLM, tools, workflow orchestration, and persistent data storage.

