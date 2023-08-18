from django.urls import path,include
from users.views import(
    UserView,
    TeamView
)

urlpatterns = [
    path("users/",UserView.as_view(),name="users"),
    path("team/",TeamView.as_view(),name="team"),
]
