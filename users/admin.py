from django.contrib import admin
from users.models import(
    User,
    Team,
    Task,
    TeamMember
)

class TeamAdmin(admin.ModelAdmin):
    search_fields = ['team_name']
    fields = ["team_name","leader_id"]
    list_display = ["team_name","leader_id"]
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    search_fields=['email','user_name']
    fields = ['first_name','user_name',"email","password","role"]
    list_display= ['first_name',"email","role"]

class TaskAdmin(admin.ModelAdmin):
    search_fields = ['task_name','team_id']
    fields = ['task_name','team_id','status','completed_at']
    list_display = ['task_name','team_id','status']
    
admin.site.register(User,UserAdmin)
admin.site.register(Team,TeamAdmin)
admin.site.register(Task,TaskAdmin)
admin.site.register(TeamMember)