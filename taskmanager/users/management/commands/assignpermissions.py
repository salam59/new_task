from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from users import models

user_content_type = ContentType.objects.get_for_model(models.CustomUser)
team_content_type = ContentType.objects.get_for_model(models.Team)
task_content_type = ContentType.objects.get_for_model(models.Task)

user_permissions = Permission.objects.filter(content_type=user_content_type)
team_permissions = Permission.objects.filter(content_type=team_content_type)
task_permissions = Permission.objects.filter(content_type=task_content_type)

def manager_permissions():
    print("manager")
    group = Group.objects.get(name="Managers")
    for content_permissions in [user_permissions,team_permissions,task_permissions]:
        for permission in content_permissions:
            group.permissions.add(permission)
    group.save()

def leader_permissions():
    print("leader")
    permissions = ['view_customuser','view_team','view_task','change_task','add_teammember','change_teammember','delete_teammember']
    group = Group.objects.get(name="Team Leaders")
    for permission in permissions:
        print(permission)
        group.permissions.add(Permission.objects.get(codename=permission))
    group.save()

def member_permissions():
    print("member")
    permissions = ['view_customuser','view_team','view_task']
    group = Group.objects.get(name="Team Members")
    for permission in permissions:
        group.permissions.add(Permission.objects.get(codename=permission))
    group.save()

class Command(BaseCommand):
    help = 'Creates initial permissions to groups'

    def handle(self, *args, **options):
        # group_names = ['Managers', 'Team Leaders', 'Team Members']
        # for group_name in group_names:
        #     group, created = Group.objects.get_or_create(name=group_name)
        #     if created:
        manager_permissions()
        leader_permissions()
        member_permissions()
        self.stdout.write(self.style.SUCCESS(f"Permissions created."))

