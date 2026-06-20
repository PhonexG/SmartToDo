from django.urls import path

from . import views

urlpatterns = [
    path("", views.task_list_view, name="task_list"),
    path("create/", views.task_create_view, name="task_create"),
    path("<int:task_id>/", views.task_detail_view, name="task_detail"),
    path("<int:task_id>/edit/", views.task_edit_view, name="task_edit"),
    path("<int:task_id>/delete/", views.task_delete_view, name="task_delete"),
    path("<int:task_id>/status/<str:status>/", views.task_change_status_view, name="task_change_status"),

    path("topics/", views.topic_list_view, name="topic_list"),
    path("topics/<int:topic_id>/", views.topic_detail_view, name="topic_detail"),
]