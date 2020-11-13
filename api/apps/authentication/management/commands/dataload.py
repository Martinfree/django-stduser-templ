from io import BytesIO
from PIL import Image
from faker import Faker

from django.core.files.base import File
from django.core.management.base import BaseCommand

from apps.authentication.models import StdUser

from apps.department.models import(Profession,
                                   Faculty,
                                   AcadGroup,
                                   Classes, Mark,
                                   Activity, Summary,
                                   Partner, Labour,
                                   Article, Student,
                                   Teacher, Images)
from apps.mailing.models import Message
from apps.task.models import Task
from apps.news.models import NewsInt, News
from apps.schedule.models import (Schedule, Calendar, TimeTable, Attendance)
from apps.subjects.models import Lesson

from settings.tests import *

TEST_PASSWORD = "Admin123!"
TEST_SU_EMAIL = "superuser@example.com"
TEST_TIME = '12:00:{}'
TEST_TIME2 = '13:{}'
TEST_DATE = '2020-11-{}'
TEST_DATE2 = '2020-12-{}'
CURATOR = 'teacher_{}@example.com'
HEADMAN = 'headman_{}@example.com'
FIRST_NAME = 'Ivan'

DAYS = [
    "вівторок",
    "середа",
    "четвер",
    "п'ятниця",
    "субота"
]
fake = Faker('uk_UA')

