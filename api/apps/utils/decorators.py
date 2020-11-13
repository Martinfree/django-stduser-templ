from rest_framework import status
from rest_framework.response import Response
from apps.utils.permissions import (IsAuthenticated,
                                    _IsAuthenticated,
                                    IsAdminUser,
                                    IsModeratorUser,
                                    IsStaffUser,
                                    IsUser,
                                    IsOwner,
                                    IsTeacher,
                                    IsStudent)

from apps.utils.functions import get_user_dec

P = {'_IsAuthenticated': _IsAuthenticated,
    'IsAdminUser': IsAdminUser,
    'IsAuthenticated':IsAuthenticated,
    'IsTeacher': IsTeacher,
    'IsStudent': IsStudent,
    'IsModeratorUser': IsModeratorUser,
    'IsStaffUser': IsStaffUser,
    'IsUser': IsUser,
    'IsOwner':IsOwner,}

FOO = {'IntNews': '',
       'Calendar': '',
       'Labour':  '',
       'Activity': '',
       'Partner': '',
       'Summary': '',
       'Images': '',}

# decorator for get access to request by extraneous
def permission(permission):
    def perm(func):
        def p(request, args, **kwargs):
            permis = P.get(permission)
            if (permis.has_permission(get_user_dec(value="email",arg=args.user))) is True:
                return func(request, args, **kwargs)
            else:
                return Response({'Status': 'User has no permissions'})
        return p
    return perm

# decorator for multiple rights
def permissions(permissions,argument):
    def perm(func):
        def p(request, args, **kwargs):
            for permission in permissions:
                if (permission == "IsAdminUser") or (permission == "IsModeratorUser") or (permission == "IsStaffUser"):
                    permis = P.get(permission)
                    user=get_user_dec(value="email", arg=args.user)
                    if permis.has_permission(user) is True:
                        return func(request, args, **kwargs)
                elif (permission == "IsUser"):
                    permis = P.get(permission)
                    if argument == "args":
                        user=get_user_dec(value="id",arg=args.data.get('id'))
                        if user == None:
                            return Response(status=status.HTTP_404_NOT_FOUND)
                        if permis.has_object_permission(get_user_dec(value="email",arg=args.user), user) is True:
                            return func(request, args,**kwargs)
                        else:
                            return Response({'Status': 'User has no permissions'},status=status.HTTP_403_FORBIDDEN)
                    elif argument == "kwargs":
                        user=get_user_dec(value="id",arg=kwargs.get('id'))
                        if user == None:
                            return Response(status=status.HTTP_404_NOT_FOUND)
                        if permis.has_object_permission(get_user_dec(value="email",arg=args.user), user) is True:
                            return func(request, args, **kwargs)
                        else:
                            return Response({'Status': 'User has no permissions'},status=status.HTTP_403_FORBIDDEN)
                elif (permission == "IsTeacher"):
                    permis = P.get(permission)
                    if permis.has_permission(get_user_dec(value="email",arg=args.user)) is True:
                        return func(request, args,**kwargs)
                    else:
                        return Response({'Status': 'User has no permissions'},status=status.HTTP_403_FORBIDDEN)
                elif (permission == "IsStudent"):
                    permis = P.get(permission)
                    if permis.has_permission(get_user_dec(value="email",arg=args.user)) is True:
                        return func(request, args,**kwargs)
                    else:
                        return Response({'Status': 'User has no permissions'},status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response({"Status":"No such request"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return p
    return perm

# decorator for owner
def IsOwnerPerm(permissions, argument, mod):
    def perm(func):
        def p(request, args, **kwargs):
            for permission in permissions:
                if (permission == "IsAdminUser") or (permission == "IsModeratorUser") or (permission == "IsStaffUser"):
                    permis = P.get(permission)
                    if permis.has_permission(get_user_dec(value="email",arg=args.user)):
                        return func(request, args, **kwargs)
                elif(permission == "IsOwner"):
                    permis = P.get(permission)
                    object = FOO.get(mod)
                    if argument == "kwargs":
                        if permis.has_owner_permission(args.user, object(value="id",arg=kwargs.get('id'))) or permis.has_owner_permission(args.user, object(value="author_user", arg=kwargs.get('author_user'), request=request)):
                            return func(request, args, **kwargs)
                        else:
                            return Response({'Status': 'User has no permissions'},status=status.HTTP_403_FORBIDDEN)
                    elif argument == "args":
                        if permis.has_owner_permission(args.user, object(value="id",arg=args.data.get('id'), request=request)) or permis.has_owner_permission(args.user, object(value="author_user", arg=kwargs.get('author_user'), request=request)):
                            return func(request, args, **kwargs)
                        else:
                            return Response({'Status': 'User has no permissions'},status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response({"Status": "No such request"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return p
    return perm
