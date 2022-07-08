from django.urls import path, include
from . import views
from django.shortcuts import render
from django.http import HttpResponse



urlpatterns = [
    path('index', views.index, name = 'index'), 
    path('login', views.login, name = 'login'),
    path('register_line', views.register_line, name = 'register_line'),
    path('register_phone', views.register_phone, name = 'register_phone'),

    path('search_list', views.search_list, name = 'search_list'),
    path('search_carer_detail', views.search_carer_detail, name = 'search_carer_detail'),

    path('booking_patient_info', views.booking_patient_info, name = 'booking_patient_info'),
    path('booking_location', views.booking_location, name = 'booking_location'),
    path('booking_contact', views.booking_contact, name = 'booking_contact'),
    path('booking_confirm', views.booking_confirm, name = 'booking_confirm'),
    
    path('news', views.news, name = 'news'),
    path('news_detail', views.news_detail, name = 'news_detail'),

    path('requirement_list', views.requirement_list, name = 'requirement_list'),
    path('requirement_detail', views.requirement_detail, name = 'requirement_detail'),

    path('become_carer', views.become_carer, name = 'become_carer'),
    path('my_service_setting', views.my_service_setting, name = 'my_service_setting'),
    
    path('my_bank_account', views.my_bank_account, name = 'my_bank_account'),
    path('my_bookings', views.my_bookings, name = 'my_bookings'),
    path('my_booking_detail', views.my_booking_detail, name = 'my_booking_detail'),
    path('my_cases', views.my_cases, name = 'my_cases'),
    path('my_case_detail', views.my_case_detail, name = 'my_case_detail'),
    path('my_care_certificate', views.my_care_certificate, name = 'my_care_certificate'),
    path('my_files', views.my_files, name = 'my_files'),
    path('my_profile', views.my_profile, name = 'my_profile'),
    path('my_edit_profile', views.my_edit_profile, name = 'my_edit_profile'),
    path('my_reviews', views.my_reviews, name = 'my_reviews'),
    path('my_write_review', views.my_write_review, name = 'my_write_review'),
    path('my_notification_setting', views.my_notification_setting, name = 'my_notification_setting'),

    path('request_form_service_type', views.request_form_service_type, name = 'request_form_service_type'),
    path('request_form_patient_info', views.request_form_patient_info, name = 'request_form_patient_info'),
    path('request_form_contact', views.request_form_contact, name = 'request_form_contact'),
    path('request_form_confirm', views.request_form_confirm, name = 'request_form_confirm'),

    path('recommend_carer', views.recommend_carer, name = 'recommend_carer'),

    
]

