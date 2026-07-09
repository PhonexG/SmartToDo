from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from tasks.models import Task


@login_required
def dashboard_view(request):
    tasks = Task.objects.filter(user=request.user)

    today = timezone.localdate()

    total_tasks = tasks.count()
    todo_tasks = tasks.filter(status="todo").count()
    in_progress_tasks = tasks.filter(status="in_progress").count()
    done_tasks = tasks.filter(status="done").count()

    high_risk_tasks = tasks.filter(risk_level="high").count()

    overdue_tasks = tasks.filter(
        deadline__lt=today
    ).exclude(status="done")

    today_tasks = tasks.filter(deadline=today)

    priority_tasks = (
        tasks.exclude(status="done")
        .order_by("-priority", "deadline")[:5]
    )

    context = {
        "total_tasks": total_tasks,
        "todo_tasks": todo_tasks,
        "in_progress_tasks": in_progress_tasks,
        "done_tasks": done_tasks,
        "high_risk_tasks": high_risk_tasks,
        "overdue_tasks": overdue_tasks,
        "today_tasks": today_tasks,
        "priority_tasks": priority_tasks,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )