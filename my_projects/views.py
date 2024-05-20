from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from my_projects.models import Task, Project
from my_projects.serializers import TaskSerializer, ProjectSerializer, UserRegisterSerializer
from django.contrib.auth.models import User

class UserRegisterViewSet(viewsets.ViewSet):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'User created successfully', 'user': user}, status=status.HTTP_201_CREATED)

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class=ProjectSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user, is_deleted=False)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, members=[self.request.user])

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk):
        project = self.get_object()
        if project.created_by != request.user:
            return Response({'error': 'You are not authorized to add members to this project'}, status=status.HTTP_403_FORBIDDEN)
        project.members.add(request.data['members'])
        project.save()
        return Response()
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Task.objects.filter(project_id=project_id, project__members=self.request.user, is_deleted=False, project__is_deleted=False)

    def create(self, request, *args, **kwargs):
        project_id = kwargs['project_id']
        try:
            project = Project.objects.get(id=project_id)
            if project.members.filter(id=request.user.id).exists():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(created_by=request.user, project=project)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'error': 'You are not a member of this project'}, status=status.HTTP_403_FORBIDDEN)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        project_id = kwargs['project_id']
        task_id = kwargs['pk']
        try:
            task = Task.objects.get(id=task_id, project_id=project_id)
            if task.project.members.filter(id=request.user.id).exists():
                serializer = self.get_serializer(task, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            return Response({'error': 'You are not a member of this project'}, status=status.HTTP_403_FORBIDDEN)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class UndeleteProjectViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def undelete(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id, is_deleted=True)
            if project:
                project.is_deleted = False
                project.save()
                return Response({'message': 'Project undeleted successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class UndeleteTaskViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def undelete(self, request, project_id, task_id):
        try:
            project = Project.objects.get(id=project_id, is_deleted=False)
            if project:
                task = Task.objects.get(id=task_id, project=project, is_deleted=True)
                if task:
                    task.is_deleted = False
                    task.save()
                    return Response({'message': 'Task undeleted successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
