from rest_framework import serializers
from Task.models import Task,User,Table
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
   class Meta:
        model = User
        fields = ['name', 'email','password']
        extra_kwargs = {'password': {'write_only': True}}
   def create(self,validated_data):
        password = validated_data.pop('password',None)
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
   def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long')
        return value
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
