from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.models import (
    CustomUser,
    Team,
)
from users.serializers import (
    UserSerializer,
    TeamSerializer,
)
# Create your views here.

class UserView(APIView):

    def get(self,request):
        users = CustomUser.objects.all()
        serialize = UserSerializer(users,many=True)
        return Response(serialize.data,status=status.HTTP_200_OK)
        # return Response(serialize.errors)
    
    def post(self,request):
        data = request.data
        serialize = UserSerializer(data=data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data,status=status.HTTP_201_CREATED)
        return Response(serialize.errors)

class TeamView(APIView):
    def get(self,request):
        team = Team.objects.all()
        serialize = TeamSerializer(team,many=True)
        return Response(serialize.data,status=status.HTTP_200_OK)
    def post(self,request):
        data = request.data
        serialize = TeamSerializer(data=data)
        if serialize.is_valid():
            user_name = data.get("leader")
            leader = CustomUser.objects.get(user_name=user_name)
            instance = serialize.save(leader_id=leader)
            return Response(serialize.data,status=status.HTTP_201_CREATED)
        return Response(serialize.errors)