from django.contrib.auth.models import User
from rest_framework import serializers
from my_projects.models import Project, Task


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class TaskSerializer(serializers.ModelSerializer):
    project  = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)
    due_date = serializers.DateField(required=False)    
    
    class Meta:
        model = Task
        fields = '__all__'

    def validate(self, data):
        if self.instance:
            return data
        
class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    members = UserSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Project
        fields = '__all__'
    
