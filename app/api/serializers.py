from rest_framework import serializers
from modelCore.models import User, MarkupItem, License, Servant,ServantWeekdayTime, ServantMarkupItemPrice, ServantSkill,UserLicenseShipImage
from modelCore.models import ServantLicenseShipImage, Recipient, ServiceItem, City, CityArea, Transportation, Case,OrderState, Order, OrderReview  
from modelCore.models import CaseServiceItemShip ,ServantServiceItemShip,Message,SystemMessage


class MarkupItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkupItem
        fields = '__all__'
        read_only_fields = ('id',)


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = '__all__'
        read_only_fields = ('id',)

class ServantSerializer(serializers.ModelSerializer):
    license_image = serializers.CharField(read_only=True)
    serviceTime = serializers.CharField(read_only=True)
    service_item = serializers.CharField(read_only=True)
    licenses = serializers.CharField(read_only=True)
    Languageskill = serializers.CharField(read_only=True)
    transportation = serializers.CharField(read_only=True)
    servant_ratedNum = serializers.CharField(read_only=True)
    score  = serializers.FloatField(read_only=True)
    mark_up_item = serializers.CharField(read_only=True)
    service_region = serializers.CharField(read_only=True)
    caregory_type = serializers.CharField(read_only=True)
    service_city = serializers.CharField(read_only=True)
    search_result_city = serializers.CharField(read_only=True)
    search_result_date= serializers.CharField(read_only=True)
    search_result_caretype= serializers.CharField(read_only=True)
    servant_detail_caretype = serializers.CharField(read_only=True)
    order_review = serializers.CharField(read_only=True)
    class Meta:
        model = Servant
        fields = '__all__'
        read_only_fields = ('id',)

class ServantMarkupItemPriceSerializer(serializers.ModelSerializer):
    servant_name = serializers.CharField(read_only=True)
    markup_item_name = serializers.CharField(read_only=True)
    class Meta:
        model = ServantMarkupItemPrice
        fields = '__all__'
        read_only_fields = ('id',)

class ServantSkillShipSerializer(serializers.ModelSerializer):
    servant_name = serializers.CharField(read_only=True)
    language_skill_name = serializers.CharField(read_only=True)
    class Meta:    
        model = ServantSkill
        fields = '__all__'
        read_only_fields = ('id','user')

class UserLicenseShipImageSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(read_only=True)
    license_name = serializers.CharField(read_only=True)
    class Meta:    
        model = UserLicenseShipImage
        fields = '__all__'
        read_only_fields = ('id',)

class ServantLicenseShipImageSerializer(serializers.ModelSerializer):
    servant_name = serializers.CharField(read_only=True)
    license_name = serializers.CharField(read_only=True)
    class Meta:    
        model = ServantLicenseShipImage
        fields = '__all__'
        read_only_fields = ('id',)


class RecipientSerializer(serializers.ModelSerializer):
    class Meta:    
        model = Recipient
        fields = '__all__'
        read_only_fields = ('id',)

class ServiceItemSerializer(serializers.ModelSerializer):
    class Meta:    
        model = ServiceItem
        fields = '__all__'
        read_only_fields = ('id',)


class CaseSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(read_only=True)
    servant_name = serializers.CharField(read_only=True)
    recipient_name = serializers.CharField(read_only=True)
    cityarea_name = serializers.CharField(read_only=True)
    CareType = serializers.CharField(read_only=True)
    TimeType = serializers.CharField(read_only=True)
    case_date = serializers.CharField(read_only=True)
    basic_price = serializers.CharField(read_only=True)
    hour_wage = serializers.CharField(read_only=True)
    working_hours = serializers.CharField(read_only=True)
    markup_Item = serializers.CharField(read_only=True)
    markup_Item_percent = serializers.CharField(read_only=True)
    markup_price = serializers.CharField(read_only=True)
    platform_fee = serializers.CharField(read_only=True)
    total_price = serializers.CharField(read_only=True)
    recipient_gender = serializers.CharField(read_only=True)
    recipient_age = serializers.CharField(read_only=True)
    recipient_weight = serializers.CharField(read_only=True)
    recipient_disease = serializers.CharField(read_only=True)
    recipient_conditions = serializers.CharField(read_only=True)
    recipient_disease_info = serializers.CharField(read_only=True)
    recipient_conditions_info = serializers.CharField(read_only=True)
    service_Item= serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    disease = serializers.CharField(read_only=True)
    conditions = serializers.CharField(read_only=True)
    class Meta:    
        model = Case
        fields = '__all__'
        read_only_fields = ('id',)

class CaseServiceItemShipSerializer(serializers.ModelSerializer):
    servant_name = serializers.CharField(read_only=True)
    recipient_name = serializers.CharField(read_only=True)
    serviceItem_name = serializers.CharField(read_only=True)
    cityarea_name = serializers.CharField(read_only=True)
    class Meta:    
        model = CaseServiceItemShip
        fields = '__all__'
        read_only_fields = ('id',)

class OrderStateSerializer(serializers.ModelSerializer):
    
    class Meta:    
        model = OrderState
        fields = '__all__'
        read_only_fields = ('id',)

class OrderSerializer(serializers.ModelSerializer):
    servant_name = serializers.CharField(read_only=True)
    recipient_name = serializers.CharField(read_only=True)
    cityarea_name = serializers.CharField(read_only=True)
    class Meta:    
        model = Order
        fields = '__all__'
        read_only_fields = ('id',)

class OrderReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(read_only=True)
    servant_name = serializers.CharField(read_only=True)
    recipient_name = serializers.CharField(read_only=True)
    cityarea_name = serializers.CharField(read_only=True)
    category_CareType = serializers.CharField(read_only=True)
    category_TimeType = serializers.CharField(read_only=True)
    case_date = serializers.CharField(read_only=True)
    class Meta:    
        model = OrderReview
        fields = '__all__'
        read_only_fields = ('id',)
        

