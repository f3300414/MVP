from django.urls import path
from FileSystem.views import FolderViewSet, FileViewSet

urlpatterns = [
    path('folders/', FolderViewSet.as_view(), name='folder-viewset'),
    path('files/', FileViewSet.as_view(), name='file-viewset')
]