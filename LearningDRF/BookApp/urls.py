from django.db import router
from django.urls import include, path
from .api import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('router', BookModelViewSet, basename='book')

urlpatterns = [
    path('list/', BookListApi, name="BookListApi"),
    path('create/', BookCreateApi, name="BookCreateApi"),
    path('update/<int:id>', BookUpdateApi, name="BookUpdateApi"),
    path('delete/<int:id>', BookDeleteApi, name="BookDeleteApi"),
    path('', include(router.urls)),
]
