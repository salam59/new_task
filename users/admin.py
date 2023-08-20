from django.contrib import admin
from users.models import(
    CustomUser,
    Team,
    Task,
    TeamMember,
    TaskAssignment
)

class TeamAdmin(admin.ModelAdmin):
    search_fields = ['team_name']
    fields = ["team_name","leader_id"]
    list_display = ["team_name","leader_id"]
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    search_fields=['email','user_name']
    fields = ['first_name','user_name',"email","password","role"]
    list_display= ['id','first_name',"email","role"]

class TaskAdmin(admin.ModelAdmin):
    search_fields = ['task_name','team_id']
    fields = ['task_name','team_id','status','completed_at']
    list_display = ['id','task_name','team_id','status']

class TeamMemberAdmin(admin.ModelAdmin):
    search_fields = ['team_id','user_id']
    fields = ['team_id','user_id']
    list_display = ['id','team_id','user_id']

class TaskAssignmentAdmin(admin.ModelAdmin):
    list_display = ['task_id','member_id']

admin.site.register(CustomUser,UserAdmin)
admin.site.register(Team,TeamAdmin)
admin.site.register(Task,TaskAdmin)
admin.site.register(TeamMember,TeamMemberAdmin)
admin.site.register(TaskAssignment,TaskAssignmentAdmin)