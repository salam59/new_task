from django.urls import path,include
from users.views import(
    UserView,
    # UserDetailView,
    TeamView,
    TaskView,
    TeamDetailView
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users',UserView)
router.register(r'team-details',TeamDetailView)
urlpatterns = [
    
    # path("users/",UserView.as_view(),name="users"),
    # path("users/<int:id>/",UserDetailView.as_view(),name="users-detail"),
    path("team/",TeamView.as_view(),name="team"),
    # path("team/<int:id>/",TeamDetailView.as_view(),name="team-details"),
    path("task/",TaskView.as_view(),name="task"),
    path("",include(router.urls))
]
