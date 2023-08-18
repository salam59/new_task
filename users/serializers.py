from rest_framework import serializers

from users.models import (
    CustomUser,
    Team,
    Task
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = ['email','user_name','role','first_name','password']
        exclude = ('password','last_login','first_name','last_name','is_staff','is_active','is_superuser')
    
    def validate(self,data):
        email = data['email']
        user_name = data['user_name']

        if CustomUser.objects.filter(user_name=user_name).exists():
            raise serializers.ValidationError("username exists")
        
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("email exists")
        return data
    
    def create(self, validated_data):
        user = CustomUser.objects.create(user_name=validated_data['user_name'],email=validated_data['email'],role=validated_data['role'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data

class TeamSerializer(serializers.ModelSerializer):
    leader_id = UserSerializer(read_only=True)
    class Meta:
        model = Team
        fields = '__all__'

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
    class Meta:
        model = Task
        fields = ['task_name','team_id','status']
    def validate(self, attrs):
        team_id = attrs['team_id']
        if not CustomUser.objects.filter(id=team_id).exists():
            raise serializers.ValidationError("User doesn't exist")
        return attrs
    
