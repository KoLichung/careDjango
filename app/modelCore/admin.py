from django.contrib import admin
from .models import  ChatroomUserShip, User, City, County,Service,UserWeekDayTime,UserServiceShip ,Language ,UserLanguage , License, UserLicenseShipImage
from .models import  UserServiceLocation, Case, DiseaseCondition,BodyCondition,CaseDiseaseShip,CaseBodyConditionShip ,ChatRoom , ChatroomUserShip
from .models import  CaseServiceShip ,Order ,Review ,PayInfo ,Message ,SystemMessage ,OrderWeekDay ,OrderIncreaseService

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone')

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'name')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'remark','is_increase_price')

@admin.register(UserWeekDayTime)
class UserWeekDayTimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'weekday', 'start_time', 'end_time')

@admin.register(UserServiceShip)
class UserServiceShipAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service')

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(UserLanguage)
class UserLanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'language', 'remark')

@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'remark')

@admin.register(UserLicenseShipImage)
class UserLicenseShipImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'license', 'image')

@admin.register(UserServiceLocation)
class UserServiceLocationAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'city', 'county', 'tranfer_fee')

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'servant', 'city', 'county', 'care_type', 'start_datetime', 'end_datetime')

@admin.register(DiseaseCondition)
class DiseaseConditionAdmin(admin.ModelAdmin):
    list_display = ('id','name')

@admin.register(BodyCondition)
class BodyConditionAdmin(admin.ModelAdmin):
    list_display = ('id','name')

@admin.register(CaseDiseaseShip)
class CaseDiseaseShipAdmin(admin.ModelAdmin):
    list_display = ('id', 'case', 'disease')

@admin.register(CaseBodyConditionShip)
class CaseBodyConditionShipAdmin(admin.ModelAdmin):
    list_display = ('id', 'case', 'body_condition')

@admin.register(CaseServiceShip)
class CaseServiceShipAdmin(admin.ModelAdmin):
    list_display = ('id','case', 'service')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','case', 'user','state','total_money')

@admin.register(OrderIncreaseService)
class OrderWeekDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'service', 'increase_percent', 'increase_money')

@admin.register(OrderWeekDay)
class OrderWeekDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'weekday')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'case', 'servant', 'case_offender_rating', 'servant_rating')

@admin.register(PayInfo)
class PayInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'order')

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'update_at')

@admin.register(ChatroomUserShip)
class ChatroomUserShipAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'chatroom')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'case')

@admin.register(SystemMessage)
class SystemMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'case')


