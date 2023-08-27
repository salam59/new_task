from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import(
    GenericViewSet,
    ModelViewSet
)
from rest_framework.mixins import(
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin
)
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    DestroyAPIView,
    RetrieveAPIView
) 
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group

from users.models import (
    CustomUser,
    Team,
    Task,
    # TeamMember,
    TaskAssignment
)
from users.serializers import (
    UserSerializer,
    TeamSerializer,
    TaskSerializer,
    # TeamMemberSerializer,
    TaskAssignmentSerializer
)
