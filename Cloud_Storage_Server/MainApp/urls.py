from .views import *
from . import views
from django.urls import path
from .serializers import UserSerializer

class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer

urlpatterns = [
    # Working with files
    path('api/file/upload/', UploadFile.as_view(), name='file-upload'),
    path('api/file/download/<int:pk>/', DownloadFile.as_view(), name='file-dowload'),
    path('api/file/delete/', DeleteFile.as_view(), name='file-delete'),
    path('api/file/<int:pk>/', ViewFile.as_view(), name='file'),
    path('registration/', views.RegPage, name="registration"),
    path('home/', views.HomePage, name="home"),

    # Working with users
    path("api/user/create/", UserCreate.as_view(), name="user-create"),
    path("api/user/login/", LoginView.as_view(), name="user-login"),
    path("api/user/files/", ViewUserFiles.as_view(), name="user-files")
]   