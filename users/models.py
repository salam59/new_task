from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Q
# Create your models here.

class CustomAccountManager(BaseUserManager):

    def create_user(self,user_name,email,password,role,**other_fields):
        if not email:
            raise ValueError(('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(user_name=user_name,email=email, 
                        role=role,**other_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,user_name,email,password,role,**other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
            # if other_fields.get('is_staff') is not True:
            #     raise ValueError(
            #         'Superuser must be assigned to is_staff=True.')
            # if other_fields.get('is_superuser') is not True:
            #     raise ValueError(
            #         'Superuser must be assigned to is_superuser=True.')

            # if other_fields.get('is_superuser') is not True:
            #     raise ValueError(
            #         'Superuser must be assigned to is_superuser=True.')
        return self.create_user(user_name,email,password,role, **other_fields)
    
role_choices = [
        ('0','TeamMember'),
        ('1','TeamLeader'),
        ('2','Manager')
    ]
status_choices = [
    (1,'Created'),
    (2,'Assigned'),
    (3,'In Progress'),
    (4,'Under review'),
    (5,'Done')
]
class User(AbstractBaseUser):

    user_name = models.CharField(max_length=50,unique=True,blank=False)
    email = models.EmailField(verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=50,blank=True)
    last_name = models.CharField(max_length=50,blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    role = models.IntegerField(
        role_choices,
        default=0
    )
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email',"role"]

    objects = CustomAccountManager()

    def __str__(self):
        return f"{self.first_name}-->{self.email}"
    
    def has_module_perms(self,app):
        return True
    def has_perm(self,app):
        return True
    
class Team(models.Model):
    team_name = models.CharField(max_length=50,blank=False,unique=True)
    # one user can lead one team assumption
    leader_id = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'role':'1'})
    class Meta:
        unique_together = ("team_name","leader_id")

class Task(models.Model):
    task_name = models.CharField(max_length=50,blank=False)
    team_id = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True,related_name='tasks')
    status = models.IntegerField(status_choices,default=1)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True,blank=True)
    @property
    def is_completed(self):
        return self.status == 5
    
    def save(self, *args, **kwargs):
        if self.status == 5 and not self.completed_at:
            self.completed_at = timezone.now()
        elif self.status != 5 :
            self.completed_at = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.task_name

class TeamMember(models.Model):
    team_id = models.ForeignKey(Team,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to=Q(role__in=['0','1']))
    class Meta:
        unique_together = ("team_id","user_id")
    
    def __str__(self):
        return self.user_id.first_name
    #  two fields together form a unique combination by using the unique_together 
    # option within the model's Meta class.
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=["team_id","user_id"], name='unique__teamid_userid')
    #     ]
class TaskAssignment(models.Model):
    task_id = models.ForeignKey(Task,on_delete=models.CASCADE)
    member_id = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        unique_together = ("task_id","member_id")
    #     constraints = [
    #         models.UniqueConstraint(fields=["task_id","member_id"], name='unique__taskid_userid')
    #     ]

