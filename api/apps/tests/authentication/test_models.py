import nose.tools as nt

from nose.tools.nontrivial import raises

from django.core.signing import (TimestampSigner, b64_encode)
from django.core import mail

from django.test import TestCase

from apps.utils.tests import TestModel
from apps.authentication.models import StdUser

from settings.tests import *

class AuthenticationTests(TestModel):

    def test_su_permissions(self):
        nt.assert_true(self.su.is_superuser)
        nt.assert_true(self.su.is_staff)

    def test_su_is_active(self):
        nt.assert_true(self.su.is_active)
    

    def test_admin_permissions(self):
        nt.assert_true(self.admin.is_admin)
        nt.assert_false(self.admin.is_moderator)
        nt.assert_false(self.admin.is_superuser)

    def test_admin_is_active(self):
        nt.assert_true(self.admin.is_active)


    def test_moderator_permissions(self):
        nt.assert_true(self.moderator.is_moderator)
        nt.assert_false(self.moderator.is_admin)

    def test_moderator_is_active(self):
        nt.assert_true(self.moderator.is_active)


    @raises(ValueError)
    def test_user_without_email(self):
        self.bad_user = StdUser.objects.create_user(email=None, password=TEST_PASSWORD)

    def test_get_verification_code(self):
        signer = TimestampSigner()
        code = b64_encode(bytes(signer.sign(TEST_EMAIL), encoding='utf-8'))
        
        nt.assert_equal(self.user.get_verification_code(TEST_EMAIL), code)

    def test_verify_email(self):
        code = self.user.get_verification_code(TEST_EMAIL)
        
        nt.assert_equal(self.user.verify_email(code.decode('utf-8')), 
                (True, MSG_ACCOUNT_ACTIVATED))
    
    def test_verify_password(self):
        code = self.user.get_verification_code(TEST_EMAIL)
        
        nt.assert_equal(self.user.verify_password(code.decode('utf-8'), TEST_PASSWORD), 
                True)

    ''' Test password verification without code '''
    @raises(ValueError)
    def test_verify_password_no_code(self):
        self.user.verify_password(None, TEST_PASSWORD)

    ''' Test password verification when user not exist '''
    @raises(ValueError)
    def test_verify_password_error(self):
        code = self.user.get_verification_code(TEST_EMAIL)
        self.user.verify_password(code, TEST_PASSWORD)

    ''' Test case when error occurs in verify_email func '''
    @raises(ValueError)
    def test_verify_email_error(self):
        self.user.is_active = True
        self.user.save()
        code = self.user.get_verification_code(TEST_EMAIL)
        self.user.verify_email(code.decode('utf-8')) 

    ''' If code is None '''
    @raises(ValueError)
    def test_verify_email_no_code(self):
        self.user.verify_email(code=None)

    ''' Sending of verification email test '''
    def test_send_mail(self):
        self.user.send_mail(TEST_EMAIL)
       
        nt.assert_equal(len(mail.outbox), 1)
        nt.assert_equal(mail.outbox[0].subject, MAIL_SUBJECT)
        nt.assert_equal(mail.outbox[0].to, [TEST_EMAIL, ])

    ''' Sending of password restoration mail '''
    def test_send_revovery_password(self):
        self.user.send_recovery_password(TEST_EMAIL)

        nt.assert_equal(len(mail.outbox), 1)
        nt.assert_equal(mail.outbox[0].subject, MAIL_SUBJECT)
        nt.assert_equal(mail.outbox[0].to, [TEST_EMAIL, ])

    ''' Work only when user has is_active status '''
    def test_login(self):
        self.user.is_active = True
        self.user.save()
        
        login = self.client.login(email=TEST_EMAIL, password=TEST_PASSWORD)
        
        nt.assert_true(login)

    ''' When user not is_active he cant log in '''
    def test_not_login(self):
        login = self.client.login(email=TEST_EMAIL, password=TEST_PASSWORD)
        
        nt.assert_false(login)

    ''' Test get_short_name() func '''
    def test_get_short_name(self):
        short_name = self.user.get_short_name()
        
        nt.assert_equal(short_name, "%s" % (TEST_NAME))

    ''' Test get_full_name() func '''
    def test_get_full_name(self):
        full_name = self.user.get_full_name()
        
        nt.assert_equal(full_name, "%s %s %s" % (
            TEST_NAME, 
            TEST_SURNAME, 
            TEST_PATRONIM))

    def test_title(self):
        nt.assert_equal(self.profession.name, TEST_PROFESSION)

    ''' Test faculty title '''
    def test_title(self):
        nt.assert_equal(self.faculty.name, TEST_FACULTY)


    ''' Test user is object '''
    def test_user_not_none(self):
        nt.assert_not_equal(self.student.student.user, None)

    ''' Test if no email passed '''
    @raises(ValueError)
    def test_student_not_email(self):
        StdUser.objects.create_student(
            email=None,
            profession=self.profession,
            faculty=self.faculty,
            password=TEST_PASSWORD)

    ''' Test if no such profession '''
    @raises(ValueError)
    def test_not_profession(self):
        StdUser.objects.create_student(
            email=TEST_EMAIL2,
            profession=None,
            faculty=self.faculty,
            password=TEST_PASSWORD)
   
    ''' Test if not such faculty ''' 
    @raises(ValueError)
    def test_student_not_faculty(self):
        StdUser.objects.create_student(
            email=TEST_EMAIL3,
            profession=self.profession,
            faculty=None,
            password=TEST_PASSWORD)
