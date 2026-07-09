from .chance import (
    calculate_completion_chance,
    get_risk_level,
    get_ai_explanation,
)

from .priority import (
    calculate_priority,
    get_priority_level,
)


def update_task_analysis(task):
    task.completion_chance = calculate_completion_chance(task)
    task.risk_level = get_risk_level(task.completion_chance)
    task.ai_explanation = get_ai_explanation(task, task.completion_chance)

    task.priority = calculate_priority(task)
    task.priority_level = get_priority_level(task.priority)