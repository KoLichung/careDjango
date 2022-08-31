from django.shortcuts import render,redirect
from django.core.paginator import Paginator

import datetime
from modelCore.models import BlogCategory, BlogPost, BlogPostCategoryShip

def all_cases(request):
    return render(request, 'backboard/all_cases.html')

def all_members(request):
    return render(request, 'backboard/all_members.html')

def bills(request):
    return render(request, 'backboard/bills.html')

def case_detail(request):
    return render(request, 'backboard/case_detail.html')

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

        blogPost.title = request.POST.get('title') 
        blogPost.body = request.POST.get('content') 
        blogPost.state = request.POST.get('post')
        blogPost.create_date = datetime.datetime.now()

        if blogPost.state == 'publish':
            blogPost.publish_date = datetime.datetime.now()
        
        if blogPost.title != None and blogPost.title != '':
            blogPost.save()

            for category in categories:
                if request.POST.get(f'check_category_{category.id}') != None:
                    BlogPostCategoryShip.objects.create(post=blogPost, category=category)

        return redirect('all_blogs')

    if request.GET.get('post_id') != None:
        blogPost = BlogPost.objects.get(id=request.GET.get('post_id'))
        category_ids = list(BlogPostCategoryShip.objects.filter(post=blogPost).values_list('category', flat=True))
        checkedCatories = BlogCategory.objects.filter(id__in=category_ids)
        return render(request, 'backboard/new_blog.html', {'categories': categories, 'post':blogPost, 'checkedCatories':checkedCatories})

    return render(request, 'backboard/new_blog.html', {'categories': categories})