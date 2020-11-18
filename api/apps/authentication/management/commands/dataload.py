from io import BytesIO
from PIL import Image
from faker import Faker

from django.core.files.base import File
from django.core.management.base import BaseCommand

from apps.authentication.models import StdUser

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


