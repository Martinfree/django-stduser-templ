from rest_framework.permissions import BasePermission


class AllowAny(BasePermission):
    """
    Allow any access.
    This isn't strictly required, since you could use an empty
    permission_classes list, but it's useful because it makes the intention
    more explicit.
    """

    def has_permission(self, request, view):
        return True

class _IsAuthenticated:
    """
    Allows access only to authenticated users.
    """

    def has_permission(user):
        if user == None:
            return False
        else:
            return bool(user and user.is_active)


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self,request,view):
        if request.user == None:
            return False
        else:
            return bool(request.user and request.user.is_active)

class IsTeacher:
    """
    Allows access only to authenticated users.
    """

    def has_permission(user):
        if user == None:
            return False
        else:
            return bool(user and user.is_teacher)

class IsStudent:
    """
    Allows access only to authenticated users.
    """

    def has_permission(user):
        if user == None:
            return False
        else:
            return bool(user and user.is_student)

class IsAdminUser:

    def has_permission(user):
        if user == None:
            return False
        else:
            return bool(user and user.is_admin)


class IsStaffUser:

    def has_permission(user):
        if user == None:
            return False
        if (user.is_admin == True) or (user.is_moderator == True):
            return True
        else:
            return False


class IsModeratorUser:
    """
    Allows access only to moderator users.
    """

    def has_permission(user):
        if user == None:
            return False
        else:
            return bool(user and user.is_moderator)


class IsUser:

    def has_object_permission(user, obj):
        if user == None:
            return False
        elif obj== None:
            return False
        elif (user.is_authenticated == True) and (user.id == obj.id):
            return True
        else:
            return False


class IsOwner:

    def has_owner_permission(user, obj):
        if user == None:
            return False
        elif user.is_teacher == True:
            return True
        else:
            return False
        if user == obj.author_user:
            return True
        else:
            return False
        if user.email == obj.author_user:
            return True
        elif user.email == obj.user:
            return True
        else:
            return False
        if user.email == obj.student:
            return True
        else:
            return False

class DisablePermission(BasePermission):
    """
    Global permission to disallow all requests for methods OPTIONS and HEAD.
    """

    def has_permission(self, request, view):
        if request.method == 'OPTIONS' or request.method == 'HEAD':
            return False
        return True
