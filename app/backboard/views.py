from django.shortcuts import render

# Create your views here.

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
    return render(request, 'backboard/all_blogs.html')

def new_blog(request):
    return render(request, 'backboard/new_blog.html')