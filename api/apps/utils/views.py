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

from apps.utils.serializers import BulkUploadSerializer

from apps.department.models import (Teacher, Student, AcadGroup,
                                    Partner, Article, Labour,
                                    Activity, Summary, Faculty,
                                    Classes,)

from apps.schedule.models import TimeTable, Calendar, Schedule
from apps.subjects.models import Lesson
from apps.mailing.models import Mailing
from apps.news.models import News, NewsInt

from apps.utils.permissions import (AllowAny,IsUser,_IsAuthenticated,
                                    IsAuthenticated, DisablePermission,)
from apps.utils.decorators import permission, permissions
from apps.utils.functions import bulk_table_upload

User = get_user_model()

MODELS = {
        "User": User,
        "Student": Student,
        "Teacher": Teacher,
        "Faculty": Faculty,
        "Activity": Activity,
        "Labour": Labour,
        "Partner": Partner,
        "AcadGroup": AcadGroup,
        "Article": Article,
        "Summary": Summary,
        "Classes": Classes,
        "TimeTable": TimeTable,
        "Calendar": Calendar,
        "Schedule": Schedule,
        "Lesson": Lesson,
        "Mailing": Mailing,
        "News": News,
        "NewsInt": NewsInt,}

class BulkUploadAPIView(ListAPIView, CreateAPIView):
    queryset = User.objects.none()
    permission_classes = [AllowAny, DisablePermission]
    serializer_class = BulkUploadSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                data = json.load(request.data['file'])
            except AttributeError:
                return Response(data="No file for upload",status=status.HTTP_400_BAD_REQUEST)
            model = MODELS.get(request.data['name'])
            ret = bulk_table_upload(data,model)
            if ret == 0:
                return Response(status=status.HTTP_201_CREATED)
            if ret == -1:
                return Response(data="Duplicated key detected:\n",status=status.HTTP_400_BAD_REQUEST)
            if ret == -2:
                return Response(data="something wrong with uploaded file or model is not exist",status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
