from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.http import HttpResponse ,JsonResponse ,HttpResponseRedirect ,response
import urllib
import datetime
from newebpayApi import module
import requests
import time
import json
from modelCore.forms import BlogPostCoverImageForm ,AssistancePostCoverImageForm
from modelCore.models import BlogCategory, BlogPost, BlogPostCategoryShip ,Case ,Order ,Review ,Service ,UserServiceShip ,CaseServiceShip, NewebpayCity
from modelCore.models import OrderIncreaseService, MonthSummary ,User ,UserLicenseShipImage ,License ,AssistancePost ,UserStore ,City ,County, UserServiceLocation
from django.contrib import auth
from django.contrib.auth import authenticate

def ajax_refresh_county(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.POST['action'] == 'refresh_county':
        updatedData = urllib.parse.parse_qs(request.body.decode('utf-8'))
        # print(updatedData)
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
        # print(data)
        return JsonResponse({'data':data})

def login(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']
        user = authenticate(request, phone=phone, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/backboard/all_cases')
        else:
            return redirect('/backboard/')

    return render(request, 'backboard/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/backboard/')

def all_cases(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    cases = Case.objects.all().order_by('-id')

    state = request.GET.get('state')
    if state != None and state != 'None':
        cases = cases.filter(state=state)
    
    paginator = Paginator(cases, 30)
    if request.GET.get('page') != None:
        page_number = request.GET.get('page') 
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)
    return render(request, 'backboard/all_cases.html',{'cases':page_obj,'state':state})

def all_members(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')
    
    if request.method == 'POST' and 'confirm' in request.POST :
        user = User.objects.get(id=request.POST.get('userId'))
        user.is_data_change = False
        user.save()
        return redirect('/backboard/all_members?member=data_change')

    users = User.objects.filter(is_staff=False).order_by('-id')
    members_num = users.count()
    needers_num = users.filter(is_servant_passed=False).count()
    servants_num = users.filter(is_servant_passed=True).count()
    apply_servant_num = users.filter(is_apply_servant=True,is_servant_passed=False).count()
    data_change_num = users.filter(is_data_change=True).count()

    member = request.GET.get('member')
    if member == 'needer':
        users = users.filter(is_servant_passed=False)
    elif member == 'servant':
        users = users.filter(is_servant_passed=True)
    elif member == 'apply_servant':
        users = users.filter(is_apply_servant=True,is_servant_passed=False)
    elif member == 'data_change':
        users = users.filter(is_data_change=True)

    paginator = Paginator(users, 30)
    if request.GET.get('page') != None:
        page_number = request.GET.get('page') 
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)
    return render(request, 'backboard/all_members.html',{'users':page_obj,'members_num':members_num,'needers_num':needers_num,'servants_num':servants_num,'apply_servant_num':apply_servant_num,'data_change_num':data_change_num,'member':member})

def bills(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')
    
    # summarys = MonthSummary.objects.all().order_by('-id')[:2]
    summarys = MonthSummary.objects.all().order_by('-month_date')[:2]
    this_month_day = summarys[0].month_date
    last_month_day = this_month_day - datetime.timedelta(days=20)

    return render(request, 'backboard/bills.html', {'summarys':summarys,  'this_month_day':this_month_day, 'last_month_day':last_month_day})

def case_detail(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    case_id = request.GET.get('case')
    case = Case.objects.get(id=case_id)
    
    if request.method == 'POST' and 'send_invoice' in request.POST:
        orderId = request.POST.get('orderId')
        from ezpay_invoice.tasks import send_invoice
        return_message = send_invoice(orderId)
        print(f'return message {return_message}')
        if return_message == 'SUCCESS':
            order = Order.objects.get(id=orderId)
            order.is_sent_invoice = True
            order.save()
        return redirect_params('case_detail',{'case':case_id})

    orders = Order.objects.filter(case=case)

    return render(request, 'backboard/case_detail.html',{'case':case,'orders':orders})

def member_detail(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    user_id = request.GET.get('user')
    user = User.objects.get(id=user_id)
    offend_orders = Order.objects.filter(user=user).order_by('-id')
    take_orders = Order.objects.filter(servant=user).order_by('-id')

    locations = UserServiceLocation.objects.filter(user=user)
    services = UserServiceShip.objects.filter(user=user)

    if request.method == 'POST' and 'reset_password' in request.POST :
        password = "12345"
        user.set_password(password)
        user.save()
    return render(request, 'backboard/member_detail.html',{'user':user,'offend_orders':offend_orders,'take_orders':take_orders,'locations':locations, 'services':services})


def all_blogs(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    if request.GET.get('delete_id') != None:
        BlogPost.objects.get(id=request.GET.get('delete_id')).delete()

    blogPosts = BlogPost.objects.all().order_by('-id')

    paginator = Paginator(blogPosts, 20)
    if request.GET.get('page') != None:
        page_number = request.GET.get('page') 
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)

    return render(request, 'backboard/all_blogs.html', {'blogPosts':page_obj})

# edit 跟 new 同一頁
def new_blog(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    categories = BlogCategory.objects.all()

    if request.method == 'POST':
        
        if request.GET.get('post_id') != None:
            blogPost = BlogPost.objects.get(id=request.GET.get('post_id'))
        else:
            blogPost = BlogPost()
            blogPost.create_date = datetime.datetime.now()

        blogPost.title = request.POST.get('title') 
        blogPost.body = request.POST.get('body') 
        blogPost.state = request.POST.get('post')
        
        if blogPost.state == 'publish':
            blogPost.publish_date = datetime.datetime.now()
        
        if blogPost.title != None and blogPost.title != '':

            if request.FILES.get('cover_image', False):
                blogPost.cover_image = request.FILES['cover_image']

            blogPost.save()

            for category in categories:
                if request.POST.get(f'check_category_{category.id}') != None:
                    BlogPostCategoryShip.objects.create(post=blogPost, category=category)

            # if request.FILES.get('cover_image', False):
            #     form = BlogPostCoverImageForm(request.POST, request.FILES)
            #     form.instance = 
            #     form.save()
            # else:
            #     print("no new file, do nothing")

        return redirect('all_blogs')

    if request.GET.get('post_id') != None:
        blogPost = BlogPost.objects.get(id=request.GET.get('post_id'))
        form = BlogPostCoverImageForm(instance=blogPost)
        category_ids = list(BlogPostCategoryShip.objects.filter(post=blogPost).values_list('category', flat=True))
        checkedCatories = BlogCategory.objects.filter(id__in=category_ids)
        return render(request, 'backboard/new_blog.html', {'categories':categories, 'post':blogPost, 'checkedCatories':checkedCatories, 'form':form})

    form = BlogPostCoverImageForm()
    return render(request, 'backboard/new_blog.html', {'categories':categories, 'form':form})

def all_categories(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    if request.GET.get('delete_id') != None:
        try:
            BlogCategory.objects.get(id=request.GET.get('delete_id')).delete()
        except:
            print("no such category")

    categories = BlogCategory.objects.all()
    return render(request, 'backboard/all_categories.html', {'categories':categories})

def new_edit_category(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    if request.method == 'POST':
        if request.POST.get('post') == 'save':
            if request.POST.get('name') != None and request.POST.get('name') != '':
                if request.GET.get('category_id') != None:
                    category = BlogCategory.objects.get(id=request.GET.get('category_id'))
                    category.name = request.POST.get('name')
                    category.save()
                else:
                    BlogCategory.objects.create(name=request.POST.get('name'))
        return redirect('all_categories')

    if request.GET.get('category_id') != None:
        category = BlogCategory.objects.get(id=request.GET.get('category_id'))
        return render(request, 'backboard/new_edit_category.html', {'category':category})

    return render(request, 'backboard/new_edit_category.html')

def member_data_review(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    user_id = request.GET.get('user')
    user = User.objects.get(id=user_id)
    licences = License.objects.all().order_by('id')
    if UserStore.objects.filter(user=user).count() == 0 :
        check_user_store = False
    else:
        check_user_store = True

    for license in licences:
        if UserLicenseShipImage.objects.filter(user=user, license=license).count() == 0:
            UserLicenseShipImage.objects.create(user=user,license=license)
    userLicenseImages = UserLicenseShipImage.objects.filter(user=user).order_by('license')

    if request.method == 'POST' :
        
        for userLicenseImage in userLicenseImages:
            if ('delete'+str(userLicenseImage.license.id)) in request.POST:
                userLicenseImage.image = None
                userLicenseImage.save()
        if 'post' in request.POST:

            if request.POST.get('check_apply_servant') == 'True':
                user.is_apply_servant = True
            else:
                user.is_apply_servant = False
            
            if request.POST.get('check_servant_passed') == 'True':
                if user.is_servant_passed == False:
                    # here need to notify this user by system message and fcm message
                    from messageApp.tasks import userBecomeServant
                    userBecomeServant(user)
                user.is_servant_passed = True
            else:
                user.is_servant_passed = False
            
            user.name = request.POST.get('name')
            user.ATMInfoBankCode = request.POST.get('ATMInfoBankCode')
            user.ATMInfoBranchBankCode = request.POST.get('ATMInfoBranchBankCode')
            user.ATMInfoAccount = request.POST.get('ATMInfoAccount')

            user.save()

            for userLicenseImage in userLicenseImages:
                checkLicenseImage = request.POST.get('check'+str(userLicenseImage.license.id))
                if checkLicenseImage == 'True':
                    userLicenseImage.isPassed = True
                    userLicenseImage.save()
            return redirect_params('member_detail',{'user':user.id})
        else:
            return redirect_params('member_detail',{'user':user.id})
        

    return render(request, 'backboard/member_data_review.html',{'user':user,'userLicenseImages':userLicenseImages,'check_user_store':check_user_store})

def userstore_detail(request):
    if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('/backboard/')

    user_id = request.GET.get('user')
    user = User.objects.get(id=user_id)
    userLicenseImages = UserLicenseShipImage.objects.filter(user=user).order_by('license')[:2]

    newebCitys = NewebpayCity.objects.all()
    citys = City.objects.all()
    cityName = citys.get(id=8)
    counties = County.objects.filter(city=cityName)
    countyName = counties.get(name='西屯區')

    return render(request, 'backboard/userstore_detail.html',{'user':user,'userLicenseImages':userLicenseImages,'cityName':cityName,'citys':citys,'countyName':countyName,'counties':counties, 'newebCitys':newebCitys})

def refunds(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    case_id = request.GET.get('case')
    case = Case.objects.get(id=case_id)
    order = Order.objects.get(case=case)
    if request.method == 'POST':
        refund_money = request.POST.get('refund_money')
        if refund_money != '' and refund_money != None:
            from newebpayApi.tasks import backboard_refound, approprivate_money_to_store, debit_money_to_platform
            result_approprivte = approprivate_money_to_store(order.id)
            if result_approprivte == 'SUCCESS':

                result = backboard_refound(order.id, refund_money)
                if result == "SUCCESS":
                    order.refund_money = int(refund_money)
                    order.refund_apply_date = datetime.datetime.now()
                    
                    order.total_money = order.total_money - order.refund_money

                    order.newebpay_money = round(order.total_money * (order.newebpay_percent/100))
                    order.platform_money = round(order.total_money * (order.platform_percent/100))
                    order.servant_money = order.total_money - order.newebpay_money - order.platform_money
                    order.save()

                    debit_money_to_platform(order.id, order.platform_money)

                    case.state = 'Complete'
                    case.save()

        return redirect_params('case_detail',{'case':case_id})
        
    return render(request, 'backboard/refunds.html',{'order':order})

def all_assistances(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    if request.GET.get('delete_id') != None:
        AssistancePost.objects.get(id=request.GET.get('delete_id')).delete()

    assistancePosts = AssistancePost.objects.all().order_by('-id')

    paginator = Paginator(assistancePosts, 20)
    if request.GET.get('page') != None:
        page_number = request.GET.get('page') 
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)

    return render(request, 'backboard/all_assistances.html', {'assistancePosts':page_obj})

# edit 跟 new 同一頁
def new_assistance(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    if request.method == 'POST':
        
        if request.GET.get('post_id') != None:
            assistancePost = AssistancePost.objects.get(id=request.GET.get('post_id'))
        else:
            assistancePost = AssistancePost()
            assistancePost.create_date = datetime.datetime.now()

        assistancePost.title = request.POST.get('title') 
        assistancePost.body = request.POST.get('body') 
        
        
        if assistancePost.title != None and assistancePost.title != '':

            if request.FILES.get('cover_image', False):
                assistancePost.cover_image = request.FILES['cover_image']

            assistancePost.save()

        return redirect('all_assistances')

    if request.GET.get('post_id') != None:
        assistancePost = AssistancePost.objects.get(id=request.GET.get('post_id'))
        form = AssistancePostCoverImageForm(instance=assistancePost)
        return render(request, 'backboard/new_assistance.html', { 'post':assistancePost,'form':form})

    form = AssistancePostCoverImageForm()
    return render(request, 'backboard/new_assistance.html', {'form':form})

def redirect_params(url, params=None):
    response = redirect(url)
    if params:
        query_string = urllib.parse.urlencode(params)
        response['Location'] += '?' + query_string
    return response
