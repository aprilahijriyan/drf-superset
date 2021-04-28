from django.urls import path

from .views import MediaList, MediaUpload

urlpatterns = [
    path("upload", MediaUpload.as_view(), name="media_upload"),
    path("list", MediaList.as_view(), name="media_list"),
]
