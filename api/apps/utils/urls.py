from django.urls import path

from apps.utils.views import BulkUploadAPIView

urlpatterns = [
    path('bulk/', BulkUploadAPIView.as_view(), name='bulk_create')
]

