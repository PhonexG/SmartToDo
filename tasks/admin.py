from django.contrib import admin

from .models import Topic, Task

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    # Colums of topics that admin can see
    list_display = ["id", "name", "user"]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Colums of tasks that admin can see
    list_display = [
        "id",
        "title",
        "user",
        "topic",
        "deadline",
        "hardness",
        "completion_chance",
        "risk_level",
        "status",
    ]
    list_filter = ["status", "hardness", "risk_level", "topic"]
    search_fields = ["title", "description"]