from django.urls import path
from importlib import import_module
from allauth.socialaccount import providers

from rest_framework_simplejwt.views import token_obtain_pair, token_refresh
from apps.authentication.views import (
    UserAPIView, UsersAPIView,
    VerifyPassUserAPIView, VerifyUserAPIView,
    RecoveryAPIView, SetModeratorAPIView,
    AdminUserAPIView,
    BanUserAPIView,SocialAuthAPIView,)


urlpatterns = [
    # user api
    path('social/', SocialAuthAPIView.as_view(), name='social'),
    path('users/', UsersAPIView.as_view(), name='users_list'),
    path('users/token_obtain/', token_obtain_pair, name='obtain_jwt'),
    path('users/recover_pass/', RecoveryAPIView.as_view(), name='recover'),
    path('users/token_refresh/', token_refresh, name='refresh_jwt'),
    path('users/verify/<str:code>/', VerifyUserAPIView.as_view(), name='verify'),
    path('users/recovery/<str:code>/', VerifyPassUserAPIView.as_view(), name='completerecover'),
    path('users/<str:id>/', UserAPIView.as_view(), name='user'),
]

