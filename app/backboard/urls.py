from django.urls import path, include
from . import views
from django.shortcuts import render
from django.http import HttpResponse

urlpatterns = [
    path('all_cases', views.all_cases, name = 'all_cases'), 
    path('', views.login, name='backboard_login'),
    path('all_members', views.all_members, name = 'all_members'), 
    path('bills', views.bills, name = 'bills'), 
    path('case_detail', views.case_detail, name = 'case_detail'), 
    path('member_detail', views.member_detail, name = 'member_detail'), 
    path('all_blogs', views.all_blogs, name = 'all_blogs'), 
    path('new_blog', views.new_blog, name = 'new_blog'), 
    path('all_categories', views.all_categories, name = 'all_categories'),
    path('new_edit_category', views.new_edit_category, name = 'new_edit_category'),
    path('member_data_review', views.member_data_review, name = 'member_data_review'),
    path('refunds', views.refunds, name = 'refunds'),
    path('logout', views.logout, name='backboard_logout'),
    path('all_assistances', views.all_assistances, name = 'all_assistances'), 
    path('new_assistance', views.new_assistance, name = 'new_assistance'), 
    path('userstore_detail', views.userstore_detail, name = 'userstore_detail'), 
    path('ajax_refresh_county', views.ajax_refresh_county, name = 'ajax_refresh_county'),
    

]