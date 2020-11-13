from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from PIL import Image, ImageFile
from apps.authentication.models import StdUser, StdUserManager

"""
get_ functions for raise DoesNotExist error
"""
def get_user(value,arg, request, email=None, password=None):
    if value=="id":
        try:
            return StdUser.objects.get(id=arg)
        except:
            return StdUser.objects.create_user(id=arg, email=request.data.get("email"), password=request.data.get("password"))

    elif value=="email":
        try:
            return StdUser.objects.get(email=arg)
        except:
            return StdUser.objects.create_user(email=arg, password=request.data.get(password))

def get_user_dec(value,arg):
    if value=="id":
        try:
            return StdUser.objects.get(id=arg)
        except StdUser.DoesNotExist:
            return None

    elif value=="email":
        try:
            return StdUser.objects.get(email=arg)
        except StdUser.DoesNotExist:
            return None

def image_resize(avatar, height, width):
    img = Image.open(avatar)
    if (height ==None) and (width == None):
        return img
    if img.height != height or img.width != width:
        new_img = (height, width)
        img = img.resize(new_img, Image.ANTIALIAS)
        return img


"""
def get_ext_news_dec(value,arg):
    if value=="id":
        try:
            return News.objects.get(id=arg)
        except News.DoesNotExist:
            return None

def get_int_news_dec(value,arg):
    if value=="id":
        try:
            return NewsInt.objects.get(id=arg)
        except NewsInt.DoesNotExist:
            return None

def get_calendar_dec(value,arg):
    if value=="id":
        try:
            return Calendar.objects.get(id=arg)
        except Calendar.DoesNotExist:
            return None

def get_labour_dec(value,arg):
    if value=="id":
        try:
            return Labour.objects.get(id=arg)
        except Labour.DoesNotExist:
            return None

def get_activity_dec(value,arg):
    if value=="id":
        try:
            return Activity.objects.get(id=arg)
        except Activity.DoesNotExist:
            return None

def get_partner_dec(value,arg):
    if value=="id":
        try:
            return Partner.objects.get(id=arg)
        except Partner.DoesNotExist:
            return None

def get_summary_dec(value,arg):
    if value=="id":
        try:
            return Summary.objects.get(id=arg)
        except Summary.DoesNotExist:
            return None

def get_user(value,arg, request, email=None, password=None):
    if value=="id":
        try:
            return StdUser.objects.get(id=arg)
        except:
            return StdUser.objects.create_user(id=arg, email=request.data.get("email"), password=request.data.get("password"))

    elif value=="email":
        try:
            return StdUser.objects.get(email=arg)
        except:
            return StdUser.objects.create_user(email=arg, password=request.data.get(password))

def get_student(value, arg):
    if value == "id":
        try:
            return Student.objects.get(id=arg)
        except StdUser.DoesNotExist:
            return None

    elif value=="email":
        try:
            return StdUser.objects.get(email=arg)
        except StdUser.DoesNotExist:
            return None

def get_ext_news(value,arg, request, title=None):
    if value=="id":
        try:
            return News.objects.get(id=arg)
        except:
            return News.objects.create(id=arg, title=request.data.get("title"))

def get_int_news(value,arg, request, title=None, author=None):
    if value=="id":
        try:
            return NewsInt.objects.get(id=arg)
        except:
            return NewsInt.objects.create(id=arg, title=request.data.get("title"),
                                       author=StdUser.objects.get(email=request.data.get("author")))

def get_summary(value,arg, request, teacher=None, description=None, academy_link=None):
    if value == "id":
        try:
            return Summary.objects.get(id=arg)
        except:
            return Summary.objects.create(id=arg, description=request.data.get("description"), academy_link=request.data.get("academy_link"),
                                          teacher=StdUser.objects.get(email=request.data.get("teacher")))

def get_image(value,arg):
    if value == "id":
        try:
            return Images.objects.get(id=arg)
        except Images.DoesNotExist:
            return None
    elif value == "author":
        if arg.author_user != None:
            try:
                return Images.objects.filter(author_user=arg.author_user)
            except Images.DoesNotExist:
                return None
    elif value == "author":
        if arg.author_lesson != None:
            return Images.objects.filter(author_lesson=arg.author_lesson)
    elif value == "author":
        if arg.author_partner != None:
            try:
                return Images.objects.filter(author_partner=arg.author_partner)
            except Images.DoesNotExist:
                return None
    elif value == "author":
        if arg.author_classes != None:
            try:
                return Images.objects.get(author_classes=arg.author_classes)
            except Images.DoesNotExist:
                return None
    else:
        return None

def image_resize(avatar, height, width):
    img = Image.open(avatar)
    if (height ==None) and (width == None):
        return img
    if img.height != height or img.width != width:
        new_img = (height, width)
        img = img.resize(new_img, Image.ANTIALIAS)
        return img

def get_calendar(value, arg, request, name=None, date=None):
    if value=="id":
        try:
            return Calendar.objects.get(id=arg)
        except:
            return Calendar.objects.create(id=arg, name=request.data.get("name"),
                                       date=request.data.get("date"))

def get_labour(value,arg, request, author=None, file_link=None, description=None):
    if value=="id":
        try:
            return Labour.objects.get(id=arg)
        except:
            return Labour.objects.create(id=arg,
                                       description=request.data.get("description"),
                                       file_link=request.data.get("file_link"),
                                       author=StdUser.objects.get(email=request.data.get("author")))

def get_activity(value, arg, request, title=None, description=None, user=None):
    if value=="id":
        try:
            return Activity.objects.get(id=arg)
        except:
            return Activity.objects.create(id=arg, title=request.data.get("title"),
                                  description=request.data.get("description"),
                                  user=StdUser.objects.get(email=request.data.get("user")))

def get_partner(value, arg, request, description=None, site_link=None):
    if value=="id":
        try:
            return Partner.objects.get(id=arg)
        except:
            return Partner.objects.create(id=arg,
                                  description=request.data.get("description"),
                                  site_link=request.data.get("site_link"))

def get_schedule(value, arg, request, time=None, date=None, number=None):
    if value == "id":
        try:
            return Schedule.objects.get(id=arg)
        except:
            return Schedule.objects.create(id=arg, time=request.data.get("time"),
                                  number=request.data.get("number"),
                                  date=request.data.get("date"))

def get_attendance(value, arg, request, missed=None, student=None, lesson=None):
    if value == "id":
        try:
            return Attendance.objects.get(id=arg)
        except:
            return Attendance.objects.create(id=arg, missed=request.data.get("missed"),
                                  student=StdUser.objects.get(id=request.data.get("student")),
                                  lesson=Lesson.objects.get(id=request.data.get("lesson")))

def get_acad_group(value, arg, request, name=None, curator=None, headman=None):
    if value == "id":
        try:
            return AcadGroup.objects.get(id=arg)
        except:
            return AcadGroup.objects.create(id=arg, name=request.data.get("name"),
                                  curator=request.data.get("curator"),
                                  headman=request.data.get("headman"))
    elif value == "name":
        try:
            return AcadGroup.objects.get(name=arg)
        except:
            return AcadGroup.objects.create(name=arg,
                                  curator=request.data.get("curator"),
                                  headman=request.data.get("headman"))


def get_faculty(value, arg, request, name=None):
    if value == "id":
        try:
            return Faculty.objects.get(id=arg)
        except:
            return Faculty.objects.create(id=arg, name=request.data.get("name"))

    elif value == "name":
        try:
            return Faculty.objects.get(name=arg)
        except:
            return Faculty.objects.create(name=arg)


def get_lesson(value, arg, request, name=None):
    if value == "id":
        try:
            return Lesson.objects.get(id=arg)
        except:
            return Lesson.objects.create(id=arg, name=request.data.get("name"))
    else:
        return None

def get_article(value, arg, request, title=None, authors=None,  place_of_publication=None):
    if value == "id":
        try:
            return Article.objects.get(id=arg)
        except:
            return Article.objects.create(id=arg, title=request.data.get("title"),
                                  authors=request.data.get("authors"),
                                  place_of_publication=request.data.get("place_of_publication"))
    else:
        return None

def get_classes(value, arg, request, name=None, short_name=None):
    if value == "id":
        try:
            return Classes.objects.get(id=arg)
        except:
            return Classes.objects.create(id=arg, name=request.data.get("name"),
                                  short_name=request.data.get("short_name"))
    else:
        return None

def get_mark(value, arg, request, mark=None, lesson=None, student=None):
    if value == "id":
        try:
            return Mark.objects.get(id=arg)
        except:
            return Mark.objects.create(id=arg, lesson=Lesson.objects.get(id=request.data.get("lesson")),
                                  student=StdUser.objects.get(id=request.data.get("student")),
                                  mark=request.data.get("mark"))
    else:
        return None

def get_profession(arg):
    pass


def bulk_table_upload(data,model):
    try:
        list = [model(**vals) for vals in data]
        model.objects.bulk_create(list)
        self.queryset = model.objects.all()
        return 0
    except IntegrityError:
        return -1
    except:
        return -2
    return -4

def get_message(value, arg, request, title=None, description=None, urls=None):
    if value == "id":
        try:
            return Message.objects.get(id=arg)
        except:
            return Message.objects.create(id=arg, title=request.data.get("title"),
                                  description=request.data.get("description"),
                                  urls=request.data.get("urls"))
    else:
        return None

def get_task(value, arg, request, subject=None, mark=None, lab_counter=None):
    if value == "id":
        try:
            return Task.objects.get(id=arg)
        except:
            return Task.objects.create(id=arg, subject=request.data.get("subject"),
                                  mark=request.data.get("mark"),
                                  lab_counter=request.data.get("lab_counter"))
"""
