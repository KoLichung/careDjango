from django.shortcuts import render ,redirect
from django.http import HttpResponse

import urllib
import json
import os
import datetime
from django.db.models import Avg , Count ,Sum ,Q
from modelCore.models import City, County ,User ,UserServiceLocation ,Review ,Order ,UserLanguage ,Language ,UserServiceShip ,Service
from modelCore.models import UserLicenseShipImage ,License
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
        start_datetime = request.POST.get('datetimepicker_start')
        end_datetime = request.POST.get('datetimepicker_end')
        
        return redirect_params('search_list',{'city':city.id,'county':county,'care_type':care_type,'is_continuous_time':is_continuous_time,'start_datetime':start_datetime,'end_datetime':end_datetime})

    else:
        dict = {}
        dict['citys'] = citys
        dict['city'] = city
        dict['counties'] = counties
        dict['county'] = county

        return render(request, 'web/index.html',{'dict':dict})

def ajax_call_backend(request):
    print("This is ajax")
    obj = {"test": "test"}
    return HttpResponse(json.dumps(obj))

def login(request):
    return render(request, 'web/login.html')

def register_line(request):
    return render(request, 'web/register_line.html')

def register_phone(request):
    return render(request, 'web/register_phone.html')

def search_list(request):
    citys = City.objects.all()
    counties = County.objects.all()
    servants = User.objects.filter(is_servant=True)

    county_name = request.GET.get('county')
    city_id = request.GET.get("city")
    care_type = request.GET.get('care_type')
    is_continuous_time = request.GET.get('is_continuous_time')
    

    if city_id == None:
        city_id = '8'
    city = City.objects.get(id=city_id)

    counties = counties.filter(city=City.objects.get(id=city_id))

    if county_name == None:
        countyName = '全區'
    else:
        if county_name != '全區':
            countyName = County.objects.get(city=city_id,name=county_name)
            county = County.objects.get(city=city_id,name=county_name)
            
        else:
            countyName = '全區'
    dict = {}
    dict['citys'] = citys
    dict['city'] = city
    dict['counties'] = counties
    dict['county'] = countyName
    dict['care_type'] = care_type
    forlooplist = []
    if county_name != None:
        if county_name != '全區':
            user_ids = list(UserServiceLocation.objects.filter(county=county).values_list('user', flat=True))
        else:
            user_ids = list(UserServiceLocation.objects.filter(city=city_id).values_list('user', flat=True))
        servants = servants.filter(id__in=user_ids)
    if request.method == 'POST':
        start_date = request.POST.get('datepicker_startDate')
        end_date = request.POST.get('datepicker_endDate')
        start_time = request.POST.get('timepicker_startTime')
        end_time = request.POST.get('timepicker_endTime')
        is_continuous_time = request.POST.get('is_continuous_time')
        weekdays = request.POST.getlist('weekdays[]')

        if is_continuous_time == 'True':
            time_type = '連續時間'
        else:
            time_type = '每週固定'
        dict['time_type'] = time_type
        if (start_date != '') and (end_date != '') and (start_time != '') and (end_time != ''):
            if is_continuous_time == 'True':
                servants = servants.filter(is_continuous_time=True)
            
            #所選擇的周間跟時段 要符合 servant 的服務時段
            elif weekdays != None:
                # start_date = start_datetime.split('T')[0]
                # end_date = end_datetime.split('T')[0]
                start_time_int = int(start_time.split(':')[0])
                end_time_int = int(end_time.split(':')[1])
                weekdays_num_list = weekdays
                service_time_condition_1 = Q(is_continuous_time=True)
                # service_time_condition_2 = Q(user_weekday__weekday__in=weekdays_num_list, user_weekday__start_time__lte=start_time_int, user_weekday__end_time__gte=end_time_int)
                # queryset = queryset.filter(service_time_condition_1 | service_time_condition_2).distinct()
                for weekdays_num in weekdays_num_list:
                    service_time_condition_2 = Q(user_weekday__weekday=weekdays_num, user_weekday__start_time__lte=start_time_int, user_weekday__end_time__gte=end_time_int)
                    servants = servants.filter(service_time_condition_1 | service_time_condition_2).distinct()
            # 如果一個 servant 已經在某個時段已經有了 1 個 order, 就沒辦法再接另一個 order
            # 2022-07-10

            #所選擇的日期期間/週間/時段, 要在已有的訂單時段之外, 先找出時段內的訂單, 然後找出時段內的人, 最後反過來, 非時段內的人就是可以被篩選
            #1.取出日期期間有交集的訂單
            condition1 = Q(start_datetime__range=[start_date, end_date])
            condition2 = Q(end_datetime__range=[start_date, end_date])
            condition3 = Q(start_datetime__lte=start_date)&Q(end_datetime__gte=end_date)
            orders = Order.objects.filter(condition1 | condition2 | condition3)
            #2.再從 1 取出週間有交集的訂單
            #這邊考慮把 Order 的 weekday 再寫成一個 model OrderWeekDay, 然後再去比較, 像 user__weekday 一樣
            if weekdays != None:
                weekdays_num_list = weekdays
                orders = orders.filter(order_weekday__weekday__in=weekdays_num_list).distinct()
            #3.再從 2 取出時段有交集的訂單
            time_condition_1 = Q(start_time__range=[start_time_int, end_time_int])
            time_condition_2 = Q(end_time__range=[start_time_int, end_time_int])
            time_condition3 = Q(start_time__lte=start_time_int)&Q(end_time__gte=end_time_int)
            orders = orders.filter(time_condition_1 | time_condition_2 | time_condition3)
            order_conflict_servants_id = list(orders.values_list('servant', flat=True))
            servants = servants.filter(~Q(id__in=order_conflict_servants_id))
    
    for servant in servants:
        service_city_ids = list(UserServiceLocation.objects.filter(user=servant).values_list('city', flat=True))
        service_citys = City.objects.filter(id__in=service_city_ids)
        servant_avg_rate= Review.objects.filter(servant=servant,servant_rating__gte=1).aggregate(Avg('servant_rating'))['servant_rating__avg']
        servant_rate_nums = Review.objects.filter(servant=servant,servant_rating__gte=1).aggregate(rating_nums=Count('servant_rating'))['rating_nums']
        
        if care_type == '醫院看護':
            hour_wage = servant.hospital_hour_wage
            half_day_wage = servant.hospital_half_day_wage
            one_day_wage = servant.hospital_one_day_wage
            servants = servants.filter(is_hospital=True)
            print('hospital')
        else:
            if care_type == '居家照顧' :
                servants = servants.filter(is_home=True)
            else:
                hour_wage = servant.home_hour_wage
                half_day_wage = servant.home_half_day_wage
                one_day_wage = servant.home_one_day_wage

        servant_care_type = []
        if servant.is_home == True:
            servant_care_type.append('居家照顧')
        if servant.is_hospital == True:
            servant_care_type.append('醫院看護')
        data = {'servant':servant,'service_citys':service_citys,'servant_avg_rate':servant_avg_rate,'servant_rate_nums':servant_rate_nums,'hour_wage':hour_wage,'half_day_wage':half_day_wage,'one_day_wage':one_day_wage,'servant_care_type':servant_care_type}
        forlooplist.append(data)

    return render(request, 'web/search_list.html',{'dict':dict,'forlooplist':forlooplist})

