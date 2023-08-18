from django.urls import path,include
from users.views import(
    UserView,
    TeamView,
    TaskView
)

urlpatterns = [
    path("users/",UserView.as_view(),name="users"),
    path("team/",TeamView.as_view(),name="team"),
    path("task/",TaskView.as_view(),name="task"),
]
