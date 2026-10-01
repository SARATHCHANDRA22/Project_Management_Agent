from datetime import datetime


def detect_task_risk(task):
    risks = []

    try:
        deadline = datetime.strptime(
            task.deadline,
            "%Y-%m-%d"
        )

        today = datetime.now()

        days_remaining = (deadline - today).days

        if days_remaining < 0 and task.progress < 100:
            risks.append("Task is overdue.")

        elif days_remaining <= 3 and task.progress < 70:
            risks.append(
                "Deadline is approaching but task progress is low."
            )

        if task.status.lower() == "delayed":
            risks.append("Task is marked as delayed.")

        if task.progress < 30 and days_remaining <= 7:
            risks.append(
                "Task has low progress with limited time remaining."
            )

    except ValueError:
        risks.append("Invalid deadline format.")

    return risks