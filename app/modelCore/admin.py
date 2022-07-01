from django.contrib import admin
from .models import  User, City, County

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone')

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'name')


