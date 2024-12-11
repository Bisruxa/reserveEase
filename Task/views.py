from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView
from .forms import TaskForm
from .models import Task

class TaskCreate(CreateView):
  template_name = 'Task/task_create.html'
  form_class = TaskForm
  success_url = reverse_lazy('task_list')

class TaskList(ListView):
  template_name = 'Task/task_list.html'
  model = Task
