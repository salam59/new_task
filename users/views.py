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

from users.models import (
    CustomUser,
    Team,
    Task,
    # TeamMember,
    # TaskAssignment
)
from users.serializers import (
    UserSerializer,
    TeamSerializer,
    TaskSerializer,
    # TeamMemberSerializer,
    # TaskAssignmentSerializer
)
# Create your views here.

class UserView(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field ='id'
    # def get(self,request,id):
    #     user = get_object_or_404(CustomUser,id=id)
    #     serialize = UserSerializer(user,many=False)
    #     return Response(serialize.data,status=status.HTTP_200_OK)
    #     # return Response(serialize.errors)
    

    #  { POST 
    #     "first_name":"salam",
    #     "user_name": "salahuddi",
    #     "email": "salahuddi@gmail.com",
    #     "role": 1,
    #     "password": "salahuddin"
    # }
    # def post(self,request):
    #     data = request.data
    #     serialize = UserSerializer(data=data)
    #     if serialize.is_valid():
    #         serialize.save()
    #         return Response(serialize.data,status=status.HTTP_201_CREATED)
    #     return Response(serialize.errors)

# class UserDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
#     lookup_field = "id"

class TeamView(ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    lookup_field = 'id'

    
    # def get(self,request):
    #     team = Team.objects.all()
    #     serialize = TeamSerializer(team,many=True)
    #     return Response(serialize.data,status=status.HTTP_200_OK)
    
#      {POST
#         "team_name": "NewOne11",
#         "leader_id": "jk1"
# }
    def post(self,request): #if i don't use custom post new user is being created
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
            # print(serialize.data)
            serialize.save(leader_id=leader)
            return Response(serialize.data,status=status.HTTP_201_CREATED)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)
    
class TeamDetailView(GenericViewSet,RetrieveModelMixin,DestroyModelMixin):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    lookup_field = 'id'

    #NOTE: if want to update team members,can do it in it's own model, we are retrieving teammembers from model
    # FOR LEADER_ID updation(PUT REQUEST), need to define the function manually
    # because if we want to change the leader we need to get the respective leader(from USER) details
    # and then update in the Team instance,as we did in the POST method
    # (LOOK in the POST method to understand)

    def put(self,request,id):
        data = request.data
        # print(data)
        user_name = data.get("leader_id")
        leader = get_object_or_404(CustomUser,user_name=user_name,role=1)

        serialize = TeamSerializer(data=data)
        if serialize.is_valid():
            serialize.save(leader_id=leader)
            return Response(serialize.data,status=status.HTTP_201_CREATED)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,id):
        data = request.data
        # print(data)
        obj = Team.objects.get(id=id)
        user_name = data.get("leader_id")
        if user_name:
            leader = get_object_or_404(CustomUser,user_name=user_name,role=1)
            data['leader_id'] = leader
        

        serialize = TeamSerializer(obj,data=data,partial=True)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data,status=status.HTTP_201_CREATED)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)


class TaskView(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # def get(self,request):
    #     tasks = Task.objects.all()
    #     serialize = TaskSerializer(tasks,many=True)
    #     return Response(serialize.data,status=status.HTTP_200_OK)

    #post and put
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

# class TeamMemberView(ModelViewSet):
#     queryset = TeamMember.objects.all()
#     serializer_class = TeamMemberSerializer

# class TaskAssignmentView(ModelViewSet):
#     queryset = TaskAssignment.objects.all()
#     serializer_class = TaskAssignmentSerializer
    