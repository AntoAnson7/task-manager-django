from unicodedata import name
from webbrowser import get
from django.contrib import admin
from django.urls import path,include
from .views import create_user,get_all_users, get_tasks,update_user,delete_user,create_task,get_tasks

urlpatterns = [
    path('user/create/', create_user,name="create_user"),
    path('user/get/', get_all_users,name="get_all_users"),
    path('user/update/', update_user,name="update_user"),
    path('user/delete/', delete_user,name="delete_user"),

    # tasks
    path('tasks/create/', create_task,name="create_task"),
    path('tasks/get/', get_tasks,name="get_tasks"),
]