from django.contrib import admin
from django.contrib.auth.models import User
from .models import Tasks,NewTask

admin.site.register(NewTask)
admin.site.register(Tasks)