from rest_framework import serializers
from Task.models import Task,User,Table,Reservation
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'password']  # Include first_name instead of 'name'
        extra_kwargs = {'password': {'write_only': True}}  # Make password write-only for security

    def validate_password(self, value):
        """Ensure the password is strong enough."""
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long')
        return value

    def create(self, validated_data):
        """Hash the password and create a new user."""
        password = validated_data.pop('password', None)  # Remove password before saving user
        user = super().create(validated_data)  # Create the user instance
        user.set_password(password)  # Hash the password before saving
        user.save()  # Save the user instance
        return user

    def validate(self, data):
        """You can perform any additional validation for email or name here if necessary."""
        if not data.get('email'):
            raise serializers.ValidationError("Email is required")
        return data
class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['table_id', 'capacity', 'availability', 'status']
class TaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Task
        fields = ['id', 'size', 'reservation_date', 'description', 'user', 'table']

    def validate_reservation_date(self, value):
        # Ensure reservation date is in the future
        if value <= timezone.now():
            raise serializers.ValidationError("Reservation date must be in the future.")
        return value

    def create(self, validated_data):
        # Ensure the user is automatically set
        user = self.context['request'].user  # Assuming you're using DRF's request context
        validated_data['user'] = user
        return super().create(validated_data)
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id','customer_name','reservation_date','table','status']
