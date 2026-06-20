from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "deadline",
            "hardness",
        ]

        labels = {
            "title": "Task name",
        }

        widgets = {
            "deadline": forms.DateInput(attrs={
                "type": "date"
            }),
        }