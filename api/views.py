from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer,NewTaskSerializer,TasksSerializer
from django.contrib.auth.models import User
from .models import NewTask,Tasks

@api_view(['POST'])
def create_user(request):
    if request.method=="POST":
        user=request.data
        serializer=UserSerializer(data=user)
        if serializer.is_valid():
            _user=serializer.save()
            Tasks.objects.create(owner=_user)
            return Response({"msg":"User created","user":serializer.data},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def get_all_users(request):
    if request.method=="GET":
        user=User.objects.all()
        serializer=UserSerializer(user,many=True)
        if user:
            return Response({"msg":"Retrieved all users","users":serializer.data},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=="POST":
        try:
            _,_=request.data["username"],request.data["password"]
        except:
            return Response({"msg":f"Not enough data provided (username,password)"},status=status.HTTP_400_BAD_REQUEST)
        try:
            user=User.objects.get(username=request.data['username'])
        except:
            return Response({"msg":"User not found"},status=status.HTTP_200_OK)
        if user.password==request.data['password']:
            serializer=UserSerializer(user)
            if user:
                return Response({"msg":f"Retrieved user: {request.data['username']}","user":serializer.data},status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg":f"Passwords dont match"},status=status.HTTP_200_OK)

@api_view(["POST"])
def update_user(request):
    if request.method=="POST":
        data=request.data
        user=User.objects.get(username=data['username'])
        serializer=UserSerializer(user,data=data)
        if user.password==data['password']:
            if serializer.is_valid():
                serializer.save()
                return Response({"msg":f"Updated user"},status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg":"Passwords dont match"},status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def delete_user(request):
    if request.method=="POST":
        data=request.data
        user=User.objects.get(username=data['username'])
        if user.password==data['password']:
            user.delete()
            return Response({"msg":f"Deleted user"},status=status.HTTP_200_OK)
        return Response({"msg":"Passwords dont match"},status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def create_task(request):
    if request.method == "POST":
        owner = request.data.get("owner")
        data = request.data
        data.pop("owner")
        task_serializer = NewTaskSerializer(data=data)
        if task_serializer.is_valid():
            new_task = task_serializer.save()
            try:
                user_instance = User.objects.get(username=owner)
                tasks_instance, created = Tasks.objects.get_or_create(owner=user_instance)
                tasks_instance.tasks.add(new_task)
                return Response({"msg": "Task created and added to user's task list", "task": task_serializer.data}, status=status.HTTP_201_CREATED)
            
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def get_tasks(request):
    if request.method == "POST":
        owner=User.objects.get(username=request.data["owner"])
        _task=Tasks.objects.get(owner=owner)
        task=TasksSerializer(_task)

        return Response({"task":task.data},status=status.HTTP_200_OK)
    return Response({"msg":"Invalid method POST"},status=status.HTTP_400_BAD_REQUEST)

# @api_view(["POST"])
# def update_tasks(request):
