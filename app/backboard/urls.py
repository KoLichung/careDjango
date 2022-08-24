from django.urls import path, include
from . import views
from django.shortcuts import render
from django.http import HttpResponse

urlpatterns = [
    path('', views.all_cases, name = 'all_cases'), 
    path('all_members', views.all_members, name = 'all_members'), 
    path('bills', views.bills, name = 'bills'), 
    path('case_detail', views.case_detail, name = 'case_detail'), 
    path('member_detail', views.member_detail, name = 'member_detail'), 
    path('all_blogs', views.all_blogs, name = 'all_blogs'), 
    path('new_blog', views.new_blog, name = 'new_blog'), 


]