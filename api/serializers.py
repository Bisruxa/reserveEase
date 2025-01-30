from rest_framework import serializers
from Task.models import Task,User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
class UserSerializer(serializers.ModelSerializer):
   class Meta:
        model = User
        fields = ['username', 'email','password']
        extra_fields = {'password': {'write_only': True}}
   def create(self,validated_date):
        password = validated_date.pop('password',None)
        user = super().create(validated_date)
        if password:
            user.set_password(password)
            user.save()
        return user
class TaskSerializer(serializers.ModelSerializer):
    
    user = serializers.PrimaryKeyRelatedField( read_only=True)
    class Meta:
        model = Task
        fields = "__all__"
    def validate_reservation_date(self, value):
        # Ensure reservation date is in the future
        if value <= timezone.now():
            raise serializers.ValidationError("Reservation date must be in the future.")
        return value

   