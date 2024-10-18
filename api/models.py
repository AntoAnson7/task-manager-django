from django.db import models
from django.contrib.auth.models import User

class NewTask(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=250)
    priority = models.CharField(max_length=50,choices=[('low','Low Priority'),('mid','Medium Priority'),('high','High Priority')])
    status = models.CharField(max_length=50,choices=[('completed','Completed'),('in_progress','In Progress'),('pending','Pending')])
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.name

class Tasks(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    tasks = models.ManyToManyField(NewTask, related_name='task_lists',blank=True)

    def __str__(self):
        return f"Tasks of {self.owner.username}"
