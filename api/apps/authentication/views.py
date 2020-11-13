import json
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import status
from rest_framework.views import APIView

from rest_framework.generics import (ListAPIView,
                                     DestroyAPIView,
                                     CreateAPIView)
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from django.conf import settings

from apps.authentication.serializers import (
    UserSerializer,CreateUserSerializer,
    UpdateUserSerializer,VerifyUserSerializer,
    VerifyUserPassSerializer,BulkUpdateUserSerializer,
    DeleteAllSerializer,RecoverySerializer,
    SetModeratorSerializer,NewsSubscriptionSerializer,
    AdminDeleteUserSerializer,AdminUserSerializer,
    SocialAuthSerializer,UsersBulkCreateSerializer,
    SetActiveSerializer)

from apps.authentication.models import StdUser, SocialUser
from apps.utils.permissions import (AllowAny, IsUser, _IsAuthenticated,
                                    IsAuthenticated, DisablePermission,)
from apps.utils.decorators import permission, permissions
from apps.utils.functions import get_user

User = get_user_model()


class SocialAuthAPIView(APIView):
    permission_classes = [AllowAny, DisablePermission]
    queryset = SocialUser.objects.none()
    serializer_class = SocialAuthSerializer

    def post(self, request, *args, **kwargs):
        try:
            SocialUser.objects.get(id=request.data.get('id'))
            return Response(status=status.HTTP_200_OK)
        except SocialUser.DoesNotExist:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(ListAPIView, ListModelMixin, DestroyAPIView):
    lookup_field = 'id'
    serializer_class = UserSerializer
    permission_classes = [AllowAny, DisablePermission]
    queryset = User.objects.none()

    # @permissions(["IsAdminUser", "IsUser"],"kwargs")
    def get(self, request, *args, **kwargs):
        queryset = get_user(value="id",arg=kwargs.get('id'),request=request)

        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # @permissions(["IsAdminUser", "IsUser"],"kwargs")
    def put(self, request, *args, **kwargs):
        queryset = get_user(value="id",arg=kwargs.get('id'), request=request)
        requester = request.user

        if queryset==None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if IsUser.has_object_permission(requester,queryset)==True:
            self.serializer_class = UpdateUserSerializer
            serializer = self.serializer_class(queryset,  data=request.data)
            if(serializer.is_valid()):
                serializer.update(instance=queryset, validated_data = request.data,id=request.user.id)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif requester.is_admin == True:
            self.serializer_class = AdminUserSerializer
            serializer = self.serializer_class(queryset,  data=request.data)

            if(serializer.is_valid()):
                serializer.update(instance=queryset, validated_data = request.data)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @permissions(["IsAdminUser", "IsUser"],"kwargs")
    def delete(self, request, *args, **kwargs):
        user = get_user(value="id",arg=kwargs.get('id'), request=request)
        if user == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_200_OK)


class UsersAPIView(ListAPIView, CreateAPIView):
    permission_classes = [AllowAny, DisablePermission]
    serializer_class = UserSerializer

    # @permission("_IsAuthenticated")
    def get(self, request, *args, **kwargs):
        self.queryset = User.objects.all()
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        self.serializer_class = CreateUserSerializer
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UsersBulkAPIView(ListAPIView, CreateAPIView):
    queryset = User.objects.none()
    permission_classes = [AllowAny, DisablePermission]
    serializer_class = UsersBulkCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = json.load(request.data['file'])
            list = [StdUser(**vals) for vals in data]
            StdUser.objects.bulk_create(list)
            self.queryset = User.objects.all()
            return Response(data="BULK OK",status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class VerifyUserAPIView(APIView):
    """
    Verify User by email
    """
    lookup_field = 'code'
    queryset = User.objects.all()
    serializer_class = VerifyUserSerializer
    permission_classes = [AllowAny, DisablePermission]

    def get(self, request, **kwargs):
        code = kwargs.get('code')
        StdUser.verify_email(code)
        serializer = self.serializer_class(code, data=request.data)
        return redirect('/')


class VerifyPassUserAPIView(APIView):
    lookup_field = 'code'
    serializer_class = VerifyUserPassSerializer
    permission_classes = [AllowAny, DisablePermission]

    def post(self, request, **kwargs):
        code = kwargs.get('code')
        password = request.data.get('password')
        if StdUser.verify_password(code=code, password=password):
            serializer = self.serializer_class(code, data=request.data)

            if serializer.is_valid():
                return redirect('/')


class RecoveryAPIView(APIView):
    permission_classes = [AllowAny, DisablePermission]
    redirect_to = settings.LOGIN_REDIRECT_URL

    # @permission("_IsAuthenticated")
    def get(self, request, *args, **kwargs):
        email = request.user.email

        user = User.objects.filter(Q(email=email)).distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
            user_obj.send_recovery_password(email=email)

        return Response(data={"Mail sent"},status=status.HTTP_200_OK)


class SetModeratorAPIView(APIView):
    permission_classes = [AllowAny, DisablePermission]
    queryset = User.objects.none()
    serializer_class = SetModeratorSerializer

    # @permission('IsAdminUser')
    def post(self, request, *args, **kwargs):
        user = get_user(value="id",arg=request.data.get('id'), request=request)
        if user==None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=request.data)
        set_check = request.data.get('is_moderator')
        user.is_moderator = set_check
        user.save()
        return Response(status=status.HTTP_202_ACCEPTED)


class AdminUserAPIView(APIView):
    permission_classes = [AllowAny, DisablePermission]
    queryset = User.objects.none()
    serializer_class = CreateUserSerializer

    # @permission("IsAdminUser")
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            if request.data.get('type_of_user')=="teacher":
                user = StdUser.objects.create_teacher(email=request.data.get('email'),
                                                      faculty=get_faculty(value="name",arg=request.data.get('faculty'), request=request),
                                                      password=request.data.get('password'))
            else:
                user = StdUser.objects.create_user(email=request.data.get('email'),
                                                   faculty=request.data.get('faculty'),
                                                   password=request.data.get('password'))
            user.is_active = True
            user.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    # @permission("IsAdminUser")
    def delete(self, request, *args, **kwargs):
        id = request.data.get('id')
        is_active = request.data.get('is_active')

        queryset = get_user(value="id",arg=id, request=request)
        self.serializer_class = AdminDeleteUserSerializer
        serializer=self.serializer_class(data=request.data)

        if queryset==None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            queryset.is_active = is_active
            queryset.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class BanUserAPIView(APIView):
    permission_classes = [AllowAny, DisablePermission]
    queryset = User.objects.none()
    serializer_class = SetActiveSerializer

    # @permission("IsAdminUser")
    def post(self, request, *args, **kwargs):
        user = get_user(value="id",arg=request.data.get('id'), request=request)
        is_active = request.data.get('is_active')
        if user == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=request.data)
        user.is_active = is_active
        user.save()
        return Response(status=status.HTTP_200_OK)
