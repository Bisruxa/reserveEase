from Task.models import User
from rest_framework import serializers
from Task.models import Task

class UserSerializer(serializers.ModelSerializer):
   class Meta:
        model = User
        fields = ['username', 'email']
       
class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fields = '__all__'