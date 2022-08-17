from django.shortcuts import render ,redirect
from django.http import HttpResponse ,JsonResponse

import urllib
from datetime import date ,timedelta
import datetime
import json
import os
from time import time
from django.db.models import Avg , Count ,Sum ,Q
from modelCore.models import City, County ,User ,UserServiceLocation ,Review ,Order ,UserLanguage ,Language ,UserServiceShip ,Service
from modelCore.models import UserLicenseShipImage ,License
# Create your views here.

def index(request):
    citys = City.objects.all()
    counties = County.objects.all()

    if request.method == 'POST':
        
        city = request.POST.get('city')
        county = request.POST.get('county')
        care_type = request.POST.get('care_type')
        is_continuous_time = request.POST.get('is_continuous_time')
        start_datetime = request.POST.get('datetimepicker_start')
        end_datetime = request.POST.get('datetimepicker_end')
        weekdays = request.POST.getlist('weekdays[]')
        weekday_list = weekdays
        print(weekday_list)
        weekday_str = ''
        count = 0
        for weekday in weekdays:
            count += 1
            weekday_str += weekday 
            if count < len(weekdays):
                weekday_str += ','
        print(weekday_str)
        return redirect_params('search_list',{'weekday_list':weekday_list, 'city':city,'county':county,'care_type':care_type,'is_continuous_time':is_continuous_time,'weekdays':weekday_str,'start_datetime':start_datetime,'end_datetime':end_datetime})
    
    else:
        dict = {}
        dict['citys'] = citys
        dict['city'] = citys.get(id=8)
        dict['counties'] = counties
        dict['county'] = '全區'

        return render(request, 'web/index.html',{'dict':dict})

    # elif request.is_ajax():
    #     return JsonResponse({'text':'hello world'})

