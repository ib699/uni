from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import User, Workspace, Task, SubTask, UserWorkspaceRole
from .serializers import UserSerializer, WorkspaceSerializer, TaskSerializer, SubTaskSerializer, \
    UserWorkspaceRoleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated]


class UserWorkspaceRoleViewSet(viewsets.ModelViewSet):
    queryset = UserWorkspaceRole.objects.all()
    serializer_class = UserWorkspaceRoleSerializer
    permission_classes = [IsAuthenticated]
