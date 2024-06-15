from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, WorkspaceViewSet, TaskViewSet, SubTaskViewSet, UserWorkspaceRoleViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'workspaces', WorkspaceViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'subtasks', SubTaskViewSet)
router.register(r'user-workspace-roles', UserWorkspaceRoleViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/signup/', UserViewSet.as_view({'post': 'create'}), name='signup'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