def search_carer_detail(request):
    servant_phone = request.GET.get('servant')
    reviews_all = request.GET.get('reviews')
    servant = User.objects.get(phone=servant_phone)
    dict = {}
    servant_care_type = []
    if servant.is_home == True:
            servant_care_type.append('居家照顧')
    if servant.is_hospital == True:
        servant_care_type.append('醫院看護')
    language_ids = list(UserLanguage.objects.filter(user=servant).values_list('language', flat=True))
    languages = Language.objects.filter(id__in=language_ids)
    service_ids = list(UserServiceShip.objects.filter(user=servant).values_list('service', flat=True))
    services = Service.objects.filter(id__in=service_ids)
    license_ids = list(UserLicenseShipImage.objects.filter(user=servant).values_list('license', flat=True))
    licences = License.objects.filter(id__in=license_ids,id__gt=3)
    license_not_provide = []
    for license_id in range(1,4):
        if UserLicenseShipImage.objects.filter(user=servant,license=license_id).exists() == False:
            license_not_provide.append(License.objects.get(id=license_id))

    servant_rate_nums = Review.objects.filter(servant=servant,servant_rating__gte=1).aggregate(rating_nums=Count('servant_rating'))['rating_nums']

    if len(Review.objects.filter(servant=servant)) >= 2:
        reviews = Review.objects.filter(servant=servant).order_by('-servant_rating_created_at')[:2]
        if reviews_all != None:
            reviews = Review.objects.filter(servant=servant).order_by('-servant_rating_created_at')
    else:
        reviews = Review.objects.filter(servant=servant).order_by('-servant_rating_created_at')
    user_locations = UserServiceLocation.objects.filter(user=servant)
    location_list = []
    for user_location in user_locations:
        location_list.append({'city':user_location.city,'county':user_location.county,'tranfer_fee':user_location.tranfer_fee})
    dict['servant'] = servant
    dict['care_type'] = servant_care_type
    dict['languages'] = languages
    dict['location_list'] = location_list
    dict['services'] = services
    dict['licences'] = licences
    dict['license_not_provide'] = license_not_provide
    dict['about_me'] = servant.about_me
    dict['servant_rate_nums'] = servant_rate_nums
    dict['reviews'] = reviews
    if request.method == 'POST':
        care_type = request.POST.get('care_type')
        if care_type == '醫院看護':
                hour_wage = servant.hospital_hour_wage
                half_day_wage = servant.hospital_half_day_wage
                one_day_wage = servant.hospital_one_day_wage
        else:
                hour_wage = servant.home_hour_wage
                half_day_wage = servant.home_half_day_wage
                one_day_wage = servant.home_one_day_wage
        dict['hour_wage'] = hour_wage
        dict['half_day_wage'] = half_day_wage
        dict['one_day_wage'] = one_day_wage
        print(care_type,hour_wage)
        return render(request, 'web/search_carer_detail.html',{'dict':dict,})
    
    

    return render(request, 'web/search_carer_detail.html',{'dict':dict,})

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