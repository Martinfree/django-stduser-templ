from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.authentication.models import (
        StdUser, SocialUser
)


@admin.register(SocialUser)
class SocialUserAdmin(admin.ModelAdmin):
    pass

@admin.register(StdUser)
class StdUserAdmin(BaseUserAdmin):
    readonly_fields = ['date_joined',]