class Command(BaseCommand):
    help = 'Loads data to DB'

    def print(self, data):
        self.stdout.write("[{}]".format(data))

    def get_image_file(self, name='file', ext='png', size=(50,50), color=(256, 0,0)):
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)

        return File(file_obj, name=name)

    def handle(self, *args, **kwargs):
        self.print("Creating superuser")
        self.su = StdUser.objects.create_superuser(email=TEST_SU_EMAIL,
                password=TEST_PASSWORD)

        self.print("Creating admin")
        self.admin = StdUser.objects.create_user(email=TEST_ADMIN_EMAIL,
                avatar=self.get_image_file(),
                password=TEST_PASSWORD,
                user_type=1)
        self.admin.first_name = fake.first_name_male()
        self.admin.save()

        self.print("Creating moder")
        self.moderator = StdUser.objects.create_user(email=TEST_MODER_EMAIL,
                password=TEST_PASSWORD,
                user_type=2)
        self.moderator.first_name = fake.first_name_male()
        self.moderator.save()

        self.print("Creating profession")
        self.profession = Profession.objects.create(name=TEST_PROFESSION)

        self.print("Creating faculty")
        self.faculty = Faculty.objects.create(name=TEST_FACULTY,short_name=TEST_FACULTY_SHORT,faculty_head=self.moderator)

        for i in range(1, 24):
            self.print("Creating teacher #" + str(i))
            self.teacher = StdUser.objects.create_teacher(
                email=fake.email(),
                faculty=self.faculty,
                password=TEST_PASSWORD,
                image=self.get_image_file(),
                web_link = fake.url(),
                description = fake.paragraph(),
                subject_link = fake.url())
            self.teacher.first_name = fake.first_name_male()
            self.teacher.is_active = True
            self.teacher.save()

            if i == 1:
                self.teacher_1 = self.teacher

        t=StdUser.objects.all().filter(is_teacher=True)
        emails = []
        for _ in range(20):
            emails.append(fake.email())

        for i in range(1, 4):
            self.print("Creating academic group #{}".format(i))
            self.group=AcadGroup.objects.create(
                name=GROUPS["КБ-{}".format(i)],
                faculty=self.faculty,
                course_year=COURSE_YEAR1,
                curator=t[i],
                headman=emails[i])

            self.group1=AcadGroup.objects.create(
                name=GROUPS["КСМ-{}".format(i)],
                faculty=self.faculty,
                course_year=COURSE_YEAR1,
                curator=t[i+10],
                headman=emails[i+10])


        self.print("Creating student")
        self.student = StdUser.objects.create_student(
                email=emails[5],
                profession=self.profession,
                group=self.group,
                faculty=self.faculty,
                password=TEST_PASSWORD)
        self.student.first_name = fake.first_name_male()
        self.student.is_active = True
        self.student.save()


        self.print("Creating simple user #1")
        self.user = StdUser.objects.create_user(email=fake.email(),
                password=TEST_PASSWORD)
        self.user.first_name = fake.first_name_male()
        self.user.last_name  = fake.last_name_male()

        self.print("Creating simple user #2")
        self.user2 = StdUser.objects.create_user(email=fake.email(),
                password=TEST_PASSWORD)
        self.user2.first_name = fake.first_name_male()
        self.user2.last_name  = fake.last_name_male()

        for i in range(1, 10):
            self.print("Creating int_news #{}".format(i))
            self.int_news = NewsInt.objects.create(
                    title=fake.bs(),
                    content=fake.paragraph(),
                    author=self.user)

        for i in range(1, 10):
            self.print("Creating ext_news (is_checked=True) #{}".format(i))
            self.ext_news = News.objects.create(
                    title=fake.bs(),
                    description=fake.catch_phrase(),
                    is_checked=True)

        for i in range(1, 4):
            self.print("Creating ext_news (is_checked=False) #{}".format(i))
            self.ext_news = News.objects.create(
                    title=(TEST_TITLE2 + "_" + str(i)),
                    description=TEST_DESCR,
                    is_checked=False)

        self.print("Creating class")
        self.classes = Classes.objects.create(
                name=fake.bs(),
                short_name=fake.word(),
                faculty=self.faculty,
                faculty_head=self.moderator,
                description=fake.text(max_nb_chars=7))

        for i in range(1, 6):
            self.print("Creating lesson {}".format(i))
            self.lesson=Lesson.objects.create(
                name=fake.word(),
                classroom=TEST_CLASSROOM,
                year=2020,
                amount=TEST_AMOUNT,
                type=TEST_TYPE,
                credit=False,
                course_work=False,
                exam=False,
                classes=self.classes,
                teacher=self.teacher,
                description=fake.text(max_nb_chars=23))

        for i in range(1, 6):
            self.print("Creating schedules #{}".format(i))
            self.schedule = Schedule.objects.create(
                    time=fake.future_datetime(),
                date=DAYS[i-1],
                week=TEST_WEEK,
                number=1,
                lesson=self.lesson,
                teacher=self.teacher,
                group=self.group)

        for i in range(1, 6):
            self.print("Creating schedules #{}".format(i))
            self.schedule = Schedule.objects.create(
                time=fake.future_datetime(),
                date=DAYS[i-1],
                week=TEST_WEEK,
                number=1,
                lesson=self.lesson,
                teacher=self.teacher,
                group=self.group)

        for i in range(1, 6):
            self.print("Creating schedules #{}".format(i))
            self.schedule = Schedule.objects.create(
                time=fake.future_datetime(),
                date=DAYS[i-1],
                week=TEST_WEEK,
                number=1,
                lesson=self.lesson,
                teacher=self.teacher,
                group=self.group)

        les = Lesson.objects.all().filter()

        for i in range(1, 5):
            self.print("Creating mark {}".format(i))
            self.mark = Mark.objects.create(
                    lesson=les[i],
                    student=self.student,
                    mark=fake.random_int(min=0,max=100))

        for i in range(1, 4):
            self.print("Creating calendar events #{}".format(i))
            self.calendar = Calendar.objects.create(
                    name=fake.text(max_nb_chars=31),
                    date=fake.future_datetime(),
                    description=fake.text(max_nb_chars=20),
                    author=self.teacher.email)

        self.print("Creating summary")
        self.summary = Summary.objects.create(
                academy_link=fake.url(),
                is_visible=True,
                description=fake.paragraph,
                teacher=self.teacher)

        self.print("Creating image")
        self.t_image = Images.objects.create(
                description=fake.paragraph(),
                image=self.get_image_file(),
                author_user=self.user)

        self.print("Creating labour")
        self.labour = Labour.objects.create(
                author=self.user,
                file_link = fake.url(),
                description = fake.paragraph(),
                is_visible=True)

        self.print("Creating partner")
        self.partner = Partner.objects.create(
                is_international=True,
                site_link=fake.url(),
                description=fake.company())

        for i in range(1, 20):
            self.print("Creating activity #" + str(i))
            self.activity  = Activity.objects.create(
                title=fake.text(max_nb_chars=20),
                is_visible=True,
                description=fake.paragraph(),
                user=self.user)

        self.print("Creating timetable")
        self.timetable = TimeTable.objects.create(
                number="1",
                begin=TIME_BEGIN,
                end=TIME_END)

        self.print("Creating class")
        self.classes = Classes.objects.create(
                name=TEST_TDIR,
                short_name=TEST_SHTDIR,
                faculty=self.faculty,
                faculty_head=self.moderator,
                description=TEST_DESCRIPTION_ST)

        for i in range(1, 20):
            self.print("Creating article #" + str(i))
            self.article = Article.objects.create(
                title = fake.bs(),
                library_code = fake.credit_card_number(),
                authors = TEST_AUTHORS,
                release_date = TEST_DATE.format(str(10)),
                place_of_publication = TEST_ARRAY_CHAR,
                file = None,
                external_link = fake.url(),
                annotation = fake.sentence(),
                photo = self.get_image_file(),
                owner = self.teacher_1,
                users_with_access = TEST_ARRAY_INT,
                teacher = self.teacher_1,
                classes = self.classes)

        for i in range(1, 5):
            self.print("Creating attendance {}".format(i))
            self.attendance = Attendance.objects.create(
                missed = i * 10,
                student = self.student,
                lesson = les[i])

        self.print("Creating message")
        self.message = Message.objects.create(
            title=fake.bs(),
            description=fake.text(max_nb_chars=7),
            urls=TEST_URLS,
            group_id=self.group.id,
            teacher_id=self.teacher.id)

        self.print("Creating task")
        self.task = Task.objects.create(
            subject="dssw",
            mark=20,
            lab_counter=1)