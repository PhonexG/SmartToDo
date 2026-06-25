from django.utils import timezone


def calculate_completion_chance(task):
    if task.status == "done":
        return 100

    today = timezone.localdate()
    days_left = (task.deadline - today).days

    chance = 55

    # Deadline factor
    if days_left < 0:
        chance -= 45
    elif days_left == 0:
        chance -= 30
    elif days_left <= 1:
        chance -= 22
    elif days_left <= 3:
        chance -= 14
    elif days_left <= 7:
        chance -= 5
    elif days_left <= 14:
        chance += 8
    else:
        chance += 14

    # Hardness factor
    hardness_scores = {
        "easy": 22,
        "medium": 5,
        "hard": -15,
        "very_hard": -30,
    }

    chance += hardness_scores.get(task.hardness, 0)

    # Status factor
    status_scores = {
        "todo": 0,
        "in_progress": 18,
    }

    chance += status_scores.get(task.status, 0)

    # Description clarity factor
    description = task.description.strip()

    if len(description) == 0:
        chance -= 6
    elif len(description) >= 40:
        chance += 5

    # Keep result realistic
    return max(1, min(99, chance))


def get_risk_level(task_or_chance, chance=None):
    if chance is None:
        chance = task_or_chance
        task = None
    else:
        task = task_or_chance

    if task is not None:
        today = timezone.localdate()

        if task.status != "done" and task.deadline < today:
            return "high"

    if chance >= 75:
        return "low"

    if chance >= 45:
        return "medium"

    return "high"


def get_ai_explanation(task, chance):
    today = timezone.localdate()
    days_left = (task.deadline - today).days

    if task.status == "done":
        return "This task is already completed, so the completion chance is 100%."

    reasons = []

    if days_left < 0:
        reasons.append("the deadline has already passed")
    elif days_left == 0:
        reasons.append("the deadline is today")
    elif days_left <= 3:
        reasons.append("the deadline is very close")
    elif days_left > 14:
        reasons.append("there is enough time before the deadline")

    if task.hardness == "easy":
        reasons.append("the task is easy")
    elif task.hardness == "hard":
        reasons.append("the task is hard")
    elif task.hardness == "very_hard":
        reasons.append("the task is very hard")

    if task.status == "in_progress":
        reasons.append("the task is already in progress")

    if not task.description.strip():
        reasons.append("the task description is empty, so planning may be less clear")

    if chance >= 75:
        result = "This task has a high completion chance"
    elif chance >= 45:
        result = "This task has a medium completion chance"
    else:
        result = "This task has a low completion chance"

    if reasons:
        return result + " because " + ", ".join(reasons) + "."

    return result + " based on its deadline, hardness, and current status."