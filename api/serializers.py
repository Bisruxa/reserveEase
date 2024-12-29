from rest_framework import serializers
from Task.models import Task,Catagory,User
# from django.contrib.auth import get_user_model
# User = get_user_model()
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
class CatagorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Catagory 
        fields= ['id','name']       
class TaskSerializer(serializers.ModelSerializer):
    catagory = CatagorySerializer(read_only=True)
    catagory_id = serializers.PrimaryKeyRelatedField(queryset=Catagory.objects.all(), source='catagory', write_only=True)
    user = serializers.PrimaryKeyRelatedField( read_only=True)
    class Meta:
        model = Task
        fields = "__all__"
    def validate_status(self, value):
        task = self.instance
        if task and task.status == Task.COMPLETED and value != Task.COMPLETED:
            raise serializers.ValidationError("Completed tasks cannot be changed to another status unless reverted to incomplete.")
        return value

   