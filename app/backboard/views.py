from django.shortcuts import render,redirect
from django.core.paginator import Paginator

import datetime
from modelCore.forms import BlogPostCoverImageForm
from modelCore.models import BlogCategory, BlogPost, BlogPostCategoryShip ,Case ,Order ,Review ,Service ,UserServiceShip ,CaseServiceShip
from modelCore.models import OrderIncreaseService, MonthSummary

def all_cases(request):
    cases = Case.objects.all()
    return render(request, 'backboard/all_cases.html',{'cases':cases})

def all_members(request):
    return render(request, 'backboard/all_members.html')

def bills(request):
    summarys = MonthSummary.objects.all().order_by('-id')[:2]
    this_month_day = summarys[0].month_date
    last_month_day = this_month_day - datetime.timedelta(days=30)

    return render(request, 'backboard/bills.html', {'summarys':summarys,  'this_month_day':this_month_day, 'last_month_day':last_month_day})

def case_detail(request):
    case_id = request.GET.get('case')
    case = Case.objects.get(id=case_id)
    servant = case.servant
    order = Order.objects.get(case=case)
    review = Review.objects.get(case=case)

    order_increase_services = OrderIncreaseService.objects.filter(order=order)

    return render(request, 'backboard/case_detail.html',{'case':case,'review':review,'order':order, 'order_increase_services':order_increase_services})

def member_detail(request):
    return render(request, 'backboard/member_detail.html')

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
    return render(request, 'backboard/member_data_review.html')

def refunds(request):
    return render(request, 'backboard/refunds.html')
