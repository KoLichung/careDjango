from unicodedata import category
from django.shortcuts import render ,redirect
from django.http import HttpResponse ,JsonResponse ,HttpResponseRedirect 
from django.core.files.storage import FileSystemStorage
from io import StringIO
from django.template.loader import get_template
from django.template import Context
from django.utils import timezone
from messageApp.tasks import *

import urllib
from datetime import date ,timedelta
import datetime
from django.contrib import messages
# import tkinter as tk
# from tkinter import messagebox
import json
from urllib import parse
import requests
from time import time
import logging
from django.contrib import auth
from modelCore.forms import *
from django.contrib.auth import authenticate, logout
from django.db.models import Avg , Count ,Sum ,Q
from modelCore.models import City, County ,User ,UserServiceLocation ,Review ,Order ,UserLanguage ,Language ,UserServiceShip ,Service ,UserWeekDayTime
from modelCore.models import UserLicenseShipImage ,License ,Case ,OrderIncreaseService ,TempCase ,DiseaseCondition ,BodyCondition ,CaseServiceShip ,AssistancePost
from modelCore.models import CaseBodyConditionShip, CaseDiseaseShip ,BlogCategory, BlogPostCategoryShip ,OrderWeekDay ,ChatRoom ,ChatroomUserShip ,ChatroomMessage
# Create your views here.

logger = logging.getLogger(__file__)
def index(request):
    citys = City.objects.all()

    if request.method == 'POST':
        
        city = request.POST.get('city')
        care_type = request.POST.get('care_type')
        is_continuous_time = request.POST.get('is_continuous_time')
        start_date = request.POST.get('datepicker_startDate')
        end_date = request.POST.get('datepicker_endDate')
        start_time = request.POST.get('timepicker_startTime')
        end_time = request.POST.get('timepicker_endTime')
        weekdays = request.POST.getlist('weekdays[]')
        weekday_list = weekdays
        weekday_str = ''
        count = 0
        for weekday in weekdays:
            count += 1
            weekday_str += weekday 
            if count < len(weekdays):
                weekday_str += ','
        print(weekday_str)
        return redirect_params('search_list',{'weekday_list':weekday_list, 'city':city,'care_type':care_type,'is_continuous_time':is_continuous_time,'weekdays':weekday_str,'start_date':start_date,'end_date':end_date,'start_time':start_time,'end_time':end_time})
    
    else:
        dict = {}
        dict['citys'] = citys

        return render(request, 'web/index.html',{'dict':dict})

