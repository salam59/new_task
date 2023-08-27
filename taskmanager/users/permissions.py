from rest_framework import permissions

#GROUPS

class userPermissions(permissions.BasePermission):
    pass
    # def allPermissions(self,request)

class managerPermission(permissions.BasePermission):
    def has_permission(self,request,view):
        print(request.user.groups.filter(name='Managers').exists())
        return request.user.groups.filter(name='Managers').exists()
        # return False


class canUpdateTeam(permissions.BasePermission):

    def has_object_permission(self,request,view,obj):
        if request.user.is_authenticated:
            print("------")
            print(obj.leader_id)
            print(request.user)
            print("------")
            if request.user.role == 1 and obj.leader_id == request.user and 'leader_id' not in request.data:
                return True
        return False