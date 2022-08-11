from django.urls import path, include
from . import views
from django.shortcuts import render
from django.http import HttpResponse

urlpatterns = [
    path('all_cases', views.all_cases, name = 'all_cases'), 
    path('all_members', views.all_members, name = 'all_members'), 
    path('bills', views.bills, name = 'bills'), 
    path('case_detail', views.case_detail, name = 'case_detail'), 
    path('member_detail', views.member_detail, name = 'member_detail'), 
]