from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserViewSet, TaskViewSet

router = DefaultRouter()
# router.register(r'tasks', views.TaskViewSet, basename='task')
router.register(r'users', UserViewSet, basename='user')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [] + router.urls
