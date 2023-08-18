from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView
) 
from django.shortcuts import get_object_or_404

from users.models import (
    CustomUser,
    Team,
    Task
)
from users.serializers import (
    UserSerializer,
    TeamSerializer,
    TaskSerializer
)
# Create your views here.

class UserView(APIView):

    def get(self,request):
        users = CustomUser.objects.all()
        serialize = UserSerializer(users,many=True)
        return Response(serialize.data,status=status.HTTP_200_OK)
        # return Response(serialize.errors)
    

    #  { POST 
    #     "first_name":"salam",
    #     "user_name": "salahuddi",
    #     "email": "salahuddi@gmail.com",
    #     "role": 1,
    #     "password": "salahuddin"
    # }
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
    
#      {POST
#         "team_name": "NewOne11",
#         "leader_id": "jk1"
# }
    def post(self,request):
        data = request.data
        leader_user_name = data.get('leader_id')
        leader = get_object_or_404(CustomUser,user_name=leader_user_name,role=1)
        # try:
        #     leader = CustomUser.objects.get(user_name=leader_user_name,role=1)
        #     print(leader.user_name)
        # except CustomUser.DoesNotExist:
        #     return Response({"error: User not found"},status=status.HTTP_400_BAD_REQUEST)

         # Remove the leader_id from the data dictionary before passing to serializer
        # data.pop('leader_id', None)
        serialize = TeamSerializer(data=data)
        if serialize.is_valid():
            # user_name = data.get("leader")
            # leader = CustomUser.objects.get(user_name=user_name)
            serialize.save(leader_id=leader)
            return Response(serialize.data,status=status.HTTP_201_CREATED)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)
    
class TaskView(ListAPIView,CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # def get(self,request):
    #     tasks = Task.objects.all()
    #     serialize = TaskSerializer(tasks,many=True)
    #     return Response(serialize.data,status=status.HTTP_200_OK)
    
# {
#     "task_name": "task-manager-api-2",
#     "team_id":8
# }
    # def post(self,request):
    #     data = request.data
    #     serialize = TaskSerializer(data=data)
    #     # print(serialize.data)
    #     if serialize.is_valid():
    #         serialize.save()
    #         return Response(serialize.data)
    #     return Response(serialize.errors)