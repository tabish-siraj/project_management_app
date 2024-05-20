from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_by = models.ForeignKey(User, related_name='created_projects', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='projects')
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
    

class Task(models.Model):
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    created_by = models.ForeignKey(User, related_name='created_tasks', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title