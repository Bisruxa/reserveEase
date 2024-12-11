from rest_framework.viewsets import ReadOnlyModelViewSet,ModelViewSet
from django.contrib.auth import get_user_model
from .serializers import UserSerializer,TaskSerializer
from rest_framework.permissions import IsAuthenticated
from Task.models import Task
User = get_user_model() 

class UserViewSet(ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
 