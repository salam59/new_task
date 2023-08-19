from rest_framework import serializers

from users.models import (
    CustomUser,
    Team,
    Task,
    TeamMember,
    TaskAssignment
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'user_name', 'role', 'first_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

        # exclude = (,'last_login','first_name','last_name','is_staff','is_active','is_superuser')
    
    def validate(self,data):
        email = data['email']
        user_name = data['user_name']
        if CustomUser.objects.filter(user_name=user_name).exists():
            raise serializers.ValidationError("username exists")
        
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("email exists")
        return data
    
    def create(self, validated_data):
        first_name = validated_data.get("first_name")
        password = validated_data.get("password")
        user = CustomUser.objects.create(first_name=first_name,user_name=validated_data['user_name'],email=validated_data['email'],role=validated_data['role'])
        user.set_password(password)
        user.save()
        return validated_data
    
    def update(self,instance,validated_data):
        password = validated_data.get("password")
        print(password)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.user_name = validated_data.get('user_name', instance.user_name)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        
        if password:
            instance.set_password(password)
            instance.save()
            print("worked")
        return instance

class TeamSerializer(serializers.ModelSerializer):
    leader_id = UserSerializer(read_only=True)
    team_members = serializers.SerializerMethodField()
    class Meta:
        model = Team
        fields = '__all__'

    def get_team_members(self,obj):
        team_id = obj.id
        query_list = TeamMember.objects.filter(team_id=team_id)
        # print(query_list.values('user_id'))
        # print(query_list)

        res=[]
        for member in query_list:
            res.append(UserSerializer(member.user_id).data)
        return res
        # users = CustomUser.objects.filter(user_id=member.user_id)
        # serialize = UserSerializer(users,many=True)

        # #     serialize = UserSerializer(user)
        # #     if serialize.is_valid():
        # #         result.append(serialize.data)
        # # return result


    def validate_leader_id(self,value):
        leader = None
        try:
            leader = CustomUser.objects.get(user_name=value)
        except:
            raise serializers.ValidationError("User doesn't exist")
        
        if leader.role != 1:
            raise serializers.ValidationError("User is not a Team leader")
        
        return leader
    # def validate(self, validated_data):
    #     leader = validated_data.pop('leader_id')

    #     # if not CustomUser.objects.filter(id=team_id).exists():
    #     #     raise serializers.ValidationError("User doesn't exist")

    #     team = Team.objects.create(leader_id=leader,**validated_data)
    #     return team

class TaskSerializer(serializers.ModelSerializer):
    team_members = serializers.SerializerMethodField()
    
    # started_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Task
        fields = ['task_name','team_id','team_members']
    def validate(self, attrs):
        team_id = attrs['team_id'].id #DON'T KNOW WHY BUT GETTING OBJECT INSTEAD OF ID SO IMPROVISED
        if not Team.objects.filter(id=team_id).exists():
            raise serializers.ValidationError("User doesn't exist")
        return attrs
    
    def get_team_members(self,obj):
        task_id = obj.id
        query_list = TaskAssignment.objects.filter(task_id=task_id)
        # print(query_list.values('user_id'))
        # print(query_list)

        res=[]
        for member in query_list:
            res.append(UserSerializer(member.member_id).data)
        return res
    
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['team_id'] = instance.team_id.id  # Serialize the team_id as an integer
    #     return representation

    # def to_internal_value(self, data):
    #     if 'team_id' in data and isinstance(data['team_id'], str):
    #         try:
    #             data['team_id'] = int(data['team_id'])  # Ensure team_id is parsed as an integer
    #         except ValueError:
    #             pass
    #     return super().to_internal_value(data)
    
