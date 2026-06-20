from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from ai_tools.topic_grouping import assign_topic_to_task

from .forms import TaskForm
from .models import Topic, Task


@login_required
def task_list_view(request):
    tasks = Task.objects.filter(user=request.user).order_by("deadline")

    return render(request, "tasks/task_list.html", {
        "tasks": tasks
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
        task.save(update_fields=["status"])

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