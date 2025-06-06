from django.urls import include, path
from .api import UserCreationApi, UserLoginApi, UserListApi, ProtectedViewApi
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('create/', UserCreationApi, name='user-create'),
    path('login/', UserLoginApi, name='user-login'),
    path('list/', UserListApi, name='user-list'),
    path('protected/', ProtectedViewApi, name='user-proctected'),
]
