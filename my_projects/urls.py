from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet, UserRegisterViewSet, UndeleteProjectViewSet, UndeleteTaskViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')

urlpatterns = [
    path('', include(router.urls)),
    path('register', UserRegisterViewSet.as_view({'post': 'create'}), name='register'),
    path('projects/<int:project_id>/tasks/', TaskViewSet.as_view({'post': 'create', 'get': 'list'}), name='tasks_under_project'),
    path('projects/<int:project_id>/tasks/<int:pk>/', TaskViewSet.as_view({'put': 'update', 'delete': 'destroy', 'get': 'retrieve'}), name='task_detail_under_project'),
    path('projects/<int:project_id>/undelete/', UndeleteProjectViewSet.as_view({'post': 'undelete'}), name='undelete_project'),
    path('projects/<int:project_id>/tasks/<int:task_id>/undelete/', UndeleteTaskViewSet.as_view({'post': 'undelete'}), name='undelete_task'),
]
