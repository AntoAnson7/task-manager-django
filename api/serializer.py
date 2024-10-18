from dataclasses import field
from pyexpat import model
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import NewTask,Tasks

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']

class NewTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewTask
        fields = "__all__"

class TasksSerializer(serializers.ModelSerializer):
    tasks = NewTaskSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Tasks
        fields = "__all__"