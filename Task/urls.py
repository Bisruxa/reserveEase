from django.urls import path
from . import views

urlpatterns = [
  path("tasks/", views.TaskCreate.as_view(), name="task-create"),
  # path("tasks/<int:pk>/", views.TaskDetail.as_view(), name="task-detail"),
  path("tasks/list/", views.TaskList.as_view(), name="task_list"),
]