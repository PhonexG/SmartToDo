from django.conf import settings
from django.db import models


class Topic(models.Model):
    # each topic belongs to one user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="topics"
    )
    # topic name
    name = models.CharField(max_length=100)

    class Meta:
        # user can not have two topics with the same name
        unique_together = ["user", "name"]
        # sorting by name
        ordering = ["name"]

    def __str__(self):
        return self.name


class Task(models.Model):
    HARDNESS_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
        ("very_hard", "Very Hard"),
    ]

    STATUS_CHOICES = [
        ("todo", "Todo"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    ]

    RISK_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks"
    )

    # main task title
    title = models.CharField(max_length=150)
    # additional information
    description = models.TextField(blank=True)

    deadline = models.DateField()
    hardness = models.CharField(max_length=20, choices=HARDNESS_CHOICES, default="medium")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")

    completion_chance = models.PositiveIntegerField(default=0)
    risk_level = models.CharField(max_length=20, choices=RISK_CHOICES, default="medium")

    ai_explanation = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title