from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_by = models.ForeignKey(User, related_name='created_projects', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, through='ProjectMember')
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
    
class ProjectMember(models.Model):
    ROLE_OPTIONS = (
        ('read', 'Read'),
        ('write', 'Read & Write'),
    )

    project = models.ForeignKey(Project, related_name='members', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='project_members', on_delete=models.CASCADE)
    role = models.CharField(max_length=5, choices=ROLE_OPTIONS)

    def __str__(self) -> str:
        return f'{self.user.username} - {self.project.name}'