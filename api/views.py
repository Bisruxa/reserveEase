from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.core.exceptions import ValidationError
from Task.models import Task, User, Table
from .serializers import UserSerializer, TaskSerializer, TableSerializer

# User Viewset (for managing user profiles)
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Make sure the user is authenticated to view their profile
    authentication_classes = [JWTAuthentication]  # Use JWT authentication for user profiles
    lookup_field = 'id'  # Ensures user detail view uses the 'id' field in the URL

    def get_queryset(self):
        # Only return the currently authenticated user
        return User.objects.filter(id=self.request.user.id)

# Task Viewset (for managing task reservations)
class TableViewSet(ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can view tables

    def get_permissions(self):
        """Only admins can create, update, or delete tables; regular users can only view tables."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Admins can perform write actions (create, update, delete)
            return [IsAdminUser()]
        else:
            # Regular users (authenticated) can only view tables
            return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        """List all available tables."""
        # Get all tables that are available for reservation
        tables = Table.objects.filter(availability=True)
        return super().list(request, *args, **kwargs)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can make reservations

    def list(self, request, *args, **kwargs):
        """List available reservations."""
        # Only return future reservations
        reservations = Task.objects.filter(reservation_date__gte=timezone.now())
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a reservation (task)."""
        # Ensure user can only make reservations on available tables
        data = request.data.copy()  # Use copy to avoid modifying the original request.data
        data['user'] = request.user.id  # Attach authenticated user's ID to the reservation

        # Check if the table is available for the reservation
        table = Table.objects.get(id=data['table'])
        if not table.availability:
            return Response({"error": "This table is not available for reservation."}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with reservation creation
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Save the reservation (task)
            # Mark the table as reserved by updating its availability
            table.availability = False
            table.status = 'Reserved'
            table.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)