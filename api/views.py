from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from Task.models import Task,Catagory
from .serializers import UserSerializer, TaskSerializer,CatagorySerializer
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
    def get_queryset(self):
        # Only allow the user to see their own profile
        return User.objects.filter(id=self.request.user.id)
class CatagoryViewSet(ModelViewSet):
    queryset = Catagory.objects.all()
    serializer_class = CatagorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 
    def get_queryset(self):
        # Only allow the user to see their own categories
        return Catagory.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Assign the category to the currently authenticated user
        serializer.save(user=self.request.user)
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
    def get_queryset(self):
        # Filter tasks to only those assigned to the current user
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the task to the logged-in user
        serializer.save(user=self.request.user)
  
      
      