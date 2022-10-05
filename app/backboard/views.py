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
from modelCore.models import BlogCategory, BlogPost, BlogPostCategoryShip ,Case ,Order ,Review ,Service ,UserServiceShip ,CaseServiceShip
from modelCore.models import OrderIncreaseService, MonthSummary ,User ,UserLicenseShipImage ,License ,AssistancePost ,UserStore ,City ,County
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

    cases = Case.objects.all()
    state = request.GET.get('state')
    if state != None:
        cases = cases.filter(state=state)
    paginator = Paginator(cases, 10)
    if request.GET.get('page') != None:
        page_number = request.GET.get('page') 
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)
    return render(request, 'backboard/all_cases.html',{'cases':page_obj})

def all_members(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    users = User.objects.filter(is_staff=False)
    members_num = users.count()
    needers_num = users.filter(is_servant_passed=False).count()
    servants_num = users.filter(is_servant_passed=True).count()
    apply_servant_num = users.filter(is_apply_servant=True,is_servant_passed=False).count()
    member = request.GET.get('member')
    if member == 'needer':
        users = users.filter(is_servant_passed=False)
    elif member == 'servant':
        users = users.filter(is_servant_passed=True)
    elif member == 'apply_servant':
        users = users.filter(is_apply_servant=True,is_servant_passed=False)
    paginator = Paginator(users, 10)
    if request.GET.get('page') != None:
        page_number = request.GET.get('page') 
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)
    return render(request, 'backboard/all_members.html',{'users':page_obj,'members_num':members_num,'needers_num':needers_num,'servants_num':servants_num,'apply_servant_num':apply_servant_num})

def bills(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')
    
    # summarys = MonthSummary.objects.all().order_by('-id')[:2]
    summarys = MonthSummary.objects.all().order_by('-month_date')[:2]
    this_month_day = summarys[0].month_date
    last_month_day = this_month_day - datetime.timedelta(days=30)

    return render(request, 'backboard/bills.html', {'summarys':summarys,  'this_month_day':this_month_day, 'last_month_day':last_month_day})

def case_detail(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    case_id = request.GET.get('case')
    case = Case.objects.get(id=case_id)
    order = Order.objects.get(case=case)
    # review = Review.objects.get(case=case)
    order_increase_services = OrderIncreaseService.objects.filter(order=order)

    return render(request, 'backboard/case_detail.html',{'order_increase_services':order_increase_services, 'case':case,'order':order, 'order_increase_services':order_increase_services})

def member_detail(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    user_id = request.GET.get('user')
    user = User.objects.get(id=user_id)
    offend_orders = Order.objects.filter(user=user)
    take_orders = Order.objects.filter(servant=user)
    if request.method == 'POST' and 'reset_password' in request.POST :
        password = "00000"
        user.set_password(password)
        user.save()
    return render(request, 'backboard/member_detail.html',{'user':user,'offend_orders':offend_orders,'take_orders':take_orders})


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
            if request.POST.get('checkIsServant') == 'True':
                user.is_servant_passed = True
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
    citys = City.objects.all()
    cityName = citys.get(id=8)
    counties = County.objects.filter(city=cityName)
    countyName = counties.get(name='西屯區')

    # if request.method == "POST":
    #     s
    #     ID_card_name = request.POST.get('ID_card_name')
    #     ID_number = request.POST.get('ID_number')
    #     birthday = request.POST.get('birthday')
    #     ID_card_number = request.POST.get('ID_card_number')
    #     ReissueOrChange = request.POST.get('ReissueOrChange')
    #     city = request.POST.get('city')
    #     county = request.POST.get('county')
    #     ID_card_name = request.POST.get('ID_card_name')

    #     post_url = 'https://ccore.Newebpay.com/API/AddMerchant'
    #     timeStamp = int( time.time() )
    #     PartnerID_ = "CARE168"
    #     key = "Oq1IRY4RwYXpLAfmnmKkwd26bcT6q88q"
    #     iv = "CeYa8zoA0mX4qBpP"
    #     data = {
    #             "Version" : "1.8",
    #             "TimeStamp": timeStamp,
    #             "MemberPhone": "0987-654321",
    #             "MemberAddress": "台南市中西區民族路27號",
    #             "ManagerName": user.name,
    #             "ManagerNameE": "Sheng Jie,Fang",
    #             "LoginAccount": "scottman2022",
    #             "ManagerMobile": str(user.phone),
    #             "ManagerEmail": "jason@kosbrother.com",
    #             "DisputeMail": "jason@kosbrother.com",
    #             "MerchantEmail": "jason@kosbrother.com",
    #             "MerchantID": "ACE00013",
    #             "MCType": 1,
    #             "MerchantName": "杏心測試十",
    #             "MerchantNameE": "XinshingTest10",
    #             "MerchantWebURL": "http://test.com",
    #             "MerchantAddrCity": "台南市",
    #             "MerchantAddrArea": "中西區",
    #             "MerchantAddrCode": "700",
    #             "MerchantAddr": "民族路27號",
    #             "MerchantEnAddr": "No. 132, Sec. 2, Minzu Rd., West Central Dist., Tainan City 700 , Taiwan (R.O.C.)",
    #             "NationalE": "Taiwan",
    #             "CityE": "Tainan City",
    #             "PaymentType": "CREDIT:1|WEBATM:0|VACC:0|CVS:0|BARCODE:0|EsunWallet:0|TaiwanPay:0",
    #             "MerchantType": 2,
    #             "BusinessType": "8999",
    #             "MerchantDesc": "test",
    #             "BankCode": user.ATMInfoBankCode,
    #             "SubBankCode": str(user.ATMInfoBranchBankCode),
    #             "BankAccount": user.ATMInfoAccount,
    #             "AccountName": "齊家科技股份有限公司",
    #             "CreditAutoType": 1,
    #             "AgreedDay": "CREDIT:0",
    #             "Withdraw": "",
    #             "WithdrawMer": "",
    #             "WithdrawSetting" : "Withdraw=9",
    #             "NotifyURL": "http://202.182.105.11/newebpayApi/notifyurl_callback/2/",
                
    #     }
    #     if UserLicenseShipImage.objects.get(user=user,license=License.objects.get(id=1)).image != None:
    #         IDPic = 0
    #     else:
    #         IDPic = 1
    #     extend_params_personal = {
    #         "MemberUnified": "D122776945",
    #         "IDCardDate": "1070124",
    #         "IDCardPlace": "南市",
    #         "IDPic": IDPic,
    #         "IDFrom": 2,
    #         "Date": "19850911",
    #         "MemberName": user.name,
    #     }

    #     data.update(extend_params_personal)
    #     # data.update(extend_params_company)

    #     query_str = urllib.parse.urlencode(data)
    #     encrypt_data = module.aes256_cbc_encrypt(query_str, key, iv)
    #     resp = requests.post(post_url, data ={"PartnerID_":PartnerID_, "PostData_":encrypt_data})
    #     return response(json.loads(resp.text))

    return render(request, 'backboard/userstore_detail.html',{'user':user,'userLicenseImages':userLicenseImages,'cityName':cityName,'citys':citys,'countyName':countyName,'counties':counties})

def refunds(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    case_id = request.GET.get('case')
    case = Case.objects.get(id=case_id)
    order = Order.objects.get(case=case)
    if request.method == 'POST':
        refund_money = request.POST.get('refund_money')
        if refund_money != '' and refund_money != None:
            order.refund_money = int(refund_money)
        order.refund_apply_date = datetime.datetime.now()
        order.save()
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