def ajax_refresh_county(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.POST['action'] == 'refresh_county':
            updatedData = urllib.parse.parse_qs(request.body.decode('utf-8'))
            city_id = updatedData['city_id'][0]
            counties = County.objects.filter(city=City.objects.get(id=city_id))
            # countylist = serializers.serialize('json', list(counties))
            data=[]
            for county in counties:
                item = {
                    'id':county.id,
                    'county':county.name,
                }
                data.append(item)
            return JsonResponse({'data':data})

def ajax_return_wage(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.POST['action'] == 'return_wage':
        updatedData = urllib.parse.parse_qs(request.body.decode('utf-8'))
        care_type = updatedData['care_type'][0]
        servant =updatedData['servant'][0]
        servant = User.objects.get(phone=servant)
        print('ajax_return_wage')
        data={}
        if care_type == 'home':
            if servant.home_hour_wage > 0:
                data['hour_wage'] = servant.home_hour_wage
                data['half_day_wage'] = servant.home_half_day_wage
                data['one_day_wage'] = servant.home_one_day_wage
            else:
                data['hour_wage'] = '尚未設定'
                data['half_day_wage'] = '尚未設定'
                data['one_day_wage'] = '尚未設定'
        elif care_type == 'hospital':
            if servant.hospital_hour_wage > 0:
                data['hour_wage'] = servant.hospital_hour_wage
                data['half_day_wage'] = servant.hospital_half_day_wage
                data['one_day_wage'] = servant.hospital_one_day_wage
            else:
                data['hour_wage'] = '尚未設定'
                data['half_day_wage'] = '尚未設定'
                data['one_day_wage'] = '尚未設定'
        return JsonResponse({'data':data})
    
def ajax_cal_rate(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.POST['action'] == 'ajax_cal_rate' :
        updatedData = urllib.parse.parse_qs(request.body.decode('utf-8'))
        servants = User.objects.filter(is_servant=True)
        print(updatedData)
        servant = updatedData['servant'][0]
        servant = User.objects.get(phone=servant)
        care_type = updatedData['care_type'][0]
        start_end_date = updatedData['start_end_date'][0]
        is_continuous_time = updatedData['is_continuous_time'][0]
        print(is_continuous_time)
        startTime = updatedData['startTime'][0]
        endTime = updatedData['endTime'][0]
        start_date = '20' + start_end_date.split(' to ')[0].replace('/','-')
        end_date = '20' +start_end_date.split(' to ')[1].replace('/','-')
        
        if is_continuous_time == 'True':
            # print('is_continuous_time')
            servants = servants.filter(is_continuous_time=True)
            start_time = startTime.split(':')
            end_time = endTime.split(':')
            start_time_int = int(start_time[0]) + float(int(start_time[1])/60)
            end_time_int = int(end_time[0]) + float(int(end_time[1])/60)
            condition1 = Q(start_datetime__range=[start_date, end_date])
            condition2 = Q(end_datetime__range=[start_date, end_date])
            condition3 = Q(start_datetime__lte=start_date)&Q(end_datetime__gte=end_date)
            orders = Order.objects.filter(condition1 | condition2 | condition3).distinct()
            time_condition_1 = Q(start_time__range=[start_time_int, end_time_int])
            time_condition_2 = Q(end_time__range=[start_time_int, end_time_int])
            time_condition3 = Q(start_time__lte=start_time_int)&Q(end_time__gte=end_time_int)
            order_condition = Q((time_condition_1 | time_condition_2 | time_condition3))
            orders = orders.filter(order_condition).distinct()
            order_conflict_servants_id = list(orders.values_list('servant', flat=True))
            servants = servants.filter(~Q(id__in=order_conflict_servants_id))
            if servant in servants:
                if care_type == '醫院看護':
                    hour_wage = servant.hospital_hour_wage
                elif care_type == '居家照顧':
                    hour_wage = servant.home_hour_wage
                print('calculate')
                start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
                print(start_date,end_date)
                total_hours = 0
                for i in range(7):
                    total_hours += (days_count([int(i)], start_date, end_date)) * (end_time_int - start_time_int)                    
                total_money = total_hours * hour_wage
                print(total_money,total_hours)
                data = {
                    'result':'3',
                    'total_hours':total_hours,
                    'total_money':total_money,
                    'hour_wage':hour_wage,
                }
                return JsonResponse({'data':data})
            else:
                data = {'result':'2'}
                return JsonResponse({'data':data})
        else:
            weekdays = updatedData['weekdays[]']
            if (start_date != '') | (end_date != '') | (startTime != '') | (endTime != ''):
                print('1')
                start_time = startTime.split(':')
                end_time = endTime.split(':')
                start_time_int = int(start_time[0]) + float(int(start_time[1])/60)
                end_time_int = int(end_time[0]) + float(int(end_time[1])/60)
                weekdays_num_list = weekdays
                service_time_condition_1 = Q(is_continuous_time=True)
                # service_time_condition_2 = Q(user_weekday__weekday__in=weekdays_num_list, user_weekday__start_time__lte=start_time_int, user_weekday__end_time__gte=end_time_int)
                # queryset = queryset.filter(service_time_condition_1 | service_time_condition_2).distinct()
                for weekdays_num in weekdays_num_list:
                    service_time_condition_2 = Q(user_weekday__weekday=weekdays_num, user_weekday__start_time__lte=start_time_int, user_weekday__end_time__gte=end_time_int)
                    servants = servants.filter(service_time_condition_1 | service_time_condition_2).distinct()
                if servant not in servants:
                    data = {'result':'1'}
                    return JsonResponse({'data':data})
                # 如果一個 servant 已經在某個時段已經有了 1 個 order, 就沒辦法再接另一個 order
                # 2022-07-10
                else:
                    #所選擇的日期期間/週間/時段, 要在已有的訂單時段之外, 先找出時段內的訂單, 然後找出時段內的人, 最後反過來, 非時段內的人就是可以被篩選
                    #1.取出日期期間有交集的訂單
                    condition1 = Q(start_datetime__range=[start_date, end_date])
                    condition2 = Q(end_datetime__range=[start_date, end_date])
                    condition3 = Q(start_datetime__lte=start_date)&Q(end_datetime__gte=end_date)
                    orders = Order.objects.filter(condition1 | condition2 | condition3).distinct()

                    #2.再從 1 取出週間有交集的訂單
                    #這邊考慮把 Order 的 weekday 再寫成一個 model OrderWeekDay, 然後再去比較, 像 user__weekday 一樣
                    weekdays_num_list = weekdays
                    weekday_condition_1 = Q(order_weekday__weekday__in=weekdays_num_list)
                    weedkay_condition_2 =  Q(case__is_continuous_time=True)
                    #3.再從 2 取出時段有交集的訂單
                    time_condition_1 = Q(start_time__range=[start_time_int, end_time_int])
                    time_condition_2 = Q(end_time__range=[start_time_int, end_time_int])
                    time_condition3 = Q(start_time__lte=start_time_int)&Q(end_time__gte=end_time_int)
                    order_condition_1 = Q((weekday_condition_1) & (time_condition_1 | time_condition_2 | time_condition3))
                    order_condition_2 = Q((weedkay_condition_2) & (time_condition_1 | time_condition_2 | time_condition3))
                    orders = orders.filter(order_condition_1|order_condition_2).distinct()
                    order_conflict_servants_id = list(orders.values_list('servant', flat=True))
                    servants = servants.filter(~Q(id__in=order_conflict_servants_id))
                    if servant in servants:
                        if care_type == '醫院看護':
                            hour_wage = servant.hospital_hour_wage
                        elif care_type == '居家照顧':
                            hour_wage = servant.home_hour_wage
                        print('calculate')
                        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
                        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
                        print(start_date,end_date)
                        total_hours = 0
                        for i in weekdays_num_list:
                            total_hours += (days_count([int(i)], start_date, end_date)) * (end_time_int - start_time_int)
                        total_money = total_hours * hour_wage
                        print(total_money,total_hours)
                        data = {
                            'result':'3',
                            'total_hours':total_hours,
                            'total_money':total_money,
                            'hour_wage':hour_wage,
                        }
                        return JsonResponse({'data':data})
                    else:
                        data = {'result':'2'}
                        return JsonResponse({'data':data})


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
    start_datetime = request.GET.get('start_datetime')
    end_datetime = request.GET.get('end_datetime')
    weekdays = request.GET.get('weekdays')
    if start_datetime != '':
        defaultStartDate = '20' + start_datetime.split(' ')[0].replace('/','-')
    else:
        defaultStartDate = ''
    if end_datetime != '':
        defaultEndDate = '20' + end_datetime.split(' ')[0].replace('/','-')
    else:
        defaultEndDate = ''
    weekday_list = weekdays.split(',')
    start_time = ''
    end_time = ''
    if request.method == 'POST':
        
        if request.POST.get('county') != None:
            county_name = request.POST.get('county')
        if request.POST.get('city') != None:
            city_id = request.POST.get("city")
        care_type = request.POST.get('care_type')
        is_continuous_time = request.POST.get('is_continuous_time')
        start_date = request.POST.get('datepicker_startDate')
        end_date = request.POST.get('datepicker_endDate')
        start_time = request.POST.get('timepicker_startTime')
        end_time = request.POST.get('timepicker_endTime')
        is_continuous_time = request.POST.get('is_continuous_time')
        weekdays = request.POST.getlist('weekdays[]')
        weekday_list = weekdays
        defaultStartDate = start_date
        defaultEndDate = end_date
        defaultStartTime = start_time
        defaultEndTime = end_time

        if is_continuous_time == 'True':
                servants = servants.filter(is_continuous_time=True)

            #所選擇的周間跟時段 要符合 servant 的服務時段
        if weekdays != None:
            if (start_date != '') and (end_date != '') and (start_time != '') and (end_time != ''):
                start_time = start_time.split(':')
                end_time = end_time.split(':')
                start_time_int = int(start_time[0]) + float(int(start_time[1])/60)
                end_time_int = int(end_time[0]) + float(int(end_time[1])/60)
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
                orders = Order.objects.filter(condition1 | condition2 | condition3).distinct()

                #2.再從 1 取出週間有交集的訂單
                #這邊考慮把 Order 的 weekday 再寫成一個 model OrderWeekDay, 然後再去比較, 像 user__weekday 一樣
                weekdays_num_list = weekdays
                weekday_condition_1 = Q(order_weekday__weekday__in=weekdays_num_list)
                weedkay_condition_2 =  Q(case__is_continuous_time=True)
                #3.再從 2 取出時段有交集的訂單
                time_condition_1 = Q(start_time__range=[start_time_int, end_time_int])
                time_condition_2 = Q(end_time__range=[start_time_int, end_time_int])
                time_condition3 = Q(start_time__lte=start_time_int)&Q(end_time__gte=end_time_int)
                order_condition_1 = Q((weekday_condition_1) & (time_condition_1 | time_condition_2 | time_condition3))
                order_condition_2 = Q((weedkay_condition_2) & (time_condition_1 | time_condition_2 | time_condition3))
                orders = orders.filter(order_condition_1|order_condition_2).distinct()
                order_conflict_servants_id = list(orders.values_list('servant', flat=True))
                print(orders)
                servants = servants.filter(~Q(id__in=order_conflict_servants_id))
            else:
                weekdays_num_list = weekdays
                service_time_condition_1 = Q(is_continuous_time=True)
                for weekdays_num in weekdays_num_list:
                    service_time_condition_2 = Q(user_weekday__weekday__in=weekdays_num)
                    servants = servants.filter(service_time_condition_1 | service_time_condition_2).distinct()
    
    if city_id == None:
        city_id = '8'
    city = City.objects.get(id=city_id)
    counties = counties.filter(city=City.objects.get(id=city_id))

    if county_name == None:
        county_name = '全區'
    else:
        if county_name != '全區':
            print(county_name)
            county_name = County.objects.get(city=city_id,name=county_name)
            
        else:
            county_name = '全區'
    if care_type == '居家照顧':
            servants = servants.filter(is_home=True)

    elif care_type == '醫院看護':
        servants = servants.filter(is_hospital=True)

    dict = {}
    dict['citys'] = citys
    dict['city'] = city
    dict['counties'] = counties
    dict['county'] = county_name
    dict['care_type'] = care_type
    if start_time != None and start_time != '':
        dict['start_time'] = defaultStartTime
        print(dict['start_time'])
    if end_time != None and end_time != '' :
        dict['end_time'] = defaultEndTime
    
    if county_name != None:
        if county_name != '全區':
            user_ids = list(UserServiceLocation.objects.filter(county=county_name).values_list('user', flat=True))
        else:
            user_ids = list(UserServiceLocation.objects.filter(city=city_id).values_list('user', flat=True))
        servants = servants.filter(id__in=user_ids)
    if is_continuous_time == 'True':
        time_type = '連續時間'
    else:
        time_type = '每週固定'
    dict['time_type'] = time_type
    weekday_str = ''
    count = 0
    for weekday in weekdays:
        count += 1
        weekday_str += weekday 
        if count < len(weekdays):
            weekday_str += ','

    return render(request, 'web/search_list.html',{'dict':dict,'servants':servants,'care_type':care_type,'defaultStartDate':defaultStartDate,'defaultEndDate':defaultEndDate,'weekdays':weekday_str,'weekday_list':weekday_list,'is_continuous_time':is_continuous_time})

def search_carer_detail(request):
    citys = City.objects.all()
    counties = County.objects.all()
    county_name = request.GET.get('county')
    city_id = request.GET.get("city")
    if city_id == None:
        city_id = '8'
    city = City.objects.get(id=city_id)
    counties = counties.filter(city=City.objects.get(id=city_id))

    if county_name == None:
        county_name = '全區'
    else:
        if county_name != '全區':
            county_name = County.objects.get(city=city_id,name=county_name)
            
        else:
            county_name = '全區'
    start_date = ''
    end_date = ''
    servant_phone = request.GET.get('servant')
    reviews_all = request.GET.get('reviews')
    care_type = request.GET.get('care_type')
    is_continuous_time = request.GET.get('is_continuous_time')
    weekdays = request.GET.get('weekdays')
    start_date = request.GET.get('StartDate')
    end_date = request.GET.get('EndDate')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    if (start_date != None and start_date != '') & (end_date != None and end_date != ''):
        start_date_str = start_date.split('-')[0][2:4] + '/' + start_date.split('-')[1] + '/' +start_date.split('-')[2]
        end_date_str = end_date.split('-')[0][2:4] + '/' +end_date.split('-')[1] + '/' +end_date.split('-')[2]
        defaultStartEndDate = start_date_str + ' to ' + end_date_str
    else:
        defaultStartEndDate = ''
    weekday_list = weekdays.split(',')
    
    servant = User.objects.get(phone=servant_phone)
        
    servant_care_type = []
    if servant.is_home == True:
            servant_care_type.append('居家照顧')
    if servant.is_hospital == True:
        servant_care_type.append('醫院看護')

    license_not_provide = []
    for license_id in range(1,4):
        if UserLicenseShipImage.objects.filter(user=servant,license=license_id).exists() == False:
            license_not_provide.append(License.objects.get(id=license_id))

    if len(Review.objects.filter(servant=servant)) >= 2:
        reviews = Review.objects.filter(servant=servant).order_by('-servant_rating_created_at')[:2]
        if reviews_all != None:
            reviews = Review.objects.filter(servant=servant).order_by('-servant_rating_created_at')
    else:
        reviews = Review.objects.filter(servant=servant).order_by('-servant_rating_created_at')

    if request.method == 'POST':
        care_type = request.POST.get('care_type')
        city = request.POST.get('city')
        county = request.POST.get('county')
        start_end_date = request.POST.get('strat_end_date')
        is_continuous_time = request.POST.get('is_continuous_time')
        start_time = request.POST.get('timepicker_startTime')
        end_time = request.POST.get('timepicker_endTime')
        weekdays = request.POST.getlist('weekdays[]')
        defaultStartEndDate = start_end_date
        return redirect_params('booking_patient_info',{'city':city,'county':county,'care_type':care_type,'is_continuous_time':is_continuous_time,'strat_end_date':strat_end_date,'start_time':start_time,'servant_care_type':servant_care_type})
    
    
    defaultStartTime = start_time
    defaultEndTime = end_time
    return render(request, 'web/search_carer_detail.html',{'weekdays':weekdays, 'cityName':city,'citys':citys,'countyName':county_name,'counties':counties, 'is_continuous_time':is_continuous_time, 'defaultStartTime':defaultStartTime,'defaultEndTime':defaultEndTime,'defaultStartEndDate':defaultStartEndDate,'weekday_list':weekday_list, 'servant':servant,'license_not_provide':license_not_provide,'reviews':reviews,'citys':citys,'counties':counties,'care_type':care_type})


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

def days_count(weekdays: list, start: date, end: date):
    dates_diff = end-start
    days = [start + timedelta(days=i) for i in range(dates_diff.days)]
    return len([day for day in days if day.weekday() in weekdays])