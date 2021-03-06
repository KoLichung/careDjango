from django.shortcuts import render ,redirect
from django.http import HttpResponse

import urllib
import json
import os
from modelCore.models import City, County

# Create your views here.

def index(request):
    citys = City.objects.all()
    counties = County.objects.all()

    county_id = request.GET.get('county_id')
    city_id = request.GET.get("city_id")

    if city_id == None:
        city_id = '8'
    city = City.objects.get(id=city_id)

    counties = counties.filter(city=City.objects.get(id=city_id))

    if county_id == None:
        county = '全區'
    else:
        if county_id != 'all':
            county = County.objects.get(id=county_id)
        else:
            county = '全區'

    if request.method == 'POST':
        care_type = request.POST.get('care_type')
        is_continuous_time = request.POST.get('is_continuous_time')
        start_date = request.POST.get('datetimepicker_start')
        end_date = request.POST.get('datetimepicker_end')
        
        return redirect_params('search_list',{'city':city,'county':county,'care_type':care_type,'is_continuous_time':is_continuous_time,'start_date':start_date,'end_date':end_date})

    else:
        dict = {}
        dict['citys'] = citys
        dict['city'] = city
        dict['counties'] = counties
        dict['county'] = county

        return render(request, 'web/index.html',{'dict':dict})

def login(request):
    return render(request, 'web/login.html')

def register_line(request):
    return render(request, 'web/register_line.html')

def register_phone(request):
    return render(request, 'web/register_phone.html')

def search_list(request):
    s
    return render(request, 'web/search_list.html')

def search_carer_detail(request):
    return render(request, 'web/search_carer_detail.html')

def booking_patient_info(request):
    return render(request, 'web/booking/patient_info.html')

def booking_location(request):
    return render(request, 'web/booking/location.html')

def booking_contact(request):
    return render(request, 'web/booking/contact.html')

def booking_confirm(request):
    return render(request, 'web/booking/confirm.html')

def news(request):
    return render(request, 'web/news.html')

def news_detail(request):
    return render(request, 'web/news_detail.html')

def requirement_list(request):
    return render(request, 'web/requirement_list.html')

def requirement_detail(request):
    return render(request, 'web/requirement_detail.html')

def become_carer(request):
    return render(request, 'web/become_carer.html')

def my_service_setting(request):
    return render(request, 'web/my/service_setting.html')

def my_bank_account(request):
    return render(request, 'web/my/bank_account.html')
 
def my_bookings(request):
    return render(request, 'web/my/bookings.html')

def my_booking_detail(request):
    return render(request, 'web/my/booking_detail.html')

def my_cases(request):
    return render(request, 'web/my/cases.html')

def my_case_detail(request):
    return render(request, 'web/my/case_detail.html')

def my_care_certificate(request):
    return render(request, 'web/my/care_certificate.html')

def my_files(request):
    return render(request, 'web/my/files.html')

def my_profile(request):
    return render(request, 'web/my/profile.html')

def my_edit_profile(request):
    return render(request, 'web/my/edit_profile.html')

def my_reviews(request):
    return render(request, 'web/my/reviews.html')

def my_write_review(request):
    return render(request, 'web/my/write_review.html')

def my_notification_setting(request):
    return render(request, 'web/my/notification_setting.html')

def request_form_service_type(request):
    return render(request, 'web/request_form/service_type.html')

def request_form_patient_info(request):
    return render(request, 'web/request_form/patient_info.html')

def request_form_contact(request):
    return render(request, 'web/request_form/contact.html')

def request_form_confirm(request):
    return render(request, 'web/request_form/confirm.html')
    
def recommend_carer(request):
    return render(request, 'web/recommend_carer.html')

def redirect_params(url, params=None):
    response = redirect(url)
    if params:
        query_string = urllib.parse.urlencode(params)
        response['Location'] += '?' + query_string
    return response