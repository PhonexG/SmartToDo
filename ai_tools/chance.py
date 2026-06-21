from django.utils import timezone


def calculate_completion_chance(task):
    today = timezone.localdate()
    days_left = (task.deadline - today).days

    hardness_penalty = {
        "easy": 5,
        "medium": 20,
        "hard": 35,
        "very_hard": 50,
    }.get(task.hardness, 20)

    status_bonus = {
        "todo": 0,
        "in_progress": 15,
        "done": 100,
    }.get(task.status, 0)

    if task.status == "done":
        return 100

    if days_left < 0:
        time_score = -50
    elif days_left == 0:
        time_score = -30
    elif days_left <= 2:
        time_score = -15
    elif days_left <= 7:
        time_score = 5
    else:
        time_score = 15

    chance = 70 + time_score - hardness_penalty + status_bonus

    return max(0, min(100, chance))


def get_risk_level(chance):
    if chance >= 70:
        return "low"
    if chance >= 40:
        return "medium"
    return "high"


def get_ai_explanation(task, chance):
    if task.status == "done":
        return "This task is already completed, so the completion chance is 100%."

    if chance >= 70:
        return "This task looks manageable because the deadline and hardness are not too risky."

    if chance >= 40:
        return "This task has medium risk. The deadline or hardness may make it harder to finish."

    return "This task is risky. The deadline is close, the task is hard, or both."