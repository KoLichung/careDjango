from django.contrib import admin
from .models import ServantCityAreaShip, User, MarkupItem, Category, LanguageSkill, License, Servant, ServantMarkupItemPrice
from .models import ServantSkillShip,UserLicenseShipImage, ServantLicenseShipImage, ServantCategoryShip, Recipient, ServiceItem,  CityArea, Transportation, Case,OrderState, Order, OrderReview , CaseServiceItemShip 
from .models import City, CityArea

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone')

@admin.register(MarkupItem)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Category)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'care_type', 'time_type')

@admin.register(LanguageSkill)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(License)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Servant)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','user','gender')

@admin.register(ServantMarkupItemPrice)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'servant','markup_item','pricePercent')

@admin.register(ServantSkillShip)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'servant','languageSkill')

@admin.register(UserLicenseShipImage)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','license','image')

@admin.register(ServantLicenseShipImage)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'servant','license','image')

@admin.register(ServantCategoryShip)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'servant','category')

@admin.register(Recipient)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','user','gender','age','weight')

@admin.register(ServiceItem)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(City)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(CityArea)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'city','area')

@admin.register(ServantCityAreaShip)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'servant','cityarea')
    
@admin.register(Transportation)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'servant','cityarea','price')

@admin.register(Case)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient','servant','cityarea','category','start_date','end_date','start_time','end_time')

    
@admin.register(Order)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','case','state','createdate')

@admin.register(OrderReview)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'order','user_score','user_review_createdate','servant_score','servant_review_createdate')

@admin.register(CaseServiceItemShip)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'case','service_item')



