from django.shortcuts import render,redirect
from django.core.paginator import Paginator
import urllib
import datetime
from modelCore.forms import BlogPostCoverImageForm
from modelCore.models import BlogCategory, BlogPost, BlogPostCategoryShip ,Case ,Order ,Review ,Service ,UserServiceShip ,CaseServiceShip
from modelCore.models import OrderIncreaseService, MonthSummary ,User ,UserLicenseShipImage ,License
from django.contrib import auth
from django.contrib.auth import authenticate

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
    users = User.objects.filter(is_staff=False)
    paginator = Paginator(users, 10)
    if request.GET.get('page') != None:
        page_number = request.GET.get('page') 
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)
    return render(request, 'backboard/all_members.html',{'users':page_obj})

def bills(request):
    summarys = MonthSummary.objects.all().order_by('-id')[:2]
    this_month_day = summarys[0].month_date
    last_month_day = this_month_day - datetime.timedelta(days=30)

    return render(request, 'backboard/bills.html', {'summarys':summarys,  'this_month_day':this_month_day, 'last_month_day':last_month_day})

def case_detail(request):
    case_id = request.GET.get('case')
    case = Case.objects.get(id=case_id)
    order = Order.objects.get(case=case)
    review = Review.objects.get(case=case)
    order_increase_services = OrderIncreaseService.objects.filter(order=order)

    return render(request, 'backboard/case_detail.html',{'order_increase_services':order_increase_services, 'case':case,'review':review,'order':order, 'order_increase_services':order_increase_services})

def member_detail(request):
    user_id = request.GET.get('user')
    user = User.objects.get(id=user_id)
    offend_orders = Order.objects.filter(user=user)
    take_orders = Order.objects.filter(servant=user)
    return render(request, 'backboard/member_detail.html',{'user':user,'offend_orders':offend_orders,'take_orders':take_orders})

def all_blogs(request):
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
    if request.GET.get('delete_id') != None:
        try:
            BlogCategory.objects.get(id=request.GET.get('delete_id')).delete()
        except:
            print("no such category")

    categories = BlogCategory.objects.all()
    return render(request, 'backboard/all_categories.html', {'categories':categories})

def new_edit_category(request):

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
    user_id = request.GET.get('user')
    user = User.objects.get(id=user_id)
    licences = License.objects.all().order_by('id')
    for license in licences:
        if UserLicenseShipImage.objects.filter(user=user, license=license).count() == 0:
            UserLicenseShipImage.objects.create(user=user,license=license)
    userLicenseImages = UserLicenseShipImage.objects.filter(user=user).order_by('license')
    if request.method == 'POST' :
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

    return render(request, 'backboard/member_data_review.html',{'user':user,'userLicenseImages':userLicenseImages})

def refunds(request):
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

def redirect_params(url, params=None):
    response = redirect(url)
    if params:
        query_string = urllib.parse.urlencode(params)
        response['Location'] += '?' + query_string
    return response
