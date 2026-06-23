from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from tasks.models import Task

@login_required
def dashboard_view(request):
    tasks = Task.objects.filter(user=request.user)
    total_tasks = tasks.count()

    done_tasks = tasks.filter(status="done").count()
    todo_tasks = tasks.filter(status="todo").count()
    in_progress_tasks = tasks.filter(status="in_progress").count()

    high_risk_tasks = tasks.filter(risk_level="high").count()

    today = timezone.localdate()
    overdue_tasks = tasks.filter(deadline__lt=today).exclude(status="done")
    today_tasks = tasks.filter(deadline=today)
    upcoming_tasks = tasks.filter(deadline__gt=today).order_by("deadline")[:5]

    context = {
        "total_tasks": total_tasks,
        "done_tasks": done_tasks,
        "todo_tasks": todo_tasks,
        "in_progress_tasks": in_progress_tasks,
        "high_risk_tasks": high_risk_tasks,
        "overdue_tasks": overdue_tasks,
        "today_tasks": today_tasks,
        "upcoming_tasks": upcoming_tasks,
    }

    return render(request, "dashboard/dashboard.html", context)
