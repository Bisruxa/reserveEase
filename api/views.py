from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from Task.models import Task
from .serializers import UserSerializer, TaskSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import TaskFilter
from rest_framework import generics

User = get_user_model()

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
   
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TaskFilter

    # Specify default ordering (this is optional, but will help in case no sorting is passed)
    ordering_fields = ['due_date', 'priority']
    ordering = ['due_date']  

