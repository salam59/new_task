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
    leader_id = UserSerializer()
    class Meta:
        model = Team
        fields = '__all__'
    def validate(self, attrs):
        team_id = attrs['leader_id']
        if not CustomUser.objects.filter(id=team_id).exists():
            raise serializers.ValidationError("User doesn't exist")
        return attrs

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['task_name','team_id','status']
    def validate(self, attrs):
        team_id = attrs['team_id']
        if not CustomUser.objects.filter(id=team_id).exists():
            raise serializers.ValidationError("User doesn't exist")
        return attrs
    
