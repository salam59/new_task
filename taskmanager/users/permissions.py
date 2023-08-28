from rest_framework import permissions

#GROUPS

class userPermissions(permissions.BasePermission):
    pass
    # def allPermissions(self,request)

class managerPermission(permissions.BasePermission):
    def has_permission(self,request,view):
        # print(request.user.groups.filter(name='Managers').exists())
        return request.user.groups.filter(name='Managers').exists()
        # return False

class leaderUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        print("ok")
        return request.user.groups.filter(name='Team Leaders').exists() and view.action!='create'
    def has_object_permission(self, request, view, obj):
        print("object")
        if request.user.groups.filter(name='Team Leaders').exists():
            print(1)
            if view.action in ['retrieve','update','partial_update','destroy']:
                print(4)
                if request.user == obj:
                    print(5)
                    return True
                return False
                
        return False
                    
        # print("object")
        # return request.user == obj and request.user.groups.filter(name='Team Leaders').exists()

class leaderTeamPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Team Leaders').exists() and view.action != 'create'
    def has_object_permission(self, request, view, obj):
        print("object")
        if request.user.groups.filter(name='Team Leaders').exists():
            print(1)
            # if view.action == 'create':
            #     print(2)
            #     return False
            if view.action in ['destroy'] :
                print(3)
                return False
            elif view.action == 'list':
                print(4)
                return True
            elif view.action in ['retrieve','update','partial_update']:
                print(5)
                if request.user == obj.leader_id:
                    if view.action == 'retrieve':
                        return True
                    else:
                        if 'leader_id' not in request.data:
                            return True
                        return False
                return False
        return False

        #     if request.user == obj.leader_id and 'leader_id' not in request.data:
        #         return True
        #     return False
        # return request.user == obj and request.user.groups.filter(name='Team Leaders').exists()
    
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