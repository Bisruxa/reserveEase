from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import ModelViewSet
from Task.models import Task
from .serializers import UserSerializer, TaskSerializer
from rest_framework.response import Response
from Task.models import User
from django.utils import timezone
from rest_framework import status
from django.core.exceptions import ValidationError


# class UserProfileView(ModelViewSet):
#     serializer_class = UserSerializer
#     authentication_classes = [JWTAuthentication]  # Ensures token authentication
#     permission_classes = [IsAuthenticated] 

#     def get(self, request, *args, **kwargs):
#         user = request.user  # Get the currently authenticated user
#         serializer = UserProfileSerializer(user)  # Serialize the user data
#         return Response(serializer.data)
#     def get_queryset(self):
#         # Only return the currently authenticated user
#         return User.objects.filter(id=self.request.user.id)

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    permission_classes = []
class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
   
    def list(self, request, *args, **kwargs):
        """List available reservations."""
        reservations = Task.objects.filter(reservation_date__gte=timezone.now())
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new reservation."""
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data.copy()
        data['user'] = request.user.id  # Attach current user to the reservation

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            # Ensure reservation does not conflict
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
      
      