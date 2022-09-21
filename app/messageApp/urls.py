from django.urls import path, include
from rest_framework.routers import DefaultRouter

from messageApp import views

urlpatterns = [
    path('test', views.TestFCMViewSet.as_view()),
    path('device_register', views.FCMDeviceViewSet.as_view()),
]