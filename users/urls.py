from django.urls import path,include
from users.views import(
    UserView,
    # UserDetailView,
    TeamView,
    TaskView,
    TeamDetailView,
    # TeamMemberView,
    TaskAssignmentView
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users',UserView)
router.register(r'team-details',TeamDetailView)
router.register(r'task',TaskView)
router.register(r'task-assignment',TaskAssignmentView)
# router.register(r'team-members',TeamMemberView)
urlpatterns = [
    
    # path("users/",UserView.as_view(),name="users"),
    # path("users/<int:id>/",UserDetailView.as_view(),name="users-detail"),
    path("team/",TeamView.as_view(),name="team"),
    # path("team/<int:id>/",TeamDetailView.as_view(),name="team-details"),
    # path("task/",TaskView.as_view(),name="task"),
    path("",include(router.urls))
]
