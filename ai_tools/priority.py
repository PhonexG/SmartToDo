from django.utils import timezone


DEADLINE_WEIGHT = 35
HARDNESS_WEIGHT = 25
STATUS_WEIGHT = 15
RISK_WEIGHT = 15
CHANCE_WEIGHT = 10


def calculate_priority(task):
    score = 0

    score += calculate_deadline(task)
    score += calculate_hardness(task)
    score += calculate_status(task)
    score += calculate_risk(task)
    score += calculate_chance(task)

    return score


def calculate_deadline(task):
    today = timezone.localdate()
    days_left = (task.deadline - today).days

    if days_left <= 0:
        return DEADLINE_WEIGHT
    elif days_left == 1:
        return 30
    elif days_left <= 3:
        return 25
    elif days_left <= 7:
        return 18
    elif days_left <= 14:
        return 10
    else:
        return 5


def calculate_hardness(task):
    mapping = {
        "easy": 5,
        "medium": 15,
        "hard": HARDNESS_WEIGHT,
    }

    return mapping.get(task.hardness, 0)


def calculate_status(task):
    mapping = {
        "todo": STATUS_WEIGHT,
        "in_progress": 8,
        "done": 0,
    }

    return mapping.get(task.status, 0)


def calculate_risk(task):
    mapping = {
        "low": 5,
        "medium": 10,
        "high": RISK_WEIGHT,
    }

    return mapping.get(task.risk_level, 0)


def calculate_chance(task):
    chance = task.completion_chance

    if chance >= 90:
        return 0
    elif chance >= 70:
        return 3
    elif chance >= 50:
        return 6
    elif chance >= 30:
        return 8
    else:
        return CHANCE_WEIGHT