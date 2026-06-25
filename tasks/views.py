from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone

from ai_tools.chance import calculate_completion_chance, get_risk_level, get_ai_explanation
from ai_tools.topic_grouping import assign_topic_to_task

from .forms import TaskForm
from .models import Topic, Task


@login_required
def task_list_view(request):
    current_filter = request.GET.get("filter")
    tasks = Task.objects.filter(user=request.user)

    today = timezone.localdate()

    filter_map = {
        "todo": lambda qs: qs.filter(status="todo"),
        "in_progress": lambda qs: qs.filter(status="in_progress"),
        "done": lambda qs: qs.filter(status="done"),
        "high_risk": lambda qs: qs.filter(risk_level="high"),
        "overdue": lambda qs: qs.filter(deadline__lt=today).exclude(status="done"),
    }

    tasks = filter_map.get(current_filter, lambda qs: qs)(tasks)
    tasks = tasks.order_by("deadline")

    return render(request, "tasks/task_list.html", {
        "tasks": tasks,
        "current_filter": current_filter,
    })


@login_required
def task_detail_view(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    return render(request, "tasks/task_detail.html", {
        "task": task
    })


@login_required
def task_create_view(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.status = "todo"
            task.save()

            # Automatically creates or assigns topic based on task text.
            assign_topic_to_task(task)
            task.completion_chance = calculate_completion_chance(task)
            task.risk_level = get_risk_level(task, task.completion_chance)
            task.ai_explanation = get_ai_explanation(task, task.completion_chance)
            task.save(update_fields=["completion_chance", "risk_level", "ai_explanation"])

            return redirect("task_detail", task_id=task.id)

    else:
        form = TaskForm()

    return render(request, "tasks/task_form.html", {
        "form": form,
        "page_title": "Create task"
    })


@login_required
def task_edit_view(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            task = form.save()

            # Recalculate topic if title or description was changed.
            assign_topic_to_task(task)
            task.completion_chance = calculate_completion_chance(task)
            task.risk_level = get_risk_level(task.completion_chance)
            task.ai_explanation = get_ai_explanation(task, task.completion_chance)
            task.save(update_fields=["completion_chance", "risk_level", "ai_explanation"])

            return redirect("task_detail", task_id=task.id)

    else:
        form = TaskForm(instance=task)

    return render(request, "tasks/task_form.html", {
        "form": form,
        "page_title": "Edit task"
    })


@login_required
def task_delete_view(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    if request.method == "POST":
        task.delete()
        return redirect("task_list")

    return render(request, "tasks/task_confirm_delete.html", {
        "task": task
    })


@login_required
@require_POST
def task_change_status_view(request, task_id, status):
    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    allowed_statuses = ["todo", "in_progress", "done"]

    if status in allowed_statuses:
        task.status = status
        task.completion_chance = calculate_completion_chance(task)
        task.risk_level = get_risk_level(task.completion_chance)
        task.ai_explanation = get_ai_explanation(task, task.completion_chance)

        task.save(update_fields=[
            "status",
            "completion_chance",
            "risk_level",
            "ai_explanation"
        ])

    return redirect("task_list")


@login_required
def topic_list_view(request):
    topics = Topic.objects.filter(user=request.user).order_by("name")

    return render(request, "tasks/topic_list.html", {
        "topics": topics
    })


@login_required
def topic_detail_view(request, topic_id):
    topic = get_object_or_404(
        Topic,
        id=topic_id,
        user=request.user
    )

    tasks = Task.objects.filter(
        user=request.user,
        topic=topic
    ).order_by("deadline")

    return render(request, "tasks/topic_detail.html", {
        "topic": topic,
        "tasks": tasks
    })