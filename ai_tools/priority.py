from django.utils import timezone

DEADLINE_WEIGHT = 35
HARDNESS_WEIGHT = 25
STATUS_WEIGHT = 15
RISK_WEIGHT = 15
CHANCE_WEIGHT = 10


def calculate_priority(task):
    score = (
        calculate_deadline(task)
        + calculate_hardness(task)
        + calculate_status(task)
        + calculate_risk(task)
        + calculate_chance(task)
    )

    return min(score, 100)


def calculate_deadline(task):
    today = timezone.localdate()
    days_left = (task.deadline - today).days

    if days_left <= 0:
        return DEADLINE_WEIGHT
    elif days_left <= 1:
        return 30
    elif days_left <= 3:
        return 24
    elif days_left <= 7:
        return 16
    elif days_left <= 14:
        return 8
    else:
        return 2


def calculate_hardness(task):
    mapping = {
        "easy": 8,
        "medium": 17,
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
        "low": 4,
        "medium": 9,
        "high": RISK_WEIGHT,
    }

    return mapping.get(task.risk_level, 0)


def calculate_chance(task):
    chance = max(0, min(task.completion_chance, 100))
    return round((100 - chance) / 100 * CHANCE_WEIGHT)

def get_priority_level(priority):
    if priority >= 80:
        return "critical"
    elif priority >= 60:
        return "high"
    elif priority >= 40:
        return "medium"
    else:
        return "low"