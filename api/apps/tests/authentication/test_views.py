import json
import nose.tools as nt

from nose.tools import nottest
from nose.tools.nontrivial import raises

from django.core import mail
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.authentication.models import StdUser
from apps.department.models import (
        Teacher,
        Student,
        Profession,
        Faculty)
from apps.authentication.serializers import (
        UserSerializer,
        UpdateUserSerializer,
        BulkUpdateUserSerializer,)

from settings.tests import *


""" Tests admin access to api methonds """
class TestAdminPermsAPIViews(APITestCase):
    
    """ Setup test data """
    @classmethod
    def setUpTestData(cls):
        cls.user = StdUser.objects.create_user(
                email=TEST_ADMIN_EMAIL,
                password=TEST_PASSWORD,
                user_type=1)

    def setUp(self):
        self.t_user = StdUser.objects.create_user(
                email=TEST_EMAIL2,
                password=TEST_PASSWORD)
        self.faculty = Faculty.objects.create(name=TEST_FACULTY)
        self.profession = Profession.objects.create(name=TEST_PROFESSION)
        self.teacher = StdUser.objects.create_teacher(
                email=TEST_TEACHER_EMAIL,
                password=TEST_PASSWORD,
                faculty=self.faculty)
        self.student = StdUser.objects.create_student(
                email=TEST_STUDENT_EMAIL,
                password=TEST_PASSWORD,
                faculty=self.faculty,
                profession=self.profession )

        self.get_token()

    """ This func helps to get jwt access token many times """
    @nottest
    def get_token(self):
        url = reverse('obtain_jwt')

        access_token = self.client.post(
                url,
                { "email": self.user.email, "password": TEST_PASSWORD },
                format='json').data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    
    def test_mass_mail_admin(self):
        url = reverse('mass_mail')
        
        data = {
                "subject": "TEST",
                "body": "TEST",
                "is_active": True,
                'is_student':True, 
                'is_teacher':True, 
                'is_moderator': True, 
                'is_admin': True
        }
        response = self.client.post(url, data, format='json') 

        nt.assert_equal(response.status_code, status.HTTP_200_OK)
    
    
    def test_bad_mass_mail_admin(self):
        url = reverse('mass_mail')
        
        data = {
                "subt": "TEST",
                "body": "TEST",
                "is_active": 34232523,
                'is_student':True, 
                'is_teacher':True, 
                'is_moderator': True, 
                'is_admin': True
        }

        response = self.client.post(url, data, format='json') 

        nt.assert_equal(response.status_code, status.HTTP_400_BAD_REQUEST)

    """ Test request to get users list """
    def test_get_all_users(self):
        url = reverse('users_list')
        
        response = self.client.get(url)
    
        users = StdUser.objects.all()
        serializer = UserSerializer(users, many=True)
        
        nt.assert_equal(response.data, serializer.data)
        nt.assert_equal(response.status_code, status.HTTP_200_OK)

    """ Test of creating user """
    def test_post_create_user(self):
        url = reverse('users_list')
        
        data = {
                "email": TEST_EMAIL3,
                "password": TEST_PASSWORD,
        }

        response = self.client.post(url, data, format='json') 
        user = StdUser.objects.get(email=TEST_EMAIL3)

        nt.assert_equal(response.status_code, status.HTTP_201_CREATED)
        nt.assert_not_equal(user, None)

    def test_bad_post_create_user(self):
        url = reverse('users_list')
        
        data = {
                "email": 12313221,
                "password": 213131231,
        }

        response = self.client.post(url, data, format='json') 

        nt.assert_equal(response.status_code, status.HTTP_400_BAD_REQUEST)
 

    """ Tests put update for one user """
    def test_put_one_user(self):
        url = reverse('user', args=[self.t_user.id])

        data = {
            "email": self.t_user.email,
            "bio": TEST_BIO,
            "news_subscription": True
        }

        response = self.client.put(url, data, format='json')
        
        nt.assert_equal(response.status_code, status.HTTP_200_OK)
    
    def test_bad_put_one_user(self):
        url = reverse('user', args=[self.user.id])

        data = {
            "email": 12345,
            "bio": 123445,
            "news_subscription": 123231
        }

        response = self.client.put(url, data, format='json')
        
        nt.assert_equal(response.status_code, status.HTTP_400_BAD_REQUEST)
     
    """ Test get one User """
    def test_get_one_user(self):
        url = reverse('user', args=[self.t_user.id,])
        
        response = self.client.get(url)
        
        nt.assert_equal(response.status_code, status.HTTP_200_OK)
         
    """ Test post one user """
    def test_post_one_user(self):
        url = reverse('user', args=[self.t_user.id],)

        response = self.client.post(url)

        nt.assert_equal(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

   
    """ Tests delete for one user """
    def test_delete_one_user(self):
        url = reverse('user', args=[self.t_user.id])

        response = self.client.delete(url)
        
        nt.assert_equal(response.data, None)
     
    """ Test set moderator """
    def test_set_moderator(self):
        url = reverse('set_moder')
        
        data = {
                "id": self.user.id,
                'is_moderator': True
        }

        response = self.client.post(url, data, format='json')
        nt.assert_equal(response.status_code, status.HTTP_202_ACCEPTED)
    
    """ Test set moderator """
    def test_not_found_set_moderator(self):
        url = reverse('set_moder')
        
        data = {
                "id": BAD_USER_ID,
                'is_moderator': True
        }

        response = self.client.post(url, data, format='json')
        nt.assert_equal(response.status_code, status.HTTP_404_NOT_FOUND)


    """ Test of creating user """
    def test_post_admin_create_user(self):
        url = reverse('admin_user')
        
        data = {
                "email": TEST_EMAIL6,
                "password": TEST_PASSWORD,
        }

        response = self.client.post(url, data, format='json') 
        user = StdUser.objects.get(email=TEST_EMAIL6)

        nt.assert_equal(response.status_code, status.HTTP_201_CREATED)
        nt.assert_not_equal(user, None)
    
    """ Test of creating user """
    def test_post_admin_create_user(self):
        url = reverse('admin_user')
        
        data = {
                "email": 23432423,
                "password": TEST_PASSWORD,
        }

        response = self.client.post(url, data, format='json') 

        nt.assert_equal(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    """ No such perm """
    def test_not_found_admin_delete_user(self):
        url = reverse('admin_user')
        
        data = {
            "id": BAD_USER_ID
        }

        response = self.client.delete(url, data, format='json')
        nt.assert_equal(response.status_code, status.HTTP_404_NOT_FOUND)
    
    """ No such perm """
    def test_admin_delete_user(self):
        url = reverse('admin_user')
        
        data = {
            "id": self.user.id
        }

        response = self.client.delete(url, data, format='json')
        nt.assert_not_equal(response.status_code, status.HTTP_404_NOT_FOUND)
        nt.assert_equal(response.status_code, status.HTTP_200_OK)


""" Test moderator access to api """
class TestModerPermsAPIViews(APITestCase):
    
    """ Setup test data """
    @classmethod
    def setUpTestData(cls):
        cls.user = StdUser.objects.create_user(
                email=TEST_MODER_EMAIL,
                password=TEST_PASSWORD,
                user_type=2)

    def setUp(self):
        self.t_user = StdUser.objects.create_user(
                email=TEST_EMAIL2,
                password=TEST_PASSWORD)
        self.faculty = Faculty.objects.create(name=TEST_FACULTY)
        self.profession = Profession.objects.create(name=TEST_PROFESSION)
        self.teacher = StdUser.objects.create_teacher(
                email=TEST_TEACHER_EMAIL,
                password=TEST_PASSWORD,
                faculty=self.faculty)
        self.student = StdUser.objects.create_student(
                email=TEST_STUDENT_EMAIL,
                password=TEST_PASSWORD,
                faculty=self.faculty,
                profession=self.profession )

    def test_not_found_post_set_news_subscription_user(self):
        url = reverse('set_subscribe')
        
        data = {
                "id": BAD_USER_ID,
                "news_subscription": True,
        }

        response = self.client.post(url, data, format='json') 

        nt.assert_equal(response.status_code, status.HTTP_404_NOT_FOUND)
  
    """ No such perm """
    def test_set_moderator(self):
        url = reverse('set_moder')

        data = {
            "id": self.user.id,
            'is_moderator': True,
        }

        response = self.client.post(url, data=data, format='json')

        nt.assert_equal(response.data, NO_SUCH_PERM);
    
    """ Test of creating user """
    def test_post_admin_create_user(self):
        url = reverse('admin_user')
        
        data = {
                "email": TEST_EMAIL6,
                "password": TEST_PASSWORD,
        }

        response = self.client.post(url, data, format='json') 

        nt.assert_equal(response.data, NO_SUCH_PERM)
    
    """ No such perm """
    def test_admin_delete_user(self):
        url = reverse('admin_user')
        
        data = {
            "id": self.user.id
        }

        response = self.client.delete(url, data, format='json') 

        nt.assert_equal(response.data, NO_SUCH_PERM)

    def test_moder_ban_user(self):
        url = reverse('ban_user')

        data = {
                "id": self.t_user.id
        }

        response = self.client.post(url, data, format='json')

        nt.assert_equal(response.status_code, status.HTTP_200_OK)
    
    """
    def test_not_found_moder_ban_user(self):
        url = reverse('ban_user')

        data = {
                "id": BAD_USER_ID
        }

        response = self.client.post(url, data, format='json')

        nt.assert_equal(response.status_code, status.HTTP_404_NOT_FOUND)
    """
    

    """Tests active user access to api methonds """
class TestActiveUserPermsAPIViews(APITestCase):
    
    """ Setup test data """
    @classmethod
    def setUpTestData(cls):
        cls.user = StdUser.objects.create_user(
                email=TEST_EMAIL,
                password=TEST_PASSWORD,
                user_type=3)
        cls.user.is_active = True
        cls.user.save()
        
    """ This func helps to get jwt access token many times """
    @nottest
    def get_token(self):
        url = reverse('obtain_jwt')

        access_token = self.client.post(
                url,
                { "email": self.user.email, "password": TEST_PASSWORD },
                format='json').data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def test_recovery_request(self):
        url = reverse('recover')
        
        response = self.client.get(url)

        nt.assert_equal(response.status_code, status.HTTP_200_OK)

    def setUp(self):
        self.t_user = StdUser.objects.create_user(
                email=TEST_EMAIL2,
                password=TEST_PASSWORD)
        self.faculty = Faculty.objects.create(name=TEST_FACULTY)
        self.profession = Profession.objects.create(name=TEST_PROFESSION)
        self.teacher = StdUser.objects.create_teacher(
                email=TEST_TEACHER_EMAIL,
                password=TEST_PASSWORD,
                faculty=self.faculty)
        self.student = StdUser.objects.create_student(
                email=TEST_STUDENT_EMAIL,
                password=TEST_PASSWORD,
                faculty=self.faculty,
                profession=self.profession)
        self.get_token()


    """ Standart user does not have such perms
    def test_get_all_users(self):
        url = reverse('users_list')
        
        response = self.client.get(url)
    
        users = StdUser.objects.all()
        serializer = UserSerializer(users, many=True)
        
        nt.assert_equal(response.data, NO_SUCH_PERM)

    """

    """ Standart user does not have such perms """
    def test_get_one_user(self):
        url = reverse('user', args=[self.t_user.id,])
        
        response = self.client.get(url)
        
        serializer = UserSerializer(self.t_user)

        nt.assert_equal(response.data, NO_SUCH_PERM)

    
    """ Tests put update for one user """
    def test_put_one_user(self):
        url = reverse('user', args=[self.user.id])

        data = {
            "email": TEST_EMAIL3,
            "fist_name": TEST_NAME,
            "last_name": TEST_SURNAME,
            "patronymic": TEST_PATRONIM,
            "bio": TEST_BIO,
            "news_subscription": True
        }

        response = self.client.put(url, data, format='json')
        
        nt.assert_equal(response.status_code, status.HTTP_200_OK)
    
    """ Tests delete for one user """
    def test_delete_one_user(self):
        url = reverse('user', args=[self.user.id])

        response = self.client.delete(url)
        
        nt.assert_equal(response.status_code, status.HTTP_200_OK)


    """ No such perm """
    def test_post_admin_create_user(self):
        url = reverse('admin_user')
        
        data = {
                "email": TEST_EMAIL6,
                "password": TEST_PASSWORD,
        }

        response = self.client.post(url, data, format='json') 

        nt.assert_equal(response.data, NO_SUCH_PERM)
    
    def test_post_set_news_subscription_user(self):
        url = reverse('set_subscribe')
        
        data = {
                "id": self.user.id,
                "news_subscription": True,
        }

        response = self.client.post(url, data, format='json') 

        nt.assert_equal(response.status_code, status.HTTP_200_OK)
       
    def test_false_post_set_news_subscription_user(self):
        url = reverse('set_subscribe')
        
        data = {
                "id": self.user.id,
                "news_subscription": False,
        }

        response = self.client.post(url, data, format='json') 

        nt.assert_equal(response.status_code, status.HTTP_200_OK)
    

""" Tests API of all user list """
class TestJWTToken(APITestCase):

    """ Setup test data """
    @classmethod
    def setUpTestData(cls):
        cls.admin = StdUser.objects.create_user(
                email=TEST_ADMIN_EMAIL,
                password=TEST_PASSWORD,
                user_type=1)

    """ Test jwt obtain """
    def test_obtain_refresh_jwt_token(self):
        url = reverse('obtain_jwt')
        
        data = {
            "email": TEST_ADMIN_EMAIL,
            "password": TEST_PASSWORD,
        }

        response = self.client.post(url, data, format='json')

        """ Testing if token in response """
        nt.assert_equal(response.status_code, status.HTTP_200_OK)
        nt.assert_true('access' in response.data)
        nt.assert_true('refresh' in response.data)
        
        access_token = response.data['access']
        refresh_token = response.data['refresh']
        
        data = {
            "refresh": refresh_token
        }

        url = reverse('refresh_jwt')

        response = self.client.post(url, data, format='json')

        """ Testing for new access token getting """
        nt.assert_equal(response.status_code, status.HTTP_200_OK)
        nt.assert_true('access' in response.data)
    
""" Test verify user API view """
class TestVerifyAPIView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = StdUser.objects.create_user(
                email = TEST_EMAIL,
                password = TEST_PASSWORD)

    def test_get(self):
        code = self.user.get_verification_code(email=self.user.email).decode()
        url = reverse('verify', kwargs={"code": code})
        
        response = self.client.get(url)

        nt.assert_equal(response.status_code, 302);

    def test_post_password_verify(self):
        code = self.user.get_verification_code(email=self.user.email).decode()
        url = reverse('completerecover', kwargs={"code": code})
        
        data = {
            "password": TEST_PASSWORD,
        }
        response = self.client.post(url, data=data)

        nt.assert_equal(response.status_code, 302);
    

