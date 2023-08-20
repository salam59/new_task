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
    
    # def validate(self,data):
    #     email = data['email']
    #     user_name = data['user_name']
    #     if CustomUser.objects.filter(user_name=user_name).exists():
    #         raise serializers.ValidationError("username exists")
        
    #     if CustomUser.objects.filter(email=email).exists():
    #         raise serializers.ValidationError("email exists")
    #     return data
    
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
    # extra_data = serializers.CharField(write_only=True)
    class Meta:
        model = Team
        fields = '__all__'

    def get_team_members(self,obj):
        team_id = obj.id
        query_list = TeamMember.objects.filter(team_id=team_id)
       
        res=[]
        for member in query_list:
            res.append(UserSerializer(member.user_id).data)
        return res

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

    def create(self, validated_data):
        team_members = self.initial_data.get("team_members") #list of ids of users
        print(team_members)
        team = Team.objects.create(**validated_data)
        for member in team_members:
            member_data = CustomUser.objects.get(id=member)
            TeamMember.objects.create(team_id=team,user_id=member_data)
        return team
    

        

class TaskSerializer(serializers.ModelSerializer):
    team_members = serializers.SerializerMethodField()
    
    # started_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Task
        fields = ['task_name','team_id','team_members']
    def validate(self, attrs):
        if "team_id" in attrs: # for Patch to work, we may not send team_id during patch
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
    

    #NOTE: FOR BOTH CREATE AND UPDATE
    #remove,add users as team members, check if the user is actually part of team if want to add CASE-1
    #for remove if the user is there as member just delete if not present just ignore CASE-2
    def create(self,data):
        task = Task.objects.create(**data)
        # below part is adding the users as team members to the TeamMember Model
        assignments = self.initial_data.get('assignments') #user ids posted as IDs
        team_id = data.get("team_id")
        team_members = TeamMember.objects.filter(team_id=team_id)
        team_members_user_ids = [member.user_id.id for member in team_members]
        # print(team_members_user_ids,team_id)
        for member_id in assignments:
            # print(member_id)
            if member_id in team_members_user_ids:
                member_obj = CustomUser.objects.get(id=member_id)
                TaskAssignment.objects.create(task_id = task,member_id=member_obj)
            else:
                raise serializers.ValidationError(f"{member_id} is  not part of team {team_id}")
        # task = Task.objects.create(**data)
        return task
   
    def update(self, instance, validated_data):
        instance.task_name = validated_data.get("task_name",instance.task_name)
        instance.team_id = validated_data.get("team_id",instance.task_name)
        instance.status = validated_data.get("status",instance.status)
        remove_users = self.initial_data.get("assignments-remove")
        add_users = self.initial_data.get( "assignments-add")
        print(remove_users)
        print(add_users)

        #Getting all the taskassignments of the current task
        task_assignments = TaskAssignment.objects.filter(task_id = instance.id )
        #Removal
        # remove if the user is there as member just delete if not present just ignore CASE-2
        if remove_users:
            for assignments in task_assignments:
                if assignments.member_id.id in remove_users:
                    assignments.delete()
        #addition
        #add users as team members, check if the user is actually part of team if want to add CASE-1
        if add_users:
            team_id = validated_data.get("team_id")
            team_members = TeamMember.objects.filter(team_id=team_id)
            team_members_user_ids = [member.user_id.id for member in team_members]
            # print(team_members_user_ids,team_id)
            for member_id in add_users:
                # print(member_id)
                if member_id in team_members_user_ids:
                    member_obj = CustomUser.objects.get(id=member_id)
                    TaskAssignment.objects.create(task_id = instance,member_id=member_obj)
                else:
                    raise serializers.ValidationError(f"{member_id} is  not part of team {team_id}")
        instance.save()
        return instance
    
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
    
# class TeamMemberSerializer(serializers.Serializer):
#     class Meta:
#         model = TeamMember
#         fields = "__all__"

# class TaskAssignmentSerializer(serializers.Serializer):
#     class Meta:
#         model = TaskAssignment
#         fields= ['task_id','member_id']  

# If the TeamMember and TaskAssignment models primarily hold references to other models through foreign key relationships,
# and their data can be updated or created based on the IDs of existing models, you can indeed manage with custom create 
# and update methods within the TeamSerializer and TaskSerializer. This approach can be particularly useful when the serialized data is straightforward
# and doesn't require complex transformation.