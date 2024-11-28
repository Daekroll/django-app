from django.urls import path

from .views import upload_view

app_name = 'rare_loading_file'

urlpatterns = [
    path("upload/", upload_view, name="file_upload"),
]
