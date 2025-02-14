from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from django.core.exceptions import ValidationError
from Task.models import Task, User, Table,Reservation
from .serializers import UserSerializer, TaskSerializer, TableSerializer,ReservationSerializer
from rest_framework.decorators import action
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Make sure the user is authenticated to view their profile
    authentication_classes = [JWTAuthentication]  # Use JWT authentication for user profiles
    lookup_field = 'id'  # Ensures user detail view uses the 'id' field in the URL

    def get_queryset(self):
        # Only return the currently authenticated user
        return User.objects.filter(id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        """
        Create a new user by accepting first_name, email, and password.
        """
        first_name = request.data.get('first_name')
        email = request.data.get('email')
        password = request.data.get('password')

        if not first_name or not email or not password:
            return Response({"error": "First name, email, and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Use the serializer to create the user
            user_serializer = UserSerializer(data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SigninView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response(
            {"refresh": str(refresh), "access": str(refresh.access_token), "message": "Login successful."},
            status=status.HTTP_200_OK,
        )
        
        
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
        try:
            # Ensure user can only make reservations on available tables
            data = request.data.copy()  
            data['user'] = request.user.id  
    
            # Check if the table is available for the reservation
            table_id = data.get('table')
            if table_id is None:
                return Response({"error": "Table field is required"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                table = Table.objects.get(table_id=table_id)
            except Table.DoesNotExist:
                return Response({"error": "Invalid table ID"}, status=status.HTTP_400_BAD_REQUEST)
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
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        reservation.status = 'Canceled'
        reservation.save()
        return Response({"status": "Reservation canceled"})
    @action(detail=True, methods=['post'])
    def update_reservation(self, request, pk=None):
        reservation = self.get_object()
        reservation.reservation_date = request.data.get('reservation_date')
        reservation.table = request.data.get('table')
        reservation.save()
        return Response({"status": "Reservation updated"})
