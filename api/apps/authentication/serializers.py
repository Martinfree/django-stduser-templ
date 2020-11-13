from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import get_user_model
from PIL import Image
import os
from apps.utils.functions import image_resize
from django.conf import settings
from apps.authentication.models import SocialUser
User = get_user_model()


class SocialAuthSerializer(serializers.ModelSerializer):
    
    class Meta(object):
        model = SocialUser
        fields =(
                'id',
                'email',
                'first_name',
                'last_name',
                'photo_url',
                'provider',
                )
    def save(self):
        id = " "
        first_name = " "
        last_name = " "
        photo_url = " "
        provider = " "
        for data in self.validated_data:
            if data =='id':
                id = self.validated_data['id']
            if data =='email':
                email = self.validated_data['email']
            if data =='firstName':
                first_name = self.validated_data['firstName']
            if data =='lastName':
                last_name = self.validated_data['lastName']
            if data =='photoUrl':
                photo_url = self.validated_data['photoUrl']
            if data =='provider':
                provider = self.validated_data['provider']
        social_user=SocialUser.objects.create(id=id,
                email=email,
                first_name=first_name,
                last_name=last_name,
                photo_url=photo_url,
                provider=provider)
        user = User.objects.create_user(email=email,password=f'{provider}{id}{email}')
        user.social_user = social_user
        user.is_active=True
        user.save()
        return user

class CreateUserSerializer(serializers.ModelSerializer):
    type_of_user = serializers.CharField(max_length=16,required=False,allow_blank=True)
    faculty = serializers.CharField(max_length=32,required=False,allow_blank=True)
    group = serializers.CharField(max_length=32,required=False,allow_blank=True)
    profession = serializers.CharField(max_length=32,required=False,allow_blank=True)

    class Meta(object):
        model = User
        fields = (
            'email',
            'type_of_user',
            'faculty',
            'profession',
            'group',
            'password',
        )

    def create(self, validated_data):

        validate_password(password=validated_data.get('password',),
                user=validated_data.get('email'),
                password_validators=None)

        email = validated_data.get('email');
        user = User.objects.create_user(**validated_data, user_type=3)
        user.send_mail(email=email)
        return user

class UsersBulkCreateSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False)

    class Meta(object):
        model = User
        fields = (
            'file',
        )
 

class RecoverySerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=64)

    class Meta(object):
        model = User
        fields = ('email',)


class VerifyUserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('code',)


class VerifyUserPassSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64)

    class Meta(object):
        model = User
        fields = ('code', 'password',)


class DeleteUserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User

        fields = ('email', 'password',)


class FindUserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()

    class Meta(object):
            model = User
            fields = (
                'id',
                'email',
                'first_name',
                'last_name',
                'patronymic',
                'bio',
                'avatar',
                'date_of_birth',

                'date_joined',
                'last_update',

                'news_subscription',
                'is_moderator',
                'is_active',
                'is_admin',

                'is_student',
                'is_teacher',
            )


class UserSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'patronymic',
            'bio',
            'avatar',
            'date_of_birth',

            'date_joined',
            'last_update',

            'news_subscription',
            'is_active',
            'is_admin',
            'is_moderator',
            'user_permissions',

            'is_student',
            'is_teacher',

            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'patronymic',
            'bio',
            'avatar',
            'news_subscription'
        )

    def update(self, instance, validated_data, id=None):
        image = None

        for d in validated_data:
            if d == 'email':
                instance.email = validated_data.get('email', instance.email)
            if d == 'first_name':
                instance.first_name = validated_data.get('first_name', instance.first_name)
            if d == 'last_name':
                instance.last_name = validated_data.get('last_name', instance.last_name)
            if d == 'patronymic':
                instance.patronymic = validated_data.get('patronymic', instance.patronymic)
            if d == 'bio':
                instance.bio = validated_data.get('bio', instance.bio)
            if d == 'avatar':
                os.remove(settings.BASE_DIR + '/media/authentication/' + os.path.basename(str(instance.avatar)))
                instance.avatar=validated_data.get('avatar',instance.avatar)
                image = image_resize(avatar = validated_data.get('avatar', instance.avatar),height = 300, width = 300)
            if d == 'news_subscription':
                instance.news_subscription = validated_data.get('news_subscription', instance.news_subscription)
        instance.save()

        if image !=None:
            main, tail = os.path.splitext(str(instance.avatar))
            name = 'avatar_'+str(id)+str(tail)
            os.remove(settings.BASE_DIR + '/media/authentication/' + os.path.basename(str(instance.avatar)))
            image.save(settings.BASE_DIR + '/media/authentication/' + name)
            instance.avatar.name = 'authentication/'+name
            instance.save()
        return instance



class AdminUserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = (
            'email',
            'is_moderator',
            'bio',
            'avatar',
            'is_active',
            'news_subscription'
        )

class BulkUpdateUserSerializer(serializers.ModelSerializer):
    
    class Meta(object):
        model = User
        fields = (
            'first_name',
            'last_name',
            'patronymic',
            'bio',
            'news_subscription'
        )

class DeleteAllSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ('email',
                  'password')


class AdminDeleteUserSerializer(serializers.ModelSerializer):

    class Meta(object):
        models = User
        fields = (
        'id',
        'is_active')


class SetActiveSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = (
                'id','is_active',)

class SetModeratorSerializer(serializers.ModelSerializer):
    id = serializers.CharField(max_length=19)
    class Meta(object):
        model = User
        fields = (
                'id','is_moderator',)

class NewsSubscriptionSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = (
            'id', 'news_subscription',)

