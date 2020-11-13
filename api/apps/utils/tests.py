import nose.tools as nt
from nose.tools import nottest
from nose.tools.nontrivial import raises
from django.core.files.uploadedfile import SimpleUploadedFile
from settings.base import BASE_DIR


from django.core.signing import (TimestampSigner, b64_encode)
from django.core import mail

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from apps.authentication.models import StdUser
from apps.department.models import(
        Profession, Faculty,
        Activity, Summary,
        Partner, Labour,
        Images, AcadGroup,
        Article, Classes,
        Student, Teacher,
        Mark, Message)
from apps.news.models import News,NewsInt
from apps.schedule.models import (Calendar, TimeTable, Schedule,Attendance)
from apps.subjects.models import Lesson
from apps.mailing.models import Mailing

from settings.tests import *
from PIL import Image
from django.core.files.base import File
from io import BytesIO

class TestModel(TestCase):

    @staticmethod
    def get_image_file(name='test', ext='png', size=(50, 50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    @classmethod
    def setUpTestData(cls):
        """Create all data for Testing models"""
        cls.su = StdUser.objects.create_superuser(email=TEST_SU_EMAIL,
                password=TEST_PASSWORD)

        cls.admin = StdUser.objects.create_user(email=TEST_ADMIN_EMAIL,
                password=TEST_PASSWORD,
                user_type=1)

        cls.moderator = StdUser.objects.create_user(email=TEST_MODER_EMAIL,
                password=TEST_PASSWORD,
                user_type=2)

        cls.faculty = Faculty.objects.create(name=TEST_FACULTY)

        cls.profession = Profession.objects.create(name=TEST_PROFESSION)

        cls.mailing = Mailing.objects.create(author=TEST_EMAIL_MAILING)
        cls.mailing2 = Mailing.objects.create(author=TEST_EMAIL_MAILING2)

        cls.teacher = StdUser.objects.create_teacher(
                email=TEST_TEACHER_EMAIL,
                faculty=cls.faculty,
                password=TEST_PASSWORD,
                image=cls.get_image_file(),
                web_link = TEST_ACADEMY_LINK_ST,
                description = TEST_DESCRIPTION_ST,
                subject_link = TEST_ACADEMY_LINK_ST)

        cls.group=AcadGroup.objects.create(
                name=GROUPS["КБ-1"],faculty=cls.faculty, headman=TEST_EMAIL6,
                course_year=COURSE_YEAR1)


        cls.student = StdUser.objects.create_student(
                email=TEST_STUDENT_EMAIL,
                profession=cls.profession,
                group=cls.group,
                faculty=cls.faculty,
                password=TEST_PASSWORD)

        cls.user = StdUser.objects.create_user(email=TEST_EMAIL,
                password=TEST_PASSWORD)
        cls.user.first_name = TEST_NAME
        cls.user.last_name  = TEST_SURNAME
        cls.user.patronymic = TEST_PATRONIM
        cls.user.is_active = True

        cls.user2 = StdUser.objects.create_user(email=TEST_EMAIL2,
                password=TEST_PASSWORD)
        cls.user2.first_name = TEST_NAME
        cls.user2.last_name  = TEST_SURNAME
        cls.user2.patronymic = TEST_PATRONIM


        cls.int_news = NewsInt.objects.create(
                title=TEST_TITLE,
                author=cls.user)

        cls.ext_news = News.objects.create(
                title=TEST_TITLE2,
                description=TEST_DESCR,
                is_checked=True)

        cls.classes = Classes.objects.create(
                name=TEST_TDIR,
                short_name=TEST_SHTDIR,
                faculty=cls.faculty,
                faculty_head=cls.moderator,
                description=TEST_DESCRIPTION_ST)

        cls.message = Message.objects.create(
                title=TEST_TITLE,
                description=TEST_DESCR,
                urls=TEST_URLS,
                group=cls.group,
                teacher=cls.teacher)

        cls.lesson=Lesson.objects.create(
                name=TEST_LESSON_NAME,
                classroom=TEST_CLASSROOM,
                year=COURSE_YEAR,
                amount=TEST_AMOUNT,
                type=TEST_TYPE,
                credit=False,
                course_work=False,
                exam=False,
                classes=cls.classes,
                teacher=cls.teacher,
                description=TEST_DESCRIPTION_ST)

        cls.schedule = Schedule.objects.create(
                time=TEST_TIME,
                date=TEST_DATE,
                week=TEST_WEEK,
                number=TEST_NUMBER,
                lesson=cls.lesson,
                teacher=cls.teacher,
                group=cls.group)

        cls.calendar = Calendar.objects.create(
                name=TEST_TITLE2,
                date=TEST_DATE,
                description=TEST_DESCR,
                author=TEST_EMAIL)

        cls.summary = Summary.objects.create(
                academy_link=TEST_ACADEMY_LINK_ST,
                is_visible=True,
                description=TEST_DESCR,
                teacher=cls.user)

        cls.partner = Partner.objects.create(
                is_international=True,
                site_link=TEST_ACADEMY_LINK_ST,
                description=TEST_DESCR)


        cls.classes = Classes.objects.create(
                name=TEST_TDIR,
                short_name=TEST_SHTDIR,
                faculty=cls.faculty,
                faculty_head=cls.moderator,
                description=TEST_DESCRIPTION_ST)

        cls.t_image = Images.objects.create(
                description=TEST_DESCR,
                image=cls.get_image_file(),
                author_user=cls.user,
                author_partner=cls.partner,
                author_lesson=cls.lesson,
                author_classes=cls.classes)

        cls.labour = Labour.objects.create(
                author = cls.user,
                file_link = TEST_FILE_LINK_ST,
                description=TEST_DESCR,
                is_visible=True)

        cls.activity  = Activity.objects.create(
                title=TEST_TITLE2,
                is_visible=True,
                description=TEST_DESCR,
                user=cls.user)

        cls.timetable = TimeTable.objects.create(
            number="1",
            begin=TIME_BEGIN,
            end=TIME_END)

        cls.attendance = Attendance.objects.create(
                missed=0,
                student = cls.user,
                lesson = cls.lesson
                )

        cls.article = Article.objects.create(
            title = TEST_TITLE,
            library_code = TEST_LIBRARY_CODE,
            authors = TEST_AUTHORS,
            release_date = TEST_DATE,
            place_of_publication = TEST_ARRAY_CHAR,
            file = None,
            external_link = TEST_ACADEMY_LINK_ST,
            annotation = TEST_DESCR,
            photo = cls.get_image_file(),
            owner = cls.user,
            users_with_access = TEST_ARRAY_INT,
            teacher = cls.teacher,
            classes = cls.classes
        )

        cls.mark = Mark.objects.create(
                lesson = cls.lesson,
                student = cls.student,
                mark = TEST_MARK)



class TestViews(APITestCase):
    USER_TYPE = 1

    @staticmethod
    def get_image_file(name='test', ext='png', size=(50, 50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    @nottest
    def get_token(self):
        """ This func helps to get jwt access token many times """
        url = reverse('obtain_jwt')

        access_token = self.client.post(
                url,
                { "email": self.user.email, "password": TEST_PASSWORD },
                format='json').data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)


    @classmethod
    def setUpTestData(cls):
        """Create all data for Testing api endpoints"""
        cls.su = StdUser.objects.create_superuser(email=TEST_SU_EMAIL,
                password=TEST_PASSWORD)

        cls.admin = StdUser.objects.create_user(email=TEST_ADMIN_EMAIL,
                password=TEST_PASSWORD,
                user_type=1)

        cls.moderator = StdUser.objects.create_user(email=TEST_MODER_EMAIL,
                password=TEST_PASSWORD,
                user_type=2)

        cls.faculty = Faculty.objects.create(name=TEST_FACULTY)
        cls.faculty = Faculty.objects.create(name=TEST_FACULTY2)

        cls.profession = Profession.objects.create(name=TEST_PROFESSION)

        cls.group = cls.group=AcadGroup.objects.create(
                name=GROUPS["КБ-1"],faculty=cls.faculty,
                course_year=COURSE_YEAR1)
        cls.teacher = StdUser.objects.create_teacher(
                email=TEST_TEACHER_EMAIL,
                faculty=cls.faculty,
                password=TEST_PASSWORD)

        cls.teacher2 = StdUser.objects.create_teacher(
                email=TEST_TEACHER_EMAIL2,
                faculty=cls.faculty,
                password=TEST_PASSWORD)

        cls.teacher3 = StdUser.objects.create_teacher(
                email=TEST_EMAIL6,
                faculty=cls.faculty,
                password=TEST_PASSWORD)
        cls.teacher4 = StdUser.objects.create_teacher(
                email=TEST_EMAIL4,
                faculty=cls.faculty,
                password=TEST_PASSWORD)


        cls.mailing = Mailing.objects.create(author=TEST_EMAIL_MAILING)
        cls.mailing2 = Mailing.objects.create(author=TEST_EMAIL_MAILING2)

        cls.student = StdUser.objects.create_student(
                email=TEST_STUDENT_EMAIL,
                profession=cls.profession,
                faculty=cls.faculty,
                password=TEST_PASSWORD,
                group=cls.group)

        cls.student3 = StdUser.objects.create_student(
                email=TEST_EMAIL5,
                profession=cls.profession,
                faculty=cls.faculty,
                password=TEST_PASSWORD,
                group=cls.group)

        cls.student4 = StdUser.objects.create_student(
                email=TEST_EMAIL7,
                profession=cls.profession,
                faculty=cls.faculty,
                password=TEST_PASSWORD,
                group=cls.group)



        cls.user = StdUser.objects.create_user(
                email=TEST_EMAIL,
                password=TEST_PASSWORD,
                user_type=cls.USER_TYPE)

        cls.user.first_name = TEST_NAME
        cls.user.last_name  = TEST_SURNAME
        cls.user.patronymic = TEST_PATRONIM
        cls.user.is_active = True
        cls.user.save()

        cls.t_user = StdUser.objects.create_user(
                email=TEST_EMAIL2,
                password=TEST_PASSWORD)
        cls.t_user.is_active = True
        cls.t_user.save()

        cls.partner = Partner.objects.create(
                is_international=True,
                site_link=TEST_ACADEMY_LINK_ST,
                description=TEST_DESCR)

        cls.partner2 = Partner.objects.create(
                is_international=True,
                site_link=TEST_ACADEMY_LINK_ST2,
                description=TEST_DESCR)

        cls.classes = Classes.objects.create(
                name=TEST_TDIR,
                short_name=TEST_SHTDIR,
                faculty=cls.faculty,
                faculty_head=cls.moderator,
                description=TEST_DESCRIPTION_ST)

        cls.lesson=Lesson.objects.create(
                name=TEST_LESSON_NAME2,
                classroom=TEST_CLASSROOM,
                year=COURSE_YEAR,
                amount=TEST_AMOUNT,
                type=TEST_TYPE,
                credit=False,
                course_work=True,
                exam=True,
                classes=cls.classes,
                teacher=cls.teacher,
                description=TEST_DESCRIPTION_ST)

        cls.lesson2=Lesson.objects.create(
                name=TEST_LESSON_NAME3,
                classroom=TEST_CLASSROOM,
                year=COURSE_YEAR,
                amount=TEST_AMOUNT,
                type=TEST_TYPE,
                credit=False,
                course_work=False,
                exam=False,
                classes=cls.classes,
                teacher=cls.teacher,
                description=TEST_DESCRIPTION_ST)

        cls.classes = Classes.objects.create(
                name=TEST_TDIR,
                short_name=TEST_SHTDIR,
                faculty=cls.faculty,
                faculty_head=cls.moderator,
                description=TEST_DESCRIPTION_ST)

        cls.img = Images.objects.create(
                description=TEST_DESCRIPTION_ST,
                image=SimpleUploadedFile(name='test.jpeg', content=open(BASE_DIR+'/apps/utils/test.jpeg', 'rb').read(), content_type='image/jpeg'),
                author_user=cls.user,
                author_partner=cls.partner,
                author_lesson=cls.lesson,
                author_classes=cls.classes)

        cls.int_news = NewsInt.objects.create(
                title=TEST_TITLE,
                author=cls.user)

        cls.group=AcadGroup.objects.create(
                name='КБ-51',headman=cls.student.email,curator=cls.teacher.email,faculty=cls.faculty,
                course_year="2019-10-11")
        cls.group2=AcadGroup.objects.create(
                name=GROUPS["КБ-2"],headman=TEST_EMAIL3 ,curator=cls.teacher2.email,faculty=cls.faculty,
                course_year=COURSE_YEAR1)

        cls.schedule = Schedule.objects.create(
                time=TEST_TIME,
                date=TEST_DATE,
                week=TEST_WEEK,
                number=TEST_NUMBER,
                lesson=cls.lesson2,
                teacher=cls.teacher,
                group=cls.group)

        cls.conflict_schedule = Schedule.objects.create(
                time=TEST_TIME,
                date=TEST_DATE,
                week=TEST_WEEK,
                number=TEST_NUMBER,
                lesson=cls.lesson2,
                teacher=cls.teacher,
                group=cls.group)


        cls.calendar = Calendar.objects.create(
                name=TEST_TITLE2,
                date=TEST_DATE,
                description=TEST_DESCR,
                author=TEST_EMAIL)

        cls.summary = Summary.objects.create(
                academy_link=TEST_ACADEMY_LINK_ST,
                is_visible=True,
                description=TEST_DESCR,
                teacher=cls.user)

        cls.t_image = Images.objects.create(
                description=TEST_DESCR,
                image=cls.get_image_file(),
                author_user=cls.user,
                author_partner=cls.partner2,
                author_classes=cls.classes)

        cls.labour = Labour.objects.create(
                author = cls.user,
                file_link = TEST_FILE_LINK_ST,
                description=TEST_DESCR,
                is_visible=True)

        cls.activity  = Activity.objects.create(
                title=TEST_TITLE2,
                is_visible=True,
                description=TEST_DESCR,
                user=cls.user)

        cls.attendance = Attendance.objects.create(
                missed=0,
                student = cls.student,
                lesson = cls.lesson2
                )

        cls.attendance2 = Attendance.objects.create(
                missed=2,
                student = cls.student3,
                lesson = cls.lesson2
                )

        cls.timetable = TimeTable.objects.create(
            number="1",
            begin=TIME_BEGIN,
            end=TIME_END)

        cls.mark = Mark.objects.create(
                lesson = cls.lesson,
                student = cls.student,
                mark = TEST_MARK)

        cls.mark2 = Mark.objects.create(
                lesson = cls.lesson,
                student = cls.student3,
                mark = TEST_MARK2)

        cls.article = Article.objects.create(
            title=TEST_TITLE,
            library_code=TEST_LIBRARY_CODE,
            authors=TEST_AUTHORS,
            release_date=TEST_DATE,
            place_of_publication=TEST_ARRAY_CHAR,
            file=None,
            external_link=TEST_ACADEMY_LINK_ST,
            annotation=TEST_DESCR,
            photo=cls.get_image_file(),
            owner=cls.user,
            users_with_access=TEST_ARRAY_INT,
            teacher=cls.teacher,
            classes=cls.classes
        )

    def setUp(self):
        self.get_token()