def ajax_post_image(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' :
        print(request.files)
        # isthisFile=request.files.get('file')
        # print(isthisFile)
        # updatedData = urllib.parse.parse_qs(request.body.decode('utf-8'))
        # print(updatedData)
        return JsonResponse({'data':'ajax'})

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
        servants = User.objects.filter(is_servant_passed=True)
        servants = servants.exclude(is_home=False,is_hospital=False)
        print(updatedData)
        servant_id = updatedData['servant'][0]
        servant = User.objects.get(id=servant_id)
        care_type = updatedData['care_type'][0]
        start_end_date = updatedData['start_end_date'][0]
        is_continuous_time = updatedData['is_continuous_time'][0]
        startTime = updatedData['startTime'][0]
        endTime = updatedData['endTime'][0]
        city_id = updatedData['city_id'][0]
        start_date = '20' + start_end_date.split(' to ')[0].replace('/','-')
        end_date = '20' +start_end_date.split(' to ')[1].replace('/','-')
        transfer_fee = UserServiceLocation.objects.get(user=servant,city=City.objects.get(id=city_id)).transfer_fee
        print(is_continuous_time)
        if is_continuous_time == 'True':
            servants = servants.filter(is_continuous_time=True)
            if servant not in servants:
                data = {'result':'1'}
                return JsonResponse({'data':data})
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
            StartDate = datetime.datetime.strptime(start_date,'%Y-%m-%d').date()
            EndDate = datetime.datetime.strptime(end_date,'%Y-%m-%d').date()
            StartTime = datetime.datetime.strptime(startTime,'%H:%M').time()
            EndTime = datetime.datetime.strptime(endTime,'%H:%M').time()
            start_datetime = datetime.datetime.combine(StartDate,StartTime)
            end_datetime = datetime.datetime.combine(EndDate,EndTime)
            if servant in servants:     
                number_of_transfer = 1
                amount_transfer_fee = transfer_fee * 1
                diff = end_datetime - start_datetime
                days, seconds = diff.days, diff.seconds
                hours = days * 24 + seconds // 3600
                minutes = (seconds % 3600) // 60
                total_hours = hours + round(minutes/60)
                if care_type == 'home':
                    if total_hours < 12:
                        wage = servant.home_hour_wage
                    elif total_hours >=12 and total_hours < 24:
                        wage = round(servant.home_half_day_wage/12)
                    else:
                        wage = round(servant.home_one_day_wage/24)
                elif care_type == 'hospital':
                    if total_hours < 12:
                        wage = servant.hospital_hour_wage
                    elif total_hours >=12 and total_hours < 24:
                        wage = round(servant.hospital_half_day_wage/12)
                    else:
                        wage = round(servant.hospital_one_day_wage/24)             
                base_money = total_hours * wage 
                total_money = base_money + amount_transfer_fee
                print(total_money,'test')
                data = {
                    'result':'3',
                    'total_hours':total_hours,
                    'base_money':base_money,
                    'hour_wage':wage,
                    'transfer_fee':transfer_fee,
                    'number_of_transfer':number_of_transfer,
                    'amount_transfer_fee':amount_transfer_fee,
                    'total_money':total_money,
                }
                print('data',data)
                if 'increase_service[]' in updatedData:
                    increase_service_ids = updatedData['increase_service[]']
                    print(increase_service_ids)
                    increase_service_data = {}
                    count = 0
                    for service_id in increase_service_ids:
                        count += 1
                        service = Service.objects.get(id=service_id)
                        increase_percent = UserServiceShip.objects.get(user=servant,service=service).increase_percent
                        increase_money = round(total_money * increase_percent / 100)
                        total_money += increase_money
                        increase_data = {
                            'service' : service.name,
                            'increase_percent' : increase_percent,
                            'increase_money':increase_money,
                        }
                        increase_service_data['data'+str(count)] = increase_data
                    print(increase_service_data)
                    data['total_money'] = total_money
                    return JsonResponse({'data':data,'increase_service_data':increase_service_data})
                else:
                    return JsonResponse({'data':data})
            else:
                data = {'result':'2'}
                return JsonResponse({'data':data})
        else:
            weekdays = updatedData['weekdays[]']
            print('e')
            if (start_date != '') | (end_date != '') | (startTime != '') | (endTime != ''):
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
                    weekday_condition_1 = Q(order_weekdays__weekday__in=weekdays_num_list)
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
                        print(servant)
                        one_day_work_hours = float(end_time_int) - float(start_time_int)
                        print(one_day_work_hours)
                        if care_type == 'home':
                            if one_day_work_hours < 12:
                                wage = servant.home_hour_wage
                            elif one_day_work_hours >=12 and one_day_work_hours < 24:
                                wage = round(servant.home_half_day_wage/12)
                        elif care_type == 'hospital':
                            if one_day_work_hours < 12:
                                wage = servant.hospital_hour_wage
                            elif one_day_work_hours >=12 and one_day_work_hours < 24:
                                wage = round(servant.hospital_half_day_wage/12)
                        print(wage)
                        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
                        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
                        total_hours = 0
                        number_of_transfer = 0
                        for i in weekdays_num_list:
                            number_of_transfer += (days_count([int(i)], start_date, end_date))
                            total_hours += (days_count([int(i)], start_date, end_date)) * (end_time_int - start_time_int)
                        
                        amount_transfer_fee = transfer_fee * number_of_transfer
                        base_money = total_hours * wage 
                        total_money = base_money + amount_transfer_fee
                        data = {
                            'result':'3',
                            'total_hours':total_hours,
                            'base_money':base_money,
                            'hour_wage':wage,
                            'transfer_fee':transfer_fee,
                            'number_of_transfer':number_of_transfer,
                            'amount_transfer_fee':amount_transfer_fee,
                            'total_money':total_money,

                        }
                        print(data)
                        if 'increase_service[]' in updatedData:
                            increase_service_ids = updatedData['increase_service[]']
                            print(increase_service_ids)
                            increase_service_data = {}
                            count = 0
                            for service_id in increase_service_ids:
                                count += 1
                                service = Service.objects.get(id=service_id)
                                increase_percent = UserServiceShip.objects.get(user=servant,service=service).increase_percent
                                increase_money = round(total_money * increase_percent / 100)
                                total_money += increase_money
                                increase_data = {
                                    'service' : service.name,
                                    'increase_percent' : increase_percent,
                                    'increase_money':increase_money,
                                    
                                }
                                increase_service_data['data'+str(count)] = increase_data
                           
                            data['total_money'] = total_money
                            return JsonResponse({'data':data,'increase_service_data':increase_service_data})
                        else:
                            return JsonResponse({'data':data})
                    else:
                        data = {'result':'2'}
                        return JsonResponse({'data':data})

def login(request):
    if request.method == 'POST' and 'login'in request.POST :
        phone = request.POST['phone']
        password = request.POST['password']
        print(phone,password)
        user = authenticate(request, phone=phone, password=password)
        if user is not None:
            auth.login(request, user)
            print('is_user')
            return redirect('index')
        else:
            print('not user')
            return redirect('login')
    elif request.method == 'POST' and 'line_login' in request.POST:
        auth_url = 'https://access.line.me/oauth2/v2.1/authorize?'
        # call_back = 'http://202.182.105.11/' + redirect_to
        call_back = 'http://202.182.105.11/web/login_line?next=/web/index'

        print(call_back)
        data = {
            'response_type': 'code',
            'client_id': '1657316694',
            'redirect_uri': call_back,
            'state': 'abcde',
        }
        query_str = urllib.parse.urlencode(data) + '&scope=profile%20openid%20email'
        login_url = auth_url + query_str
        print(login_url)
        return redirect(login_url) 

    return render(request, 'web/login.html')

def register_line(request):
    line_id = request.GET.get('line_id', '')
    print(line_id)
    if request.method == 'POST' and line_id != None :
        userName = request.POST.get('userName')
        phone = request.POST.get('phone')
        
        if User.objects.filter(phone=phone,name=userName).exists() != False:
            user = User.objects.get(name=userName,phone=phone)
            user.line_id = line_id
            user.save()
            auth.login(request, user)
            print(request.user)
            return redirect('index')
        else:
            user = User()
            user.name = userName
            user.phone = phone
            user.line_id = line_id
            user.save()
            auth.login(request, user)
            print(request.user)
            return redirect('index')

    
    return render(request, 'web/register_line.html')

def login_line(request):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = "https://api.line.me/oauth2/v2.1/token"
    code = request.GET.get('code')
    FormData = {
        'grant_type': 'authorization_code',
        'client_id': '1657316694',
        'client_secret': 'd7751034c13427e80df2818ce86d3a26',
        'code': code,
        'redirect_uri': 'http://202.182.105.11/web/login_line?next=/web/index' ,
    }
    data = parse.urlencode(FormData)
    resp = requests.post(url, headers=headers, data=data)
    id_token = json.loads(resp.text)['id_token']
    postdata = {
        'id_token': id_token,
        'client_id': '1657316694',
    }
    get_info_url = 'https://api.line.me/oauth2/v2.1/verify'
    get_info_resp = requests.post(get_info_url, headers=headers, data=postdata)
    line_id = json.loads(get_info_resp.text)['sub']
    if User.objects.filter(line_id=line_id).exists() != True:
        print('line is not register')
        return redirect_params('register_line',{'line_id':line_id})
    else:
        user = User.objects.get(line_id=line_id)
        if user is not None:
            auth.login(request, user)
            print(request.user)
            return redirect('index')
        else:
            print('not user')
            return redirect_params('login')

def register_phone(request):
    if request.method == 'POST' and 'register'in request.POST :
        username = request.POST['userName']
        phone = request.POST['phone']
        password = request.POST['password']
        if User.objects.filter(phone=phone).exists() != False:
            user = authenticate(request, phone=phone, password=password)
            if user is not None and user.name == username :
                auth.login(request, user)
                return redirect('index')
            else:
                return render(request, 'web/register_phone.html',{'alert_flag': True})
        else:
            user = User()
            user.name = username
            user.phone = phone
            user.set_password(password)
            user.save()
            auth.login(request, user)
            print(request.user)
            return redirect('index')
    elif request.method == 'POST' and 'line_login' in request.POST:
        auth_url = 'https://access.line.me/oauth2/v2.1/authorize?'
        # call_back = 'http://202.182.105.11/' + redirect_to
        call_back = 'http://202.182.105.11/web/login_line?next=/web/index'

        print(call_back)
        data = {
            'response_type': 'code',
            'client_id': '1657316694',
            'redirect_uri': call_back,
            'state': 'abcde',
        }
        query_str = urllib.parse.urlencode(data) + '&scope=profile%20openid%20email'
        login_url = auth_url + query_str
        print(login_url)
        return redirect(login_url) 
    return render(request, 'web/register_phone.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def search_list(request):
    
    citys = City.objects.all()
    servants = User.objects.filter(is_servant_passed=True)
    servants = servants.exclude(is_home=False,is_hospital=False)
    city_id = request.GET.get("city")
    care_type = request.GET.get('care_type')
    is_continuous_time = request.GET.get('is_continuous_time')
    start_date= request.GET.get('start_date')
    end_date= request.GET.get('end_date')
    print(start_date,end_date)
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    weekdays = request.GET.get('weekdays')

    if start_date != '':
        defaultStartDate = start_date
    else:
        defaultStartDate = ''

    if end_date != '':
        defaultEndDate = end_date
    else:
        defaultEndDate = ''

    if start_time != '':
        defaultStartTime = start_time
    else:
        defaultStartTime = ''
        
    if end_time != '':
        defaultEndTime = end_time
    else:
        defaultEndTime = ''

    weekday_str = ''
    count = 0
    if weekdays != None:
        weekday_list = weekdays.split(',')
        
        for weekday in weekdays:
            count += 1
            weekday_str += weekday 
            if count < len(weekdays):
                weekday_str += ','
    else:
        weekday_list = []
    if request.method == 'POST':
        # if 'request_form' in request.POST:
        #     if request.user.is_authenticated:
        #         return redirect('request_form_service_type')
        #     else:
        #         return redirect('login')

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
        print(servants,'1')
        print(is_continuous_time)
        if is_continuous_time == 'True':
                servants = servants.filter(is_continuous_time=True)
        print(servants,'2')
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
                weekday_condition_1 = Q(order_weekdays__weekday__in=weekdays_num_list)
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
    print(servants,'3')
    if city_id == None:
        city_id = '8'
    city = City.objects.get(id=city_id)

    print(servants,'4')
    if care_type == '居家照顧':
        servants = servants.filter(is_home=True)
        print('is_home',servants)

    elif care_type == '醫院看護':
        servants = servants.filter(is_hospital=True)
    print(servants,'5')
    dict = {}
    dict['citys'] = citys
    dict['city'] = city
    dict['care_type'] = care_type
    if start_time != None and start_time != '':
        dict['start_time'] = defaultStartTime
        print(dict['start_time'])
    if end_time != None and end_time != '' :
        dict['end_time'] = defaultEndTime
    print(servants)
    user_ids = list(UserServiceLocation.objects.filter(city=city_id).values_list('user', flat=True))
    print(user_ids)
    servants = servants.filter(id__in=user_ids)
    print(servants)
    if is_continuous_time == 'True':
        time_type = '連續時間'
    else:
        time_type = '每週固定'
    dict['time_type'] = time_type
    if defaultStartDate == None:
        defaultStartDate = ''
    if defaultEndDate == None:
        defaultEndDate = ''
    return render(request, 'web/search_list.html',{'dict':dict,'servants':servants,'care_type':care_type,'defaultStartDate':defaultStartDate,'defaultEndDate':defaultEndDate,'weekdays':weekday_str,'weekday_list':weekday_list,'is_continuous_time':is_continuous_time})

def search_carer_detail(request):
    citys = City.objects.all()
    city_id = request.GET.get("city")
    if city_id == None:
        city_id = '8'
    city = City.objects.get(id=city_id)
    start_date = ''
    end_date = ''
    servant_id = request.GET.get('servant')
    reviews_all = request.GET.get('reviews')
    care_type = request.GET.get('care_type')
    is_continuous_time = request.GET.get('is_continuous_time')
    weekdays = request.GET.get('weekdays')
    start_date = request.GET.get('StartDate')
    end_date = request.GET.get('EndDate')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    if care_type == '居家照顧':
        care_type = 'home'
    elif care_type == '醫院看護':
        care_type = 'hospital'
    if (start_date != None and start_date != '') & (end_date != None and end_date != ''):
        start_date_str = start_date.split('-')[0][2:4] + '/' + start_date.split('-')[1] + '/' +start_date.split('-')[2]
        end_date_str = end_date.split('-')[0][2:4] + '/' +end_date.split('-')[1] + '/' +end_date.split('-')[2]
        defaultStartEndDate = start_date_str + ' to ' + end_date_str
    else:
        defaultStartEndDate = ''
    if weekdays != None:
        weekday_list = weekdays.split(',')
    else:
        weekday_list = []
    
    servant = User.objects.get(id=servant_id)
        
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
    defaultStartTime = start_time
    defaultEndTime = end_time
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            if user == servant:
                return render(request, 'web/search_carer_detail.html',{'servant_care_type':servant_care_type, 'weekdays':weekdays, 'cityName':city,'citys':citys, 'is_continuous_time':is_continuous_time, 'defaultStartTime':defaultStartTime,'defaultEndTime':defaultEndTime,'defaultStartEndDate':defaultStartEndDate,'weekday_list':weekday_list, 'servant':servant,'license_not_provide':license_not_provide,'reviews':reviews,'citys':citys,'care_type':care_type,'alert_flag': True})
            else:
                care_type = request.POST.get('care_type')
                city = request.POST.get('city')
                start_end_date = request.POST.get('start_end_date')
                is_continuous_time = request.POST.get('is_continuous_time')
                start_time = request.POST.get('timepicker_startTime')
                end_time = request.POST.get('timepicker_endTime')
                weekdays = request.POST.getlist('weekdays[]')
                defaultStartEndDate = start_end_date
                start_date = start_end_date.split(' to ')[0]
                end_date = start_end_date.split(' to ')[1]
                start_date = datetime.datetime.strptime(start_date,"%y/%m/%d")
                end_date = datetime.datetime.strptime(end_date,"%y/%m/%d")
                print(care_type)
                weekday_str = ''
                count = 0
                for weekday in weekdays:
                    count += 1
                    weekday_str += weekday 
                    if count < len(weekdays):
                        weekday_str += ','
                if TempCase.objects.filter(user=user,servant=servant,is_booking=True).exists() != False:
                    tempcase = TempCase.objects.get(user=user,servant=servant,is_booking=True)
                else:
                    tempcase = TempCase()
                tempcase.user = user
                tempcase.servant = servant
                tempcase.is_booking = True
                tempcase.care_type = care_type
                tempcase.city = City.objects.get(id=city).name
                if start_time != None: 
                    start_time = start_time.split(':')
                    start_time_int = int(start_time[0]) + float(int(start_time[1])/60)
                    tempcase.start_time = start_time_int
                if end_time != None:
                    end_time = end_time.split(':')
                    end_time_int = int(end_time[0]) + float(int(end_time[1])/60)
                    tempcase.end_time = end_time_int
                if start_date != None: 
                    tempcase.start_datetime = start_date
                if end_date != None:
                    tempcase.end_datetime = end_date
                if is_continuous_time == 'True':
                    tempcase.is_continuous_time = True
                else:
                    tempcase.is_continuous_time = False
                    weekdays = request.POST.getlist('weekdays[]')
                    weekday_str = ''
                    count = 0
                    for weekday in weekdays:
                        count += 1
                        weekday_str += weekday 
                        if count < len(weekdays):
                            weekday_str += ','
                    tempcase.weekday = weekday_str
                tempcase.save()
                return redirect_params('booking_patient_info',{'weekdays':weekday_str, 'city':city,'care_type':care_type,'is_continuous_time':is_continuous_time,'start_end_date':start_end_date,'start_time':start_time,'end_time':end_time,'servant':servant.id})
        else:
            return redirect('login')
    defaultStartTime = start_time
    defaultEndTime = end_time
    return render(request, 'web/search_carer_detail.html',{'servant_care_type':servant_care_type, 'weekdays':weekdays, 'cityName':city,'citys':citys, 'is_continuous_time':is_continuous_time, 'defaultStartTime':defaultStartTime,'defaultEndTime':defaultEndTime,'defaultStartEndDate':defaultStartEndDate,'weekday_list':weekday_list, 'servant':servant,'license_not_provide':license_not_provide,'reviews':reviews,'citys':citys,'care_type':care_type})

def booking_patient_info(request):
    user = request.user
    servant_id = request.GET.get('servant')
    servant = User.objects.get(id=servant_id)
    citys = City.objects.all()
    if TempCase.objects.filter(user=user,servant=servant,is_booking=True).exists() :
        last_tempcase = TempCase.objects.get(user=user,servant=servant,is_booking=True)
        care_type = last_tempcase.care_type
        start_date = str(last_tempcase.start_datetime.date())
        end_date = str(last_tempcase.end_datetime.date())
        start_date = start_date.split('-')
        end_date = end_date.split('-')
        start_end_date = start_date[0].split('20')[1] + "/" + start_date[1] + "/" + start_date[2] + " to " + end_date[0].split('20')[1] + "/" + end_date[1] + "/" + end_date[2]
        city = City.objects.get(name=last_tempcase.city)
        city_id = city.id
        is_continuous_time = str(last_tempcase.is_continuous_time)
        if is_continuous_time == 'False':
            weekdays = last_tempcase.weekday
            weekday_list = weekdays.split(',')
        else:
            weekday_list = []
        start_time_int = last_tempcase.start_time
        end_time_int = last_tempcase.end_time
        start_time = str(int(start_time_int)) + ':' + str(int((float(start_time_int)-int(start_time_int))*60))
        end_time = str(int(end_time_int)) + ':' + str(int((float(end_time_int)-int(end_time_int))*60))
        start_time = datetime.datetime.strptime(start_time,"%H:%M")
        end_time = datetime.datetime.strptime(end_time,"%H:%M")
        start_time = start_time.strftime("%H:%M")
        end_time = end_time.strftime("%H:%M")
        patient_name = last_tempcase.name
        gender = last_tempcase.gender
        weight = last_tempcase.weight
        age = last_tempcase.age
        disease = last_tempcase.disease
        disease_remark = last_tempcase.disease_remark
        body_condition = last_tempcase.body_condition
        conditions_remark = last_tempcase.conditions_remark
        service = last_tempcase.service
        increase_service = last_tempcase.increase_service
        disease_list = []
        if disease != None and disease != '':
            disease_Idlist = disease.split(',')
            for diseaseId in disease_Idlist:
                disease_list.append(DiseaseCondition.objects.get(id=diseaseId))
        else:
            disease_Idlist = []
        if '1' in disease_Idlist:
            disease_none = True
        else:
            disease_none = False
        
        body_condition_list = []
        if body_condition != None and body_condition != '' :
            body_condition_Idlist = body_condition.split(',')
            for body_condition_id in body_condition_Idlist:
                body_condition_list.append(BodyCondition.objects.get(id=body_condition_id))
        else:
            body_condition_Idlist = []
        if '1' in body_condition_Idlist:
            body_condition_none = True
        else:
            body_condition_none = False

        if service != None and service != '' :
            service_Idlist = service.split(',')
        else:
            service_Idlist = []
        service_list = []
        for service_id in service_Idlist:
            service_list.append(Service.objects.get(id=service_id))
        
        if increase_service != None and increase_service != '' :
            increase_service_Idlist = increase_service.split(',')
        else:
            increase_service_Idlist = []
        increase_service_list = []
        for increase_service_id in increase_service_Idlist:
            increase_service_list.append(UserServiceShip.objects.get(user=servant,service=Service.objects.get(id=increase_service_id)))
        print(increase_service_list)
    else:
        return redirect_params('search_carer_detail',{'servant':servant})
    
    start_date = start_end_date.split(' to ')[0]
    end_date = start_end_date.split(' to ')[1]
    start_date = datetime.datetime.strptime(start_date,"%y/%m/%d")
    end_date = datetime.datetime.strptime(end_date,"%y/%m/%d")
    start_date_str = start_date.strftime("%m/%d")
    end_date_str = end_date.strftime("%m/%d")
    diseases = DiseaseCondition.objects.all().order_by('id')[1:]
    body_conditions = BodyCondition.objects.all().order_by('id')[1:]
    services = Service.objects.all().order_by('id')[4:]
    weekday_str = ''
    count = 0
    for weekday in weekday_list:
        count += 1
        weekday_str += weekday 
        if count < len(weekday_list):
            weekday_str += ','
    increase_services = Service.objects.filter(is_increase_price=True).order_by('id')
    for service in increase_services:
        if UserServiceShip.objects.filter(user=servant, service=service).count() == 0:
            UserServiceShip.objects.create(user=servant,service=service)
    increase_service_ships = UserServiceShip.objects.filter(user=servant).order_by('service')[:4]
    if request.method == 'POST' :
        patient_name = request.POST.get('patient_name')
        gender = request.POST.get('gender')
        weight = request.POST.get('weight')
        age = request.POST.get('age')
        disease_none = request.POST.get('disease_none')
        diseases_list = request.POST.getlist('diseases[]')
        disease_text = request.POST.get('disease_text')
        body_condition_none = request.POST.get('body_condition_none')
        body_conditions_list = request.POST.getlist('body_conditions[]')
        body_condition_note = request.POST.get('body_condition_note')
        services_list = request.POST.getlist('services[]')
        increase_services_list = request.POST.getlist('increase_services[]')
        care_type = request.POST.get('care_type')
        city = request.POST.get('city')
        start_end_date = request.POST.get('start_end_date')
        is_continuous_time = request.POST.get('is_continuous_time')
        start_time = request.POST.get('timepicker_startTime')
        end_time = request.POST.get('timepicker_endTime')
        if TempCase.objects.filter(user=user,servant=servant,is_booking=True).exists() :
            tempcase = TempCase.objects.get(user=user,servant=servant,is_booking=True)
        else:
            tempcase = TempCase()
        tempcase.user = user
        tempcase.servant = servant
        tempcase.care_type = care_type
        tempcase.city = City.objects.get(id=city).name
        tempcase.start_datetime = start_date
        tempcase.end_datetime = end_date
        if start_time != None: 
            start_time = start_time.split(':')
            start_time_int = int(start_time[0]) + float(int(start_time[1])/60)
            tempcase.start_time = start_time_int
        if end_time != None:
            end_time = end_time.split(':')
            end_time_int = int(end_time[0]) + float(int(end_time[1])/60)
            tempcase.end_time = end_time_int
        if is_continuous_time == 'True':
            tempcase.is_continuous_time = True
        else:
            tempcase.is_continuous_time = False
            weekdays = request.POST.getlist('weekdays[]')
            weekday_str = ''
            count = 0
            for weekday in weekdays:
                count += 1
                weekday_str += weekday 
                if count < len(weekdays):
                    weekday_str += ','
            tempcase.weekday = weekday_str
        tempcase.name = patient_name
        tempcase.gender = gender
        tempcase.weight = weight
        tempcase.age = age
        if disease_none != None:
            tempcase.disease = '1'
        else:
            disease_str = ''
            count = 0
            for disease in diseases_list:
                count += 1
                disease_str += disease 
                if count < len(diseases_list):
                    disease_str += ','
            tempcase.disease = disease_str
        tempcase.disease_remark = disease_text

        if body_condition_none != None:
            tempcase.body_condition = '1'
        else:
            body_condition_str = ''
            count = 0
            for body_condition in body_conditions_list:
                count += 1
                body_condition_str += body_condition 
                if count < len(body_conditions_list):
                    body_condition_str += ','
            tempcase.body_condition = body_condition_str
        tempcase.conditions_remark = body_condition_note

        if services_list != None:
            service_str = ''
            count = 0
            for service in services_list:
                count += 1
                service_str += service 
                if count < len(services_list):
                    service_str += ','
            tempcase.service = service_str
        
        if increase_services_list != None:
            increase_service_str = ''
            count = 0
            for increase_service in increase_services_list:
                count += 1
                increase_service_str += increase_service 
                if count < len(increase_services_list):
                    increase_service_str += ','
            tempcase.increase_service = increase_service_str
        tempcase.save()
        return redirect_params('booking_location',{'servant':servant.id})
    return render(request, 'web/booking/patient_info.html',{'start_end_date':start_end_date,'city_id':city_id, 'service_list':service_list,'increase_service_list':increase_service_list, 'body_condition_list':body_condition_list,'conditions_remark':conditions_remark, 'age':age,'disease_list':disease_list,'disease_remark':disease_remark, 'patient_name':patient_name,'gender':gender,'weight':weight,'weekday_str':weekday_str, 'increase_service_ships':increase_service_ships, 'weekday_list':weekday_list, 'servant':servant, 'care_type':care_type, 'start_time':start_time,'end_time':end_time, 'start_date_str':start_date_str,'end_date_str':end_date_str,'cityName':city,'citys':citys,'is_continuous_time':is_continuous_time, 'increase_services':increase_services, 'services':services, 'body_condition_none':body_condition_none,'disease_none':disease_none, 'diseases':diseases,'body_conditions':body_conditions})

def booking_location(request):
    servant_id= request.GET.get('servant')
    servant = User.objects.get(id=servant_id)
    user = request.user
    citys = City.objects.all()
    if TempCase.objects.filter(user=user,servant=servant,is_booking=True).exists() :
        last_tempcase = TempCase.objects.get(user=user,servant=servant,is_booking=True)
        city = last_tempcase.city
        city = City.objects.get(name=city)
        city_id = city.id
        countyName = last_tempcase.county
        counties = County.objects.filter(city=city)
        care_type = last_tempcase.care_type
        start_date = last_tempcase.start_datetime.date()
        end_date = last_tempcase.end_datetime.date()
        road_name = last_tempcase.road_name
        hospital_name = last_tempcase.hospital_name
        start_date_str = start_date.strftime("%m/%d")
        end_date_str = end_date.strftime("%m/%d")
        is_continuous_time = last_tempcase.is_continuous_time
        start_time_int = last_tempcase.start_time
        end_time_int = last_tempcase.end_time
        start_time = str(int(start_time_int)) + ':' + str(int((float(start_time_int)-int(start_time_int))*60))
        end_time = str(int(end_time_int)) + ':' + str(int((float(end_time_int)-int(end_time_int))*60))
        start_time = datetime.datetime.strptime(start_time,"%H:%M")
        end_time = datetime.datetime.strptime(end_time,"%H:%M")
        start_time = start_time.strftime("%H:%M")
        end_time = end_time.strftime("%H:%M")
        start_date = str(last_tempcase.start_datetime.date())
        end_date = str(last_tempcase.end_datetime.date())
        start_date = start_date.split('-')
        end_date = end_date.split('-')
        start_end_date = start_date[0].split('20')[1] + "/" + start_date[1] + "/" + start_date[2] + " to " + end_date[0].split('20')[1] + "/" + end_date[1] + "/" + end_date[2]
        increase_service_ids = last_tempcase.increase_service
        if is_continuous_time == False:
            weekdays = last_tempcase.weekday
            weekday_list = weekdays.split(',')
        else:
            weekday_list = []
        weekday_str = ''
        count = 0
        print(weekday_list)
        for weekday in weekday_list:
            count += 1
            weekday_str += weekday 
            if count < len(weekday_list):
                weekday_str += ','
    else:
        return redirect_params('search_carer_detail',{'servant':servant})
    if request.method == 'POST' and 'next' in request.POST:
        county_id = request.POST.get('county')
        care_type = request.POST.get('care_type')
        road_name = request.POST.get('road_name')
        hospital_name = request.POST.get('hospital_name')
        tempcase = TempCase.objects.get(user=user,servant=servant)
        tempcase.county = County.objects.get(id=county_id).name
        if road_name != None and road_name != '':
            tempcase.road_name = road_name
        if hospital_name != None and hospital_name != '':
            tempcase.hospital_name = hospital_name
        tempcase.save()
        return redirect_params('booking_contact',{'servant':servant_id})
    elif request.method == 'POST' and 'previous' in request.POST:
        return redirect_params('booking_patient_info',{'servant':servant_id})
    return render(request, 'web/booking/location.html',{'city_id':city_id, 'servant_id':servant_id,'countyName':countyName, 'counties':counties, 'road_name':road_name,'hospital_name':hospital_name, 'start_end_date':start_end_date, 'increase_service_ids':increase_service_ids, 'weekday_str':weekday_str, 'start_time':start_time,'end_time':end_time, 'is_continuous_time':is_continuous_time, 'start_date_str':start_date_str,'end_date_str':end_date_str, 'care_type':care_type, 'servant':servant, 'cityName':city,'citys':citys,})

def booking_contact(request):
    servant_id = request.GET.get('servant')
    servant = User.objects.get(id=servant_id)
    user = request.user
    if TempCase.objects.filter(user=user,servant=servant,is_booking=True).exists() :
        last_tempcase = TempCase.objects.get(user=user,servant=servant,is_booking=True)
        emergencycontact_name = last_tempcase.emergencycontact_name
        emergencycontact_relation = last_tempcase.emergencycontact_relation
        emergencycontact_phone = last_tempcase.emergencycontact_phone
        last_tempcase = TempCase.objects.get(user=user,servant=servant,is_booking=True)
        city = last_tempcase.city
        city = City.objects.get(name=city)
        city_id = city.id
        care_type = last_tempcase.care_type
        start_date = last_tempcase.start_datetime.date()
        end_date = last_tempcase.end_datetime.date()
        start_date_str = start_date.strftime("%m/%d")
        end_date_str = end_date.strftime("%m/%d")
        is_continuous_time = last_tempcase.is_continuous_time
        start_time_int = last_tempcase.start_time
        end_time_int = last_tempcase.end_time
        start_time = str(int(start_time_int)) + ':' + str(int((float(start_time_int)-int(start_time_int))*60))
        end_time = str(int(end_time_int)) + ':' + str(int((float(end_time_int)-int(end_time_int))*60))
        start_time = datetime.datetime.strptime(start_time,"%H:%M")
        end_time = datetime.datetime.strptime(end_time,"%H:%M")
        start_time = start_time.strftime("%H:%M")
        end_time = end_time.strftime("%H:%M")
        start_date = str(last_tempcase.start_datetime.date())
        end_date = str(last_tempcase.end_datetime.date())
        start_date = start_date.split('-')
        end_date = end_date.split('-')
        start_end_date = start_date[0].split('20')[1] + "/" + start_date[1] + "/" + start_date[2] + " to " + end_date[0].split('20')[1] + "/" + end_date[1] + "/" + end_date[2]
        increase_service_ids = last_tempcase.increase_service
        if is_continuous_time == False:
            weekdays = last_tempcase.weekday
            weekday_list = weekdays.split(',')
        else:
            weekday_list = []
        weekday_str = ''
        count = 0
        print(weekday_list)
        for weekday in weekday_list:
            count += 1
            weekday_str += weekday 
            if count < len(weekday_list):
                weekday_str += ','
    else:
        return redirect_params('search_carer_detail',{'servant':servant})
    if request.method == 'POST' and 'next' in request.POST:
        emergencycontact_name = request.POST.get('emergencycontact_name')
        emergencycontact_relation = request.POST.get('emergencycontact_relation')
        emergencycontact_phone = request.POST.get('emergencycontact_phone')
        tempcase = TempCase.objects.get(user=user,servant=servant,is_booking=True)
        tempcase.emergencycontact_name = emergencycontact_name
        tempcase.emergencycontact_relation = emergencycontact_relation
        tempcase.emergencycontact_phone = emergencycontact_phone
        tempcase.save()
        return redirect_params('booking_confirm',{'servant':servant_id})
    elif request.method == 'POST' and 'previous' in request.POST:
        return redirect_params('booking_location',{'servant':servant_id})
    return render(request, 'web/booking/contact.html',{'city_id':city_id, 'servant_id':servant_id,'user':user,'emergencycontact_phone':emergencycontact_phone,'emergencycontact_relation':emergencycontact_relation,'emergencycontact_name':emergencycontact_name,'start_end_date':start_end_date, 'servant_id':servant_id, 'increase_service_ids':increase_service_ids, 'weekday_str':weekday_str, 'start_time':start_time,'end_time':end_time, 'is_continuous_time':is_continuous_time, 'start_date_str':start_date_str,'end_date_str':end_date_str, 'care_type':care_type, 'servant':servant, 'cityName':city,})

def booking_confirm(request):
    servant_id = request.GET.get('servant')
    servant = User.objects.get(id=servant_id)
    servant_phone = servant.phone
    user = request.user
    if TempCase.objects.filter(user=user,servant=servant,is_booking=True).exists() :
        tempcase = TempCase.objects.get(user=user,servant=servant,is_booking=True)
        tempcase = TempCase.objects.get(user=user,servant=servant,is_booking=True)
        care_type = tempcase.care_type
        city = tempcase.city
        city = City.objects.get(name=city)
        city_id = city.id
        start_date = tempcase.start_datetime.date()
        end_date = tempcase.end_datetime.date()
        start_date_str = start_date.strftime("%m/%d")
        end_date_str = end_date.strftime("%m/%d")
        is_continuous_time = tempcase.is_continuous_time
        start_time_int = tempcase.start_time
        end_time_int = tempcase.end_time
        start_time = str(int(start_time_int)) + ':' + str(int((float(start_time_int)-int(start_time_int))*60))
        end_time = str(int(end_time_int)) + ':' + str(int((float(end_time_int)-int(end_time_int))*60))
        start_time = datetime.datetime.strptime(start_time,"%H:%M")
        end_time = datetime.datetime.strptime(end_time,"%H:%M")
        start_time = start_time.strftime("%H:%M")
        end_time = end_time.strftime("%H:%M")
        start_date = str(tempcase.start_datetime.date())
        end_date = str(tempcase.end_datetime.date())
        start_date = start_date.split('-')
        end_date = end_date.split('-')
        start_end_date = start_date[0].split('20')[1] + "/" + start_date[1] + "/" + start_date[2] + " to " + end_date[0].split('20')[1] + "/" + end_date[1] + "/" + end_date[2]
        increase_service_ids = tempcase.increase_service
        if is_continuous_time == False:
            weekdays = tempcase.weekday
            weekday_list = weekdays.split(',')
        else:
            weekday_list = []
        weekday_str = ''
        count = 0
        print(weekday_list)
        for weekday in weekday_list:
            count += 1
            weekday_str += weekday 
            if count < len(weekday_list):
                weekday_str += ','
        disease = tempcase.disease
        disease_list = []
        if disease != None and disease != '':
            disease_Idlist = disease.split(',')
            for diseaseId in disease_Idlist:
                disease_list.append(DiseaseCondition.objects.get(id=diseaseId))

        body_condition = tempcase.body_condition
        body_condition_list = []
        if body_condition != None and body_condition != '':
            body_condition_Idlist = body_condition.split(',')
            
            for body_condition_id in body_condition_Idlist:
                body_condition_list.append(BodyCondition.objects.get(id=body_condition_id))

        service = tempcase.service
        service_list = []
        if service != None and service != '':
            service_Idlist = service.split(',')
            for service_id in service_Idlist:
                service_list.append(Service.objects.get(id=service_id))
                servant_ids = list(UserServiceShip.objects.filter(service=Service.objects.get(id=service_id)).values_list('user', flat=True))
        
        increase_service = tempcase.increase_service
        increase_service_list = []
        if increase_service != None and increase_service != '':
            increase_service_Idlist = increase_service.split(',')
            for increase_service_id in increase_service_Idlist:
                increase_service_list.append(Service.objects.get(id=increase_service_id))
    else:
        return redirect_params('search_carer_detail',{'servant':servant.id})
    if request.method == 'POST' and 'pay' in request.POST:
        city_name = tempcase.city
        county_name = tempcase.county
        case = Case()
        case.user = user
        case.servant = servant
        case.city = City.objects.get(name=city_name)
        case.county = County.objects.get(city=City.objects.get(name=city_name),name=county_name)
        case.care_type = care_type
        case.name = tempcase.name
        case.gender = tempcase.gender
        case.age = tempcase.age
        case.weight = tempcase.weight
        case.disease_remark = tempcase.disease_remark
        case.conditions_remark = tempcase.conditions_remark
        case.is_continuous_time = tempcase.is_continuous_time
        case.weekday = tempcase.weekday
        case.start_time = tempcase.start_time
        case.end_time = tempcase.end_time
        case.start_datetime = tempcase.start_datetime
        case.end_datetime = tempcase.end_datetime
        case.emergencycontact_name = tempcase.emergencycontact_name
        case.emergencycontact_relation = tempcase.emergencycontact_relation
        case.emergencycontact_phone = tempcase.emergencycontact_phone
        case.created_at = datetime.datetime.now()
        case.save()

        order = Order()
        order.created_at = datetime.datetime.now()
        order.case = case
        order.user = order.case.user
        order.servant = order.case.servant
        order.state = 'unPaid'
        order.start_time = order.case.start_time
        order.end_time = order.case.end_time
        order.start_datetime = order.case.start_datetime
        order.end_datetime = order.case.end_datetime
        order.save()
        
        transfer_fee = UserServiceLocation.objects.get(user=order.servant,city=order.case.city).transfer_fee
        order.transfer_fee = transfer_fee
        if order.case.is_continuous_time == False:
            weekdays = order.case.weekday.split(',')
            for weekday in weekdays:
                orderWeekday = OrderWeekDay()
                orderWeekday.order = order
                orderWeekday.weekday = weekday
                orderWeekday.save()
            weekday_list = list(OrderWeekDay.objects.filter(order=order).values_list('weekday', flat=True))
            total_hours = 0
            number_of_transfer = 0
            for i in weekday_list:
                number_of_transfer += (days_count([int(i)], order.start_datetime.date(), order.end_datetime.date()))
                total_hours += (days_count([int(i)], order.start_datetime.date(), order.end_datetime.date())) * (order.end_time - order.start_time)
            order.work_hours = total_hours
            order.number_of_transfer = number_of_transfer
            order.amount_transfer_fee = transfer_fee * number_of_transfer
            one_day_work_hours = order.end_time - order.start_time
            if order.case.care_type == 'home':
                if one_day_work_hours < 12:
                    wage = order.case.servant.home_hour_wage
                elif one_day_work_hours >=12 and total_hours < 24:
                    wage = round(order.case.servant.home_half_day_wage/12)
            elif order.case.care_type == 'hospital':
                if one_day_work_hours < 12:
                    wage = order.case.servant.hospital_hour_wage
                elif one_day_work_hours >=12 and total_hours < 24:
                    wage = round(order.case.servant.hospital_half_day_wage/12)
        else:
            order.number_of_transfer = 1
            order.amount_transfer_fee = transfer_fee * 1
            # diff = order.end_datetime - order.start_datetime
            # days, seconds = diff.days, diff.seconds
            # hours = days * 24 + seconds // 3600
            # minutes = (seconds % 3600) // 60
            # total_hours = hours + round(minutes/60)
            total_hours = continuous_time_cal(order)
            order.work_hours = total_hours
            if order.case.care_type == 'home':
                if total_hours < 12:
                    wage = order.case.servant.home_hour_wage
                elif total_hours >=12 and total_hours < 24:
                    wage = round(order.case.servant.home_half_day_wage/12)
                else:
                    wage = round(order.case.servant.home_one_day_wage/24)
            elif order.case.care_type == 'hospital':
                if total_hours < 12:
                    wage = order.case.servant.hospital_hour_wage
                elif total_hours >=12 and total_hours < 24:
                    wage = round(order.case.servant.hospital_half_day_wage/12)
                else:
                    wage = round(order.case.servant.hospital_one_day_wage/24)
        order.wage_hour =wage
        order.base_money = order.work_hours * wage
        order.platform_percent = platform_percent_cal(user,order)
        order.save()
        Review.objects.create(order=order,case=order.case,servant=order.case.servant)
        
        for disease in disease_list:
            CaseDiseaseShip.objects.create(case=case,disease=disease)

        for body_condition in body_condition_list:
            CaseBodyConditionShip.objects.create(case=case,body_condition=body_condition)
        
        for service in service_list:
            CaseServiceShip.objects.create(case=case,service=service)

        for increase_service in increase_service_list:
            CaseServiceShip.objects.create(case=case,service=increase_service)
            orderIncreaseService = OrderIncreaseService()
            orderIncreaseService.order = order
            orderIncreaseService.service = increase_service
            orderIncreaseService.increase_percent = UserServiceShip.objects.get(user=servant,service=increase_service).increase_percent
            orderIncreaseService.increase_money = (order.base_money) * (orderIncreaseService.increase_percent)/100
            orderIncreaseService.save()

        order.total_money = ((order.base_money) + (OrderIncreaseService.objects.filter(order=order,service__is_increase_price=True).aggregate(Sum('increase_money'))['increase_money__sum']))
        order.platform_money = ((order.base_money) + (OrderIncreaseService.objects.filter(order=order,service__is_increase_price=True).aggregate(Sum('increase_money'))['increase_money__sum'])) * (order.platform_percent/100)
        order.save()

        receiveBooking(servant,order)

        chatroom = ChatRoom.objects.create(update_at=datetime.datetime.now())
        ChatroomUserShip.objects.create(user=user,chatroom=chatroom)
        message = ChatroomMessage()
        message.chatroom = chatroom
        message.user = user
        message.is_this_message_only_case = True
        message.case = case
        message.order = order
        chatroom.update_at = datetime.datetime.now()
        chatroom.save()
        message.save()

        tempcase.delete()
        order_id = order.id
        return redirect_params('http://202.182.105.11/newebpayApi/mpg_trade',{'order_id':order_id})
    elif request.method == 'POST' and 'previous' in request.POST:
        return redirect_params('booking_contact',{'servant':servant_id})
    return render(request, 'web/booking/confirm.html',{'city_id':city_id, 'servant_id':servant_id,'body_condition_list':body_condition_list,'service_list':service_list,'increase_service_list':increase_service_list, 'disease_list':disease_list,'tempcase':tempcase, 'user':user,'start_end_date':start_end_date, 'increase_service_ids':increase_service_ids, 'weekday_str':weekday_str, 'start_time':start_time,'end_time':end_time, 'is_continuous_time':is_continuous_time, 'start_date_str':start_date_str,'end_date_str':end_date_str,'care_type':care_type,'servant':servant})

def news(request):
    blogposts = BlogPost.objects.filter(state='publish')
    categories = BlogCategory.objects.all()

    if request.GET.get('category_id'):
        category_id = request.GET.get('category_id')
        the_category = BlogCategory.objects.get(id=category_id)
        post_ids = list(BlogPostCategoryShip.objects.filter(category=the_category).values_list('post', flat=True))
        blogposts = blogposts.filter(id__in=post_ids)

    return render(request, 'web/news.html',{'blogposts':blogposts,'categories':categories})

def news_detail(request):
    categories = BlogCategory.objects.all()
    blogposts = BlogPost.objects.filter(state='publish')

    blogpost_id = request.GET.get('blogpost')
    blogpost = BlogPost.objects.get(id=blogpost_id)

    if request.GET.get('category_id'):
        category_id = request.GET.get('category_id')
        the_category = BlogCategory.objects.get(id=category_id)
        post_ids = list(BlogPostCategoryShip.objects.filter(category=the_category).values_list('post', flat=True))
        blogposts = blogposts.filter(id__in=post_ids)[:3]

    return render(request, 'web/news_detail.html',{'blogpost':blogpost, 'categories':categories,'blogposts':blogposts})

def assistances(request):
    assistance_posts = AssistancePost.objects.all()

    return render(request, 'web/news.html',{'assistance_posts':assistance_posts})

def new_assistance(request):
    categories = BlogCategory.objects.all()
    blogposts = BlogPost.objects.filter(state='publish')

    blogpost_id = request.GET.get('blogpost')
    blogpost = BlogPost.objects.get(id=blogpost_id)

    if request.GET.get('category_id'):
        category_id = request.GET.get('category_id')
        the_category = BlogCategory.objects.get(id=category_id)
        post_ids = list(BlogPostCategoryShip.objects.filter(category=the_category).values_list('post', flat=True))
        blogposts = blogposts.filter(id__in=post_ids)[:3]

    return render(request, 'web/news_detail.html',{'blogpost':blogpost, 'categories':categories,'blogposts':blogposts})

def requirement_list(request):
    cases = Case.objects.all()
    citys = City.objects.all()
    city_id = ''
    care_type = ''
    start_date = ''
    end_date = ''

    if request.method == 'POST':
            
        if request.POST.get('city') != None:
            city_id = request.POST.get("city")
        care_type = request.POST.get('care_type')
        start_date = request.POST.get('datepicker_startDate')
        end_date = request.POST.get('datepicker_endDate')
        print(start_date,end_date)
        condition1 = Q(start_datetime__range=[start_date, end_date])
        condition2 = Q(end_datetime__range=[start_date, end_date])
        
        
        cases = cases.filter(city=City.objects.get(id=city_id))
        if care_type !='':
            cases = cases.filter(care_type=care_type)
    if city_id == '':
        city = ''
    else:
        city = City.objects.get(id=city_id)

    if start_date != '' and end_date != '':
        cases = cases.filter(condition1&condition2)
    if start_date != '' and end_date == '':
        cases = cases.filter(start_datetime__gte=start_date)
    if start_date == '' and end_date != '':
        cases = cases.filter(end_datetime__lte=end_date)
    cases = cases.filter(servant=None)

    return render(request, 'web/requirement_list.html',{'start_date':start_date,'end_date':end_date, 'care_type':care_type, 'cases':cases,'cityName':city,'citys':citys})

def requirement_detail(request):
    case_id = request.GET.get('case')
    user = request.user
    case = Case.objects.get(id=case_id)
    if case.is_continuous_time == False and case.weekday != None:
        week_day = case.weekday
        weekday_list = week_day.split(',')
        print(weekday_list)
        weekday_str = ''
        count = 0
        for weekday in weekday_list:
            count += 1
            if weekday == '1':
                weekday_str += '星期一' 
            elif weekday == '2':
                weekday_str += '星期二' 
            elif weekday == '3':
                weekday_str += '星期三' 
            elif weekday == '4':
                weekday_str += '星期四' 
            elif weekday == '5':
                weekday_str += '星期五' 
            elif weekday == '6':
                weekday_str += '星期六' 
            elif weekday == '0':
                weekday_str += '星期日' 
            if count < len(weekday_list):
                weekday_str += '、'
    else:
        weekday_str = '星期一 ～ 星期日'

    if request.method == 'POST':
        if user == case.user:
            return render(request, 'web/requirement_detail.html',{'case':case,'weekday_str':weekday_str,'alert_flag': True})
        else:
            case.servant = user
            order = Order(case=case,servant=user)
            order.created_at = datetime.datetime.now()
            order.user = case.user 
            order.start_datetime = case.start_datetime
            order.end_datetime = case.end_datetime
            order.start_time = case.start_time
            order.end_time = case.end_time
            order.save()

            transfer_fee = UserServiceLocation.objects.get(user=order.servant,city=order.case.city).transfer_fee
            order.transfer_fee = transfer_fee
            if order.case.is_continuous_time == False:
                weekday_list = list(OrderWeekDay.objects.filter(order=order).values_list('weekday', flat=True))
                total_hours = 0
                number_of_transfer = 0
                for i in weekday_list:
                    number_of_transfer += (days_count([int(i)], order.start_datetime.date(), order.end_datetime.date()))
                    total_hours += (days_count([int(i)], order.start_datetime.date(), order.end_datetime.date())) * (order.end_time - order.start_time)
                order.work_hours = total_hours
                order.number_of_transfer = number_of_transfer
                order.amount_transfer_fee = transfer_fee * number_of_transfer
                one_day_work_hours = order.end_time - order.start_time
                if order.case.care_type == 'home':
                    if one_day_work_hours < 12:
                        wage = order.case.servant.home_hour_wage
                        order.wage_hour =wage
                        order.hours_hour_work = total_hours
                    elif one_day_work_hours >=12 and total_hours < 24:
                        wage = round(order.case.servant.home_half_day_wage/12)
                        order.wage_hour = wage
                        order.hours_half_day_work = total_hours
                elif order.case.care_type == 'hospital':
                    if one_day_work_hours < 12:
                        wage = order.case.servant.hospital_hour_wage
                        order.wage_hour =wage
                        order.hours_hour_work = total_hours
                    elif one_day_work_hours >=12 and total_hours < 24:
                        wage = round(order.case.servant.hospital_half_day_wage/12)
                        order.wage_hour = wage
                        order.hours_half_day_work = total_hours
            else:
                order.number_of_transfer = 1
                order.amount_transfer_fee = transfer_fee * 1
                # diff = order.end_datetime - order.start_datetime
                # days, seconds = diff.days, diff.seconds
                # hours = days * 24 + seconds // 3600
                # minutes = (seconds % 3600) // 60
                # total_hours = hours + round(minutes/60)
                total_hours = continuous_time_cal(order)
                order.work_hours = total_hours
                if order.case.care_type == 'home':
                    if total_hours < 12:
                        wage = order.case.servant.home_hour_wage
                        order.wage_hour =wage
                    elif total_hours >=12 and total_hours < 24:
                        wage = round(order.case.servant.home_half_day_wage/12)
                        order.wage_hour = wage
                    else:
                        wage = round(order.case.servant.home_one_day_wage/24)
                        order.wage_one_day = wage
                        order.hours_one_day_work = total_hours
                elif order.case.care_type == 'hospital':
                    if total_hours < 12:
                        wage = order.case.servant.hospital_hour_wage
                        order.wage_hour =wage
                    elif total_hours >=12 and total_hours < 24:
                        wage = round(order.case.servant.hospital_half_day_wage/12)
                        order.wage_hour = wage
                    else:
                        wage = round(order.case.servant.hospital_one_day_wage/24)
                        order.wage_one_day = wage
            order.wage_hour =wage
            order.base_money = order.work_hours * wage
            order.platform_percent = platform_percent_cal(case.user,order)
            order.save()

            increase_services = Service.objects.filter(is_increase_price=True).order_by('id')
            for service in increase_services:
                if UserServiceShip.objects.filter(user=order.servant, service=service).count() == 0:
                    UserServiceShip.objects.create(user=order.servant,service=service)
            service_idList = list(CaseServiceShip.objects.filter(case=order.case).values_list('service', flat=True))
            for service_id in service_idList:
                if int(service_id) <= 4:
                    orderIncreaseService = OrderIncreaseService()
                    orderIncreaseService.order = order
                    orderIncreaseService.service = Service.objects.get(id=service_id)
                    orderIncreaseService.increase_percent = UserServiceShip.objects.get(user=order.servant,service=Service.objects.get(id=service_id)).increase_percent
                    orderIncreaseService.increase_money = (order.base_money) * (orderIncreaseService.increase_percent)/100
                    orderIncreaseService.save()

            order.total_money = ((order.base_money) + (OrderIncreaseService.objects.filter(order=order,service__is_increase_price=True).aggregate(Sum('increase_money'))['increase_money__sum'])) * ((100 - order.platform_percent)/100)
            order.platform_money = order.total_money * (order.platform_percent/100)
            order.save()
            neederOrderEstablished(case.user,order)
            servantOrderEstablished(case.servant,order)

            chatroom_ids1 = list(ChatroomUserShip.objects.filter(user=order.user).values_list('chatroom', flat=True))
            chatroom_ids2 = list(ChatroomUserShip.objects.filter(user=order.servant).values_list('chatroom', flat=True))
            chatroom_set = set(chatroom_ids1).intersection(set(chatroom_ids2))
            if list(chatroom_set) != []:
                chatroom_id = list(chatroom_set)[0]
                print(chatroom_id)
                chatroom = ChatRoom.objects.get(id=chatroom_id)
                message = ChatroomMessage(user=user,case=order.case,order=order,chatroom=chatroom,is_this_message_only_case=True)
                message.save()
            elif list(chatroom_set) == []:
                chatroom = ChatRoom()
                chatroom.save()
                ChatroomUserShip.objects.create(user=order.user,chatroom=chatroom)
                ChatroomUserShip.objects.create(user=order.servant,chatroom=chatroom)
                message = ChatroomMessage(user=user,case=order.case,order=order,chatroom=chatroom,is_this_message_only_case=True)
                message.save()
                
            chatroom.update_at = datetime.datetime.now()
            chatroom.save()

            return redirect('take_case_message')

    return render(request, 'web/requirement_detail.html',{'case':case,'weekday_str':weekday_str})

def take_case_message(request):
    return render(request, 'web/take_case_message.html')

def become_carer(request):
    return render(request, 'web/become_carer.html')

def my_service_setting_time(request):
    user = request.user
    
    languages = Language.objects.all()
    user_languages = UserLanguage.objects.filter(user=user)
    user_language_ids = list(user_languages.values_list('language',flat=True))

    user_weekday_times = UserWeekDayTime.objects.filter(user=user)
    user_weekdays = list(UserWeekDayTime.objects.filter(user=user).values_list('weekday',flat=True))

    if request.method == 'POST':
        gender = request.POST.get('gender')
        if gender != None:
            user.gender = gender
        
        is_continuous_time = request.POST.get('is_continuous_time') 
        if is_continuous_time == 'True':
            user.is_continuous_time = True
        else:
            user.is_continuous_time = False

        user.save()

        # handle weekdays
        weekday_id_list = request.POST.getlist('weekdays[]')
        weekday_str_list = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
        weekday_list = []
        for num in weekday_id_list:
            weekday_list.append(int(num))
        
        weekday_list.sort()
        for i in weekday_list:
            start_time = request.POST.get(weekday_str_list[int(i)][:3]+'_start_time')
            end_time = request.POST.get(weekday_str_list[int(i)][:3]+'_end_time')
            
            # 把底下的 start_time_hour/start_time_min, end_time_hour/end_time_min 做計算, 存回 start_time, end_time
            start_time_hour = int(start_time.split(':')[0])
            start_time_min = int(start_time.split(':')[1])

            end_time_hour = int(end_time.split(':')[0])
            end_time_min = int(end_time.split(':')[1])

            if UserWeekDayTime.objects.filter(user=user,weekday=str(i)).exists():
                userweekdaytime = UserWeekDayTime.objects.get(user=user,weekday=str(i))
            else:
                userweekdaytime = UserWeekDayTime()
            userweekdaytime.user = user
            userweekdaytime.weekday = str(i)
            userweekdaytime.start_time_hour = start_time_hour
            userweekdaytime.start_time_min = start_time_min
            userweekdaytime.end_time_hour = end_time_hour
            userweekdaytime.end_time_min = end_time_min

            userweekdaytime.start_time = int(start_time_hour) + float(int(start_time_min)/60)
            userweekdaytime.end_time = int(end_time_hour) + float(int(end_time_min)/60)

            userweekdaytime.save()
        
        for user_weekday_time in user_weekday_times:
            if user_weekday_time.weekday not in weekday_id_list:
                user_weekday_time.delete()


        # handle languages
        selected_languages = []
        language_ids = request.POST.getlist('languages[]')

        for language_id in language_ids:
            language = Language.objects.get(id=language_id)
            if UserLanguage.objects.filter(user=user,language=language).exists():
                userlanguage = UserLanguage.objects.get(user=user,language=language)
            else:
                userlanguage = UserLanguage()
            userlanguage.user = user
            userlanguage.language = language
            if language_id == '5':
                userlanguage.remark = request.POST.get('lan_aboriginal')
            if language_id == '8':
                userlanguage.remark = request.POST.get('lan_other')
            userlanguage.save()
            selected_languages.append(language)
        
        for user_language in user_languages:
            if user_language.language not in selected_languages:
                user_language.delete()

        return redirect('my_service_setting_time')

    return render(request, 'web/my/my_service_setting_time.html',{
        'user':user, 
        'languages':languages, 'user_languages':user_languages, 'user_language_ids':user_language_ids,
        'user_weekday_times':user_weekday_times, 'user_weekdays':user_weekdays,
        })

def my_service_setting_services(request):
    user = request.user
    
    services = Service.objects.filter(is_increase_price=False).order_by('id')
    increase_services = Service.objects.filter(is_increase_price=True).order_by('id')
    user_services_ids = list(UserServiceShip.objects.filter(user=user).values_list("service", flat=True))
    user_service_ships = UserServiceShip.objects.filter(user=user)

    city_id = '4'
    citys = City.objects.all()
    city = City.objects.get(id=city_id)

    user_service_locations = UserServiceLocation.objects.filter(user=user)
    location_range = range(user_service_locations.count(),user_service_locations.count()+20)

    if request.method == 'POST' :
        # care type and wage
        care_type_home = request.POST.get('care_type_home')
        care_type_hospital = request.POST.get('care_type_hospital')
        if care_type_home == 'home':
            user.is_home = True
        if care_type_hospital == 'hospital':
            user.is_hospital = True
        home_hour = request.POST.get('home_hour')
        home_half_day = request.POST.get('home_half_day')
        home_full_day = request.POST.get('home_full_day')
        hospital_hour = request.POST.get('hospital_hour')
        hospital_half_day = request.POST.get('hospital_half_day')
        hospital_full_day = request.POST.get('hospital_full_day')
        if home_hour != None and home_hour != '':
            user.home_hour_wage = int(home_hour)
        if home_half_day != None and home_half_day != '':
            user.home_half_day_wage = int(home_half_day)
        if home_full_day != None and home_full_day != '':
            user.home_one_day_wage = int(home_full_day)
        if hospital_hour != None and hospital_hour != '':
            user.hospital_hour_wage = int(hospital_hour)
        if hospital_half_day != None and hospital_half_day != '':
            user.hospital_half_day_wage = int(hospital_half_day)
        if hospital_full_day != None and hospital_full_day != '':
            user.hospital_one_day_wage = int(hospital_full_day)
        user.save()

        # locations
        submit_user_locations = []

        locations_nums = request.POST.get('hidden_locations[]')
        if locations_nums != None:
            location_list = locations_nums.split(',')
        else:
            location_list = []

        for num in location_list:
            set_city = request.POST.get('city_'+str(num))
            set_transfer_fee = request.POST.get('transfer_fee_'+str(num))
            set_city = City.objects.get(id=set_city)

            if UserServiceLocation.objects.filter(user=user,city=set_city).exists():
                userlocation = UserServiceLocation.objects.get(user=user,city=set_city)
            else:
                userlocation = UserServiceLocation()
            userlocation.user = user
            userlocation.city = set_city
            if set_transfer_fee != '':
                userlocation.transfer_fee = int(set_transfer_fee)
            userlocation.save()
            submit_user_locations.append(userlocation)
        # print(submit_user_locations)

        for user_location in user_service_locations:
            if user_location not in submit_user_locations:
                user_location.delete()

        # services
        services_ids = list(map(int, request.POST.getlist('services[]'))) 

        for service in services:
            if service.id in services_ids:
                if not UserServiceShip.objects.filter(user=user,service=service).exists():
                    UserServiceShip.objects.create(user=user,service=service)
            else:
                if UserServiceShip.objects.filter(user=user,service=service).exists():
                    UserServiceShip.objects.filter(user=user,service=service).delete()

        # increase_ids = list(map(int, request.POST.getlist('increases[]')))
        for increase_service in increase_services:
            # if increase_service.id in increase_ids:
                set_increase_percent = request.POST.get(increase_service.name + 'percent')

                if UserServiceShip.objects.filter(user=user,service=increase_service).exists():
                    userserviceship = UserServiceShip.objects.get(user=user,service=increase_service)
                else:
                    userserviceship = UserServiceShip()
                    userserviceship.user = user
                    userserviceship.service = increase_service
                userserviceship.increase_percent = float(set_increase_percent)
                userserviceship.save()
            # else:
            #     if UserServiceShip.objects.filter(user=user,service=increase_service).exists():
            #         UserServiceShip.objects.filter(user=user,service=increase_service).delete()

        return redirect('my_service_setting_services')

    return render(request, 'web/my/my_service_setting_services.html',
                    {
                        'user':user, 
                        'services':services,'increase_services':increase_services,'user_services_ids':user_services_ids,'user_service_ships':user_service_ships,
                        'citys':citys,'cityName':city,'user_service_locations':user_service_locations, 'location_range':location_range,
                    })

def my_service_setting_about(request):
    user = request.user
    licences = License.objects.all().order_by('id')[3:]

    for license in licences:
        if UserLicenseShipImage.objects.filter(user=user, license=license).count() == 0:
            UserLicenseShipImage.objects.create(user=user,license=license)
    
    licenseImageShips = UserLicenseShipImage.objects.filter(user=user).order_by('license')[3:]
    form = UserLicenseImageForm()
    userform = UserBackGroundImageForm()
    # increase_service_ships = UserServiceShip.objects.filter(user=servant).order_by('service')[:4]
    if request.method == 'POST':
        license_id = request.POST.get('licenseId')
        if license_id != None:
            print(type(license_id))
            if UserLicenseShipImage.objects.filter(user=user,license=License.objects.get(id=license_id)).exists() :
                shipinstance = UserLicenseShipImage.objects.get(user=user,license=License.objects.get(id=license_id))
            else:
                UserLicenseShipImage.objects.create(user=user,license=License.objects.get(id=license_id))
                shipinstance = UserLicenseShipImage.objects.get(user=user,license=License.objects.get(id=license_id))
            
            form = UserLicenseImageForm(request.POST or None, request.FILES or None,instance=shipinstance)
            if form.is_valid():
                print('valid')
                userLicenseShipImage = form.save(commit=False)
                userLicenseShipImage.user = user
                userLicenseShipImage.license = License.objects.get(id=license_id)
                userLicenseShipImage.save()
                
            userLicenseShipImage = form.instance
            print(userLicenseShipImage)
            userLicenseShipImage.user = user
            userLicenseShipImage.license = License.objects.get(id=license_id)
            userLicenseShipImage.save()

        if request.POST.get('about_me')!= None:
            about_me = request.POST.get('about_me')
            user.about_me = about_me
            user.save()

        userform = UserBackGroundImageForm(request.POST or None, request.FILES or None, instance=user)
        if userform.is_valid():
            print('valid')
            user = userform.save(commit=False)
            user.phone = user.phone
            user.save()
        user = userform.instance
        user.phone = user.phone
        user.save()

    return render(request, 'web/my/my_service_setting_about.html',{'user':user,'form':form,'userform':userform, 'licenseImageShips':licenseImageShips})

def my_bank_account(request):
    
    user = request.user
    if request.method == 'POST':
        bankNameCode = request.POST.get('bankNameCode')
        bankBranchCode = request.POST.get('bankBranchCode')
        bankAccountNum = request.POST.get('bankAccountNum')
        user.ATMInfoBankCode = bankNameCode
        user.ATMInfoBranchBankCode = bankBranchCode
        user.ATMInfoAccount = bankAccountNum
        user.save()
    return render(request, 'web/my/bank_account.html')
 
def my_bookings(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    return render(request, 'web/my/bookings.html',{'orders':orders,'user':user})

def my_booking_detail(request):
    order_id = request.GET.get('order')
    order = Order.objects.get(id=order_id)
    review = Review.objects.get(order=order)
    work_hours = round(order.work_hours)
    if request.method == 'POST':
        rating = request.POST.get('myInput')
        comment = request.POST.get('comment')
        review.servant_comment = comment
        review.servant_rating = float(rating)
        review.servant_rating_created_at = datetime.datetime.now()
        review.save()
        return render(request, 'web/my/booking_detail.html',{'order':order,'review':review,'work_hours':work_hours})
    return render(request, 'web/my/booking_detail.html',{'order':order,'review':review,'work_hours':work_hours})

def my_cases(request):
    servant = request.user
    cases = Case.objects.filter(servant=servant)
    review = Review.objects.get(servant=servant)
    return render(request, 'web/my/cases.html',{'servant':servant,'cases':cases,'review':review})

def my_case_detail(request):
    case_id = request.GET.get('case')
    case = Case.objects.get(id=case_id)
    order = Order.objects.get(case=case)
    work_hours = round(order.work_hours)
    review = Review.objects.get(case=case)
    total_money = order.total_money - order.platform_money
    ##test
    now = timezone.now()
    # tzUtc = pytz.timezone('UTC')
    remind_time_start = (case.start_datetime - timedelta(hours=3))
    remind_time_end = (case.start_datetime - timedelta(hours=2,minutes=45))
    print(now,remind_time_start,remind_time_end)
    if now > remind_time_start and now < remind_time_end:
        print('success')
    ###
    if request.method == 'POST':
        rating = request.POST.get('myInput')
        comment = request.POST.get('comment')
        print(type(rating))
        review.case_offender_comment = comment
        review.case_offender_rating = float(rating)
        review.case_offender_rating_created_at = datetime.datetime.now()
        review.save()
        return render(request, 'web/my/case_detail.html',{'case':case,'order':order,'work_hours':work_hours,'review':review,'total_money':total_money})
    return render(request, 'web/my/case_detail.html',{'case':case,'order':order,'work_hours':work_hours,'review':review,'total_money':total_money})

def my_care_certificate(request):
    servant = request.user
    case_id = request.GET.get('case')
    case = Case.objects.get(id=case_id)
    order = Order.objects.get(case=case)
    total_fee = ((order.base_money) + (OrderIncreaseService.objects.filter(order=order,service__is_increase_price=True).aggregate(Sum('increase_money'))['increase_money__sum']))
    print(total_fee)
    return render(request, 'web/my/care_certificate.html',{'case':case,'order':order,'total_fee':total_fee})

def my_simplfy_certificate(request):
    servant = request.user
    case_id = request.GET.get('case')
    case = Case.objects.get(id=case_id)
    order = Order.objects.get(case=case)
    total_fee = order.total_money
    return render(request, 'web/my/simplfy_certificate.html',{'case':case,'order':order,'total_fee':total_fee})
def my_files(request):
    user = request.user
    licences = License.objects.all().order_by('id')[:3]
    
    # UserLicenseImageShips 也許在 User Create 時就產生好
    for license in licences:
        if UserLicenseShipImage.objects.filter(user=user, license=license).count() == 0:
            UserLicenseShipImage.objects.create(user=user,license=license)
    
    licenseImageShips = UserLicenseShipImage.objects.filter(user=user).order_by('license')[:3]

    form = UserLicenseImageForm()
    if request.method == 'POST' :
        license_id = request.POST.get('licenceId')

        if UserLicenseShipImage.objects.filter(user=user,license=License.objects.get(id=license_id)).exists() :
            shipinstance = UserLicenseShipImage.objects.get(user=user,license=License.objects.get(id=license_id))
        else:
            UserLicenseShipImage.objects.create(user=user,license=License.objects.get(id=license_id))
            shipinstance = UserLicenseShipImage.objects.get(user=user,license=License.objects.get(id=license_id))
        form = UserLicenseImageForm(request.POST or None, request.FILES or None,instance=shipinstance)

        if form.is_valid():
            print('valid')
            userLicenseShipImage = form.save(commit=False)
            userLicenseShipImage.user = user
            userLicenseShipImage.license = License.objects.get(id=license_id)
            userLicenseShipImage.save()
            
        userLicenseShipImage = form.instance
        print(userLicenseShipImage)
        userLicenseShipImage.user = user
        userLicenseShipImage.license = License.objects.get(id=license_id)
        userLicenseShipImage.save()

    return render(request, 'web/my/files.html',{'user':user,'form':form,'licences':licences, 'licenseImageShips':licenseImageShips})

def my_profile(request):
    user = request.user
    return render(request, 'web/my/profile.html',{'user':user})

def my_edit_profile(request):
    user = request.user 
    userform = UserImageForm()
    if request.method == 'POST' :
        userform = UserImageForm(request.POST or None, request.FILES or None, instance=user)
        if userform.is_valid():
            print('valid')
            user = userform.save(commit=False)
            user.phone = user.phone
            user.save()
        user = userform.instance
        user.phone = user.phone
        user.save()

    if request.method == 'POST' and 'line_bind' in request.POST:
        auth_url = 'https://access.line.me/oauth2/v2.1/authorize?'
        # call_back = 'http://202.182.105.11/' + redirect_to
        call_back = 'http://127.0.0.1:8000/web/login_line?next=/web/index'

        print(call_back)
        data = {
            'response_type': 'code',
            'client_id': '1657316694',
            'redirect_uri': call_back,
            'state': 'abcde',
        }
        query_str = urllib.parse.urlencode(data) + '&scope=profile%20openid%20email'
        login_url = auth_url + query_str
        print(login_url)
        return redirect(login_url) 
    if request.method == 'POST' and 'post' in request.POST:
        print('post2')
        user_name = request.POST.get('user_name')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        user.name = user_name
        user.gender = gender
        user.phone = phone
        user.email = email
        user.save()
    
    return render(request, 'web/my/edit_profile.html',{'user':user,'userform':userform})

def my_reviews(request):
    user = request.user
    not_rated_orders = Order.objects.filter(user=user,order_reviews__servant_rating__lt=1)
    my_rating_reviews = Review.objects.filter(case__user=user,servant_rating__gte=1)
    my_reviews = Review.objects.filter(case__user=user,case_offender_rating__gte=1)
    
    return render(request, 'web/my/reviews.html',{'user':user,'not_rated_orders':not_rated_orders,'my_rating_reviews':my_rating_reviews,'my_reviews':my_reviews})

def my_write_review(request):
    
    order_id = request.GET.get('order')
    order = Order.objects.get(id=order_id)
    review = Review.objects.get(order=order)
    print(review)
    if request.method == 'POST' and 'post'in request.POST:
        
        rating = request.POST.get('myInput')
        comment = request.POST.get('comment')
        review.servant_rating = float(rating)
        review.servant_comment = comment
        review.servant_rating_created_at = datetime.datetime.now()
        review.save()
        return redirect_params('my_booking_detail',{'order':order_id})
    elif request.method == 'POST' and 'back'in request.POST:
        return redirect('my_reviews')
    return render(request, 'web/my/write_review.html',{'order':order})

def my_notification_setting(request):
    user = request.user
    if request.method == 'POST':
        check_news_content = request.POST.get('check_news_content')
        if check_news_content == 'True':
            user.is_fcm_notify = True
            user.save()
        else:
            user.is_fcm_notify = False
            user.save()
        return redirect('index')
    return render(request, 'web/my/notification_setting.html',{'user':user})

def request_form_service_type(request):
    user = request.user
    citys = City.objects.all()
    counties = County.objects.all()

    if TempCase.objects.filter(user=user,is_booking=False).exists() :
        last_tempcase = TempCase.objects.get(user=user,is_booking=False)
        care_type = last_tempcase.care_type
        start_date = str(last_tempcase.start_datetime.date())
        end_date = str(last_tempcase.end_datetime.date())
        start_date = start_date.split('-')
        end_date = end_date.split('-')
        start_end_date = start_date[0].split('20')[1] + "/" + start_date[1] + "/" + start_date[2] + " to " + end_date[0].split('20')[1] + "/" + end_date[1] + "/" + end_date[2]
        city = City.objects.get(name=last_tempcase.city)
        county_name = last_tempcase.county
        print(county_name)
        road_name = last_tempcase.road_name
        hospital_name = last_tempcase.hospital_name
        is_continuous_time = last_tempcase.is_continuous_time
        counties = counties.filter(city=city)
        print(is_continuous_time)
        if is_continuous_time == False:
            weekdays = last_tempcase.weekday
            weekday_list = weekdays.split(',')
        else:
            weekday_list = []
        start_time_int = last_tempcase.start_time
        end_time_int = last_tempcase.end_time
        start_time = str(int(start_time_int)) + ':' + str(int((float(start_time_int)-int(start_time_int))*60))
        end_time = str(int(end_time_int)) + ':' + str(int((float(end_time_int)-int(end_time_int))*60))
        start_time = datetime.datetime.strptime(start_time,"%H:%M")
        end_time = datetime.datetime.strptime(end_time,"%H:%M")
        start_time = start_time.strftime("%H:%M")
        end_time = end_time.strftime("%H:%M")
        print(start_time,end_time)

    else:
        city_id = '8'
        city = City.objects.get(id=city_id)
        counties = counties.filter(city=City.objects.get(id=city_id))
        county_name = '全區'
        start_time = ''
        end_time = ''
        weekday_list = []
        is_continuous_time = True
        start_end_date = ''
        care_type = 'home'
        road_name = ''
        hospital_name = ''

    if request.method == 'POST':
        care_type = request.POST.get('care_type')
        city = request.POST.get('city')
        county = request.POST.get('county')
        start_end_date = request.POST.get('start_end_date')
        is_continuous_time = request.POST.get('time_type')
        start_time = request.POST.get('timepicker_startTime')
        end_time = request.POST.get('timepicker_endTime')
        road_name = request.POST.get('road_name')
        hospital_name = request.POST.get('hospital_name')
        start_date ='20'+ start_end_date.split(' to ')[0]
        end_date = '20' + start_end_date.split(' to ')[1]
        start_date = datetime.datetime.strptime(start_date, "%Y/%m/%d")
        end_date = datetime.datetime.strptime(end_date, "%Y/%m/%d")
        start_time = start_time.split(':')
        end_time = end_time.split(':')
        start_time_int = int(start_time[0]) + float(int(start_time[1])/60)
        end_time_int = int(end_time[0]) + float(int(end_time[1])/60)
        if TempCase.objects.filter(user=user,is_booking=False).exists() != False:
            tempcase = TempCase.objects.get(user=user,is_booking=False)
        else:
            tempcase = TempCase()
        tempcase.user = user
        tempcase.care_type = care_type
        tempcase.city = City.objects.get(id=city).name
        tempcase.county = county
        tempcase.start_datetime = start_date
        tempcase.end_datetime = end_date
        tempcase.start_time = start_time_int
        tempcase.end_time = end_time_int
        if road_name != None and road_name != '':
            tempcase.road_name = road_name
        if hospital_name != None and hospital_name != '':
            tempcase.hospital_name = hospital_name
        if is_continuous_time == 'True':
            tempcase.is_continuous_time = True
        else:
            tempcase.is_continuous_time = False
            weekdays = request.POST.getlist('weekdays[]')
            weekday_str = ''
            count = 0
            for weekday in weekdays:
                count += 1
                weekday_str += weekday 
                if count < len(weekdays):
                    weekday_str += ','
            tempcase.weekday = weekday_str
        tempcase.save()
        return redirect('request_form_patient_info')
    
    return render(request, 'web/request_form/service_type.html',{'countyName':county_name,'counties':counties, 'road_name':road_name,'hospital_name':hospital_name, 'start_time':start_time,'end_time':end_time, 'weekday_list':weekday_list,'is_continuous_time':is_continuous_time, 'start_end_date':start_end_date,'care_type':care_type,'cityName':city,'citys':citys})

def request_form_patient_info(request):
    user = request.user
    diseases = DiseaseCondition.objects.all().order_by('id')[1:]
    body_conditions = BodyCondition.objects.all().order_by('id')[1:]
    services = Service.objects.all().order_by('id')[4:]
    increase_services = Service.objects.filter(is_increase_price=True).order_by('id')
    for increase_service in increase_services:
        if UserServiceShip.objects.filter(user=user,service=increase_service).count() == 0:
            obj = UserServiceShip.objects.create(user=user,service=increase_service)
            print(obj)
    increase_service_ships = UserServiceShip.objects.filter(user=user).order_by('service')[:4]
    if TempCase.objects.filter(user=user,is_booking=False).exists() :

        last_tempcase = TempCase.objects.get(user=user,is_booking=False)
        
        patient_name = last_tempcase.name
        gender = last_tempcase.gender
        weight = last_tempcase.weight
        age = last_tempcase.age
        disease = last_tempcase.disease
        disease_remark = last_tempcase.disease_remark
        body_condition = last_tempcase.body_condition
        conditions_remark = last_tempcase.conditions_remark
        service = last_tempcase.service
        increase_service = last_tempcase.increase_service
        disease_list = []
        if disease != None and disease != '':
            disease_Idlist = disease.split(',')
            for diseaseId in disease_Idlist:
                disease_list.append(DiseaseCondition.objects.get(id=diseaseId))
        else:
            disease_Idlist = []
        if '1' in disease_Idlist:
            disease_none = True
        else:
            disease_none = False
        
        body_condition_list = []
        if body_condition != None and body_condition != '' :
            body_condition_Idlist = body_condition.split(',')
            for body_condition_id in body_condition_Idlist:
                body_condition_list.append(BodyCondition.objects.get(id=body_condition_id))
        else:
            body_condition_Idlist = []
        if '1' in body_condition_Idlist:
            body_condition_none = True
        else:
            body_condition_none = False

        if service != None and service != '' :
            service_Idlist = service.split(',')
        else:
            service_Idlist = []
        service_list = []
        for service_id in service_Idlist:
            service_list.append(Service.objects.get(id=service_id))
        
        if increase_service != None and increase_service != '' :
            increase_service_Idlist = increase_service.split(',')
        else:
            increase_service_Idlist = []
        
        increase_service_list = []
        for increase_service_id in increase_service_Idlist:
            increase_service_list.append(UserServiceShip.objects.get(user=user,service=Service.objects.get(id=increase_service_id)))
        print(increase_service_list)
        
    if request.method == 'POST' and 'next' in request.POST:
        print('post')
        patient_name = request.POST.get('patient_name')
        gender = request.POST.get('gender')
        weight = request.POST.get('weight')
        age = request.POST.get('age')
        disease_none = request.POST.get('disease_none')
        diseases_list = request.POST.getlist('diseases[]')
        disease_text = request.POST.get('disease_text')
        body_condition_none = request.POST.get('body_condition_none')
        body_conditions_list = request.POST.getlist('body_conditions[]')
        body_condition_note = request.POST.get('body_condition_note')
        services_list = request.POST.getlist('services[]')
        increase_services_list = request.POST.getlist('increase_services[]')
        tempcase = TempCase.objects.get(user=user,is_booking=False)
        tempcase.name = patient_name
        tempcase.gender = gender
        tempcase.weight = weight
        tempcase.age = age
        if disease_none != None:
            tempcase.disease = '1'
        else:
            disease_str = ''
            count = 0
            for disease in diseases_list:
                count += 1
                disease_str += disease 
                if count < len(diseases_list):
                    disease_str += ','
            tempcase.disease = disease_str
        tempcase.disease_remark = disease_text

        if body_condition_none != None:
            tempcase.body_condition = '1'
        else:
            body_condition_str = ''
            count = 0
            for body_condition in body_conditions_list:
                count += 1
                body_condition_str += body_condition 
                if count < len(body_conditions_list):
                    body_condition_str += ','
            tempcase.body_condition = body_condition_str
        tempcase.conditions_remark = body_condition_note

        if services_list != None:
            service_str = ''
            count = 0
            for service in services_list:
                count += 1
                service_str += service 
                if count < len(services_list):
                    service_str += ','
            tempcase.service = service_str
        
        if increase_services_list != None:
            increase_service_str = ''
            count = 0
            for increase_service in increase_services_list:
                count += 1
                increase_service_str += increase_service 
                if count < len(increase_services_list):
                    increase_service_str += ','
            tempcase.increase_service = increase_service_str
        tempcase.save()
        print('save')
        return redirect('request_form_contact')
        
    elif request.method == 'POST' and 'previous' in request.POST:
        return redirect('request_form_service_type')

    return render(request, 'web/request_form/patient_info.html',{'increase_service_ships':increase_service_ships,'service_list':service_list,'increase_service_list':increase_service_list, 'body_condition_list':body_condition_list,'conditions_remark':conditions_remark, 'age':age,'disease_list':disease_list,'disease_remark':disease_remark, 'patient_name':patient_name,'gender':gender,'weight':weight, 'increase_services':increase_services, 'services':services, 'body_condition_none':body_condition_none,'body_conditions':body_conditions, 'disease_none':disease_none,'diseases':diseases})

def request_form_contact(request):
    user = request.user
    if TempCase.objects.filter(user=user,is_booking=False).exists() :
        last_tempcase = TempCase.objects.get(user=user,is_booking=False)
        emergencycontact_name = last_tempcase.emergencycontact_name
        emergencycontact_relation = last_tempcase.emergencycontact_relation
        emergencycontact_phone = last_tempcase.emergencycontact_phone


    if request.method == 'POST' and 'next' in request.POST:
        print('next')
        emergencycontact_name = request.POST.get('emergencycontact_name')
        emergencycontact_relation = request.POST.get('emergencycontact_relation')
        emergencycontact_phone = request.POST.get('emergencycontact_phone')
        tempcase = TempCase.objects.get(user=user,is_booking=False)
        tempcase.emergencycontact_name = emergencycontact_name
        tempcase.emergencycontact_relation = emergencycontact_relation
        tempcase.emergencycontact_phone = emergencycontact_phone
        tempcase.save()
        return redirect('request_form_confirm')
    elif request.method == 'POST' and 'previous' in request.POST:
        return redirect('request_form_patient_info')
    return render(request, 'web/request_form/contact.html',{ 'user':user,'emergencycontact_phone':emergencycontact_phone,'emergencycontact_relation':emergencycontact_relation,'emergencycontact_name':emergencycontact_name})

def request_form_confirm(request):
    user = request.user
    user_id = user.id
    servants = User.objects.filter(is_servant_passed=True)
    servants = servants.exclude(is_home=False,is_hospital=False)
    servants = servants.exclude(id=user_id)
    tempcase = TempCase.objects.get(user=user,is_booking=False)
    care_type = tempcase.care_type
    start_date = tempcase.start_datetime
    start_date_str = str(start_date.month ) + '/' +str(start_date.day)
    end_date = tempcase.end_datetime
    end_date_str = str(end_date.month) + '/' + str(end_date.day)
    if tempcase.is_continuous_time == True:
        time_type = '連續時間'
    else:
        time_type = '每週固定'
    start_time_int = tempcase.start_time
    end_time_int = tempcase.end_time
    start_time = str(int(start_time_int)) + ':' + str(int((float(start_time_int)-int(start_time_int))*60))
    end_time = str(int(end_time_int)) + ':' + str(int((float(end_time_int)-int(end_time_int))*60))
    start_time = datetime.datetime.strptime(start_time,"%H:%M")
    end_time = datetime.datetime.strptime(end_time,"%H:%M")
    start_time_str = start_time.strftime("%H:%M")
    end_time_str = end_time.strftime("%H:%M")

    disease = tempcase.disease
    disease_list = []
    if disease != None and disease != '':
        disease_Idlist = disease.split(',')
        for diseaseId in disease_Idlist:
            disease_list.append(DiseaseCondition.objects.get(id=diseaseId))

    body_condition = tempcase.body_condition
    body_condition_list = []
    if body_condition != None and body_condition != '':
        body_condition_Idlist = body_condition.split(',')
        
        for body_condition_id in body_condition_Idlist:
            body_condition_list.append(BodyCondition.objects.get(id=body_condition_id))

    service = tempcase.service
    service_list = []
    service_ids = []
    if service != None and service != '':
        service_ids = service.split(',')
        for service_id in service_ids:
            service_list.append(Service.objects.get(id=service_id))
            # servant_ids = list(UserServiceShip.objects.filter(service=Service.objects.get(id=service_id)).values_list('user', flat=True))
    
    increase_service = tempcase.increase_service
    increase_service_list = []
    if increase_service != None and increase_service != '':
        increase_service_ids = increase_service.split(',')
        for increase_service_id in increase_service_ids:
            increase_service_list.append(Service.objects.get(id=increase_service_id))
    
    is_continuous_time = tempcase.is_continuous_time
    weekdays = tempcase.weekday
    city_name = tempcase.city
    county_name = tempcase.county
    user_ids = list(UserServiceLocation.objects.filter(city=City.objects.get(name=city_name)).values_list('user', flat=True))
    servants = servants.filter(id__in=user_ids)

    if care_type == 'home':
        servants = servants.filter(is_home=True)
    elif care_type == 'hospital':
        servants = servants.filter(is_hospital=True)

    if is_continuous_time == 'True':
            servants = servants.filter(is_continuous_time=True)

        #所選擇的周間跟時段 要符合 servant 的服務時段
    if weekdays != None:
        if (start_date != '') and (end_date != '') and (start_time != '') and (end_time != ''):
            start_time = start_time_str.split(':')
            end_time = end_time_str.split(':')
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
            weekday_condition_1 = Q(order_weekdays__weekday__in=weekdays_num_list)
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
        else:
            weekdays_num_list = weekdays
            service_time_condition_1 = Q(is_continuous_time=True)
            for weekdays_num in weekdays_num_list:
                service_time_condition_2 = Q(user_weekday__weekday__in=weekdays_num)
                servants = servants.filter(service_time_condition_1 | service_time_condition_2).distinct()
        
    if request.method == 'POST' and 'submit' in request.POST:
        choose_servant_ids = request.POST.getlist('choose_carer[]')
        case = Case()
        case.user = user
        case.city = City.objects.get(name=city_name)
        if county_name != '全區':
            case.county = County.objects.get(city=City.objects.get(name=city_name),name=county_name)
        case.care_type = care_type
        case.name = tempcase.name
        case.gender = tempcase.gender
        case.age = tempcase.age
        case.weight = tempcase.weight
        case.disease_remark = tempcase.disease_remark
        case.conditions_remark = tempcase.conditions_remark
        case.is_continuous_time = tempcase.is_continuous_time
        case.weekday = tempcase.weekday
        case.start_time = tempcase.start_time
        case.end_time = tempcase.end_time
        case.start_datetime = tempcase.start_datetime
        case.end_datetime = tempcase.end_datetime
        case.emergencycontact_name = tempcase.emergencycontact_name
        case.emergencycontact_relation = tempcase.emergencycontact_relation
        case.emergencycontact_phone = tempcase.emergencycontact_phone
        case.created_at = datetime.datetime.now()
        case.save()
        

        for disease in disease_list:
            CaseDiseaseShip.objects.create(case=case,disease=disease)

        for body_condition in body_condition_list:
            CaseBodyConditionShip.objects.create(case=case,body_condition=body_condition)
        
        for service in service_list:
            CaseServiceShip.objects.create(case=case,service=service)
        for increase_service in increase_service_list:
            CaseServiceShip.objects.create(case=case,service=increase_service)
        
        for servant_id in choose_servant_ids:
            servant = User.objects.get(id=servant_id)
            order = Order()
            order.created_at = datetime.datetime.now()
            order.case = case
            order.user = case.user
            order.servant = servant
            order.state = 'unPaid'
            order.start_datetime = case.start_datetime
            order.end_datetime = case.end_datetime
            order.start_time = order.case.start_time
            order.end_time = order.case.end_time
            order.save()
            transfer_fee = UserServiceLocation.objects.get(user=order.servant,city=order.case.city).transfer_fee
            order.transfer_fee = transfer_fee
            
            if order.case.is_continuous_time == False:
                weekdays = order.case.weekday.split(',')
                for weekday in weekdays:
                    orderWeekday = OrderWeekDay()
                    orderWeekday.order = order
                    orderWeekday.weekday = weekday
                    orderWeekday.save()
                weekday_list = list(OrderWeekDay.objects.filter(order=order).values_list('weekday', flat=True))
                total_hours = 0
                number_of_transfer = 0
                for i in weekday_list:
                    number_of_transfer += (days_count([int(i)], order.start_datetime.date(), order.end_datetime.date()))
                    total_hours += (days_count([int(i)], order.start_datetime.date(), order.end_datetime.date())) * (order.end_time - order.start_time)
                order.work_hours = total_hours
                order.number_of_transfer = number_of_transfer
                order.amount_transfer_fee = transfer_fee * number_of_transfer
                one_day_work_hours = order.end_time - order.start_time
                if order.case.care_type == 'home':
                    if one_day_work_hours < 12:
                        wage = servant.home_hour_wage
                    elif one_day_work_hours >=12 and total_hours < 24:
                        wage = round(servant.home_half_day_wage/12)
                elif order.case.care_type == 'hospital':
                    if one_day_work_hours < 12:
                        wage = servant.hospital_hour_wage
                    elif one_day_work_hours >=12 and total_hours < 24:
                        wage = round(servant.hospital_half_day_wage/12)
            else:
                order.number_of_transfer = 1
                order.amount_transfer_fee = transfer_fee * 1
                # diff = order.end_datetime - order.start_datetime
                # days, seconds = diff.days, diff.seconds
                # hours = days * 24 + seconds // 3600
                # minutes = (seconds % 3600) // 60
                # total_hours = hours + round(minutes/60)
                total_hours = continuous_time_cal(order)
                order.work_hours = total_hours
                if order.case.care_type == 'home':
                    if total_hours < 12:
                        wage = servant.home_hour_wage
                    elif total_hours >=12 and total_hours < 24:
                        wage = round(servant.home_half_day_wage/12)
                    else:
                        wage = round(servant.home_one_day_wage/24)
                elif order.case.care_type == 'hospital':
                    if total_hours < 12:
                        wage = servant.hospital_hour_wage
                    elif total_hours >=12 and total_hours < 24:
                        wage = round(servant.hospital_half_day_wage/12)
                    else:
                        wage = round(servant.hospital_one_day_wage/24)
            order.wage_hour =wage
            order.base_money = order.work_hours * wage

            # need to change in the future
            order.platform_percent = platform_percent_cal(user,order)
            order.save()
            Review.objects.create(order=order,case=order.case,servant=order.case.servant)
            if service_ids != []:
                for service_id in service_ids:
                    if int(service_id) <= 4:
                        orderIncreaseService = OrderIncreaseService()
                        orderIncreaseService.order = order
                        orderIncreaseService.service = Service.objects.get(id=service_id)
                        if UserServiceShip.objects.filter(user=servant,service=Service.objects.get(id=service_id)).count() > 0:
                            orderIncreaseService.increase_percent = UserServiceShip.objects.get(user=servant,service=Service.objects.get(id=service_id)).increase_percent
                        else:
                            orderIncreaseService.increase_percent = 0
                        orderIncreaseService.increase_money = (order.base_money) * (orderIncreaseService.increase_percent)/100
                        orderIncreaseService.save()

            if OrderIncreaseService.objects.filter(order=order,service__is_increase_price=True).count() != 0:
                order.total_money = ((order.base_money) + (OrderIncreaseService.objects.filter(order=order,service__is_increase_price=True).aggregate(Sum('increase_money'))['increase_money__sum'])) * ((100 - order.platform_percent)/100)
            else:
                order.total_money = order.base_money
            order.platform_money = order.total_money * (order.platform_percent/100)
            order.save()
            receiveBooking(servant,order)
            chatroom_ids1 = list(ChatroomUserShip.objects.filter(user=case.user).values_list('chatroom', flat=True))
            chatroom_ids2 = list(ChatroomUserShip.objects.filter(user=servant).values_list('chatroom', flat=True))
            chatroom_set = set(chatroom_ids1).intersection(set(chatroom_ids2))
            if list(chatroom_set) != []:
                chatroom_id = list(chatroom_set)[0]
                print(chatroom_id)
                chatroom = ChatRoom.objects.get(id=chatroom_id)
                message = ChatroomMessage(user=user,case=case,chatroom=chatroom,is_this_message_only_case=True)
                message.save()
            elif list(chatroom_set) == []:
                chatroom = ChatRoom()
                chatroom.save()
                ChatroomUserShip.objects.create(user=user,chatroom=chatroom)
                ChatroomUserShip.objects.create(user=servant,chatroom=chatroom)
                message = ChatroomMessage(user=user,case=case,chatroom=chatroom,is_this_message_only_case=True)
                message.save()
            chatroom.update_at = datetime.datetime.now()
            chatroom.save()
            tempcase.delete()
        return redirect('index')
    elif request.method == 'POST' and 'previous' in request.POST:
        return redirect('request_form_contact')
    return render(request, 'web/request_form/confirm.html',{'servants':servants, 'body_condition_list':body_condition_list,'service_list':service_list,'increase_service_list':increase_service_list, 'disease_list':disease_list, 'tempcase':tempcase, 'care_type':care_type,'start_date_str':start_date_str,'end_date_str':end_date_str,'time_type':time_type,'start_time_str':start_time_str,'end_time_str':end_time_str})
    
def recommend_carer(request):
    servants = User.objects.filter(is_servant_passed=True)
    servants = servants.exclude(is_home=False,is_hospital=False)
    citys = City.objects.all()
    city_id = ''
    care_type = ''
    if request.method == 'POST':
            
        if request.POST.get('city') != None:
            city_id = request.POST.get("city")
        care_type = request.POST.get('care_type')

        

        servants = servants.filter(user_locations__city=City.objects.get(id=city_id))
        if care_type !='':
            if care_type == 'home':
                servants = servants.filter(is_home=True)
            elif care_type == 'hospital':
                servants = servants.filter(is_hospital=True)
    if city_id == '':
        city = ''
    else:
        city = City.objects.get(id=city_id)
    
    return render(request, 'web/recommend_carer.html',{'servants':servants,'care_type':care_type, 'cityName':city,'citys':citys})

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

def about(request):
    return render(request, 'web/about.html')

def privacy_policy(request):
    return render(request, 'web/privacy_policy.html')

def terms_of_service(request):
    return render(request, 'web/terms_of_service.html')

def faq(request):
    assistanceposts = AssistancePost.objects.all()
    return render(request, 'web/faq.html',{'assistanceposts':assistanceposts})

def time_format_change(time_int):
    hour = int(time_int) 
    minute = int((time_int - int(time_int)) * 60)
    if hour < 10:
        if minute < 10:
            return '0'+ str(hour) + ":0" + str(minute)
        else:
            return '0'+ str(hour) + ":" + str(minute)
    else:
        if minute < 10:
            return  str(hour) + ":0" + str(minute)
        else:
            return  str(hour) + ":" + str(minute)

def continuous_time_cal(order):
    start_time = time_format_change(order.start_time) 
    end_time = time_format_change(order.end_time) 
    print('test01',start_time,end_time)
    start_time = datetime.datetime.strptime(start_time,"%H:%M").time()
    end_time = datetime.datetime.strptime(end_time,"%H:%M").time()
    print('test02',start_time,end_time)
    start_datetime = datetime.datetime.combine(order.start_datetime.date(),start_time)
    end_datetime = datetime.datetime.combine(order.end_datetime.date(),end_time)
    diff = end_datetime - start_datetime
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    total_hours = hours + round(minutes/60)
    return total_hours

def platform_percent_cal(user,order):
    orders = Order.objects.all()
    today = datetime.datetime.today()
    current_year = today.year
    current_month = today.month
    base_percent = 2.8
    work_hours = order.work_hours
    orders_total_hours = work_hours 
    if orders.filter(user=user,start_datetime__year=current_year,start_datetime__month=current_month,state='paid').count() != 0:
        accumulate_work_hours = orders.filter(user=user,start_datetime__year=current_year,start_datetime__month=current_month,state='paid').aggregate(Sum('work_hours'))['work_hours__sum']
        print('accumulate_work_hours',accumulate_work_hours)
        orders_total_hours += accumulate_work_hours
    
    if orders_total_hours < 120:
        return (base_percent + 6.5)
    elif orders_total_hours >= 120 and orders_total_hours < 240 :
        return (base_percent + 5.5)
    elif orders_total_hours >= 240 and orders_total_hours < 360 :
        return (base_percent + 4.5)
    elif orders_total_hours > 360 :
        return (base_percent + 4)

def chat(request):
    return render(request, 'web/chat.html')