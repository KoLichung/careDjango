from rest_framework import serializers
from modelCore.models import User, MarkupItem, Category, LanguageSkill, License, Servant, ServantMarkupItemPrice, ServantSkillShip,UserLicenseShipImage, ServantLicenseShipImage, ServantCategoryShip, Recipient, ServiceItem, City, CityArea, Transportation, Case,OrderState, Order, OrderReview , CaseServiceItemShip 

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id',)

    def save(self):
        user = User(phone=self.validated_data['phone'], name=self.validated_data['name'])
        password = self.validated_data['password']
        # password2 = self.validated_data['password2']
        # if password != password2:
        #     raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user
class MarkupItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkupItem
        fields = '__all__'
        read_only_fields = ('id',)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('id',)


class LanguageSkillSerializer(serializers.ModelSerializer):
    coverImage = serializers.CharField(read_only=True)

    class Meta:
        model = LanguageSkill
        fields = '__all__'
        read_only_fields = ('id','coverImage')

class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = '__all__'
        read_only_fields = ('id',)

class ServantSerializer(serializers.ModelSerializer):
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
        model = ServantSkillShip
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

class ServantCategoryShipSerializer(serializers.ModelSerializer):
    servant_name = serializers.CharField(read_only=True)
    category_CareType = serializers.CharField(read_only=True)
    category_TimeType = serializers.CharField(read_only=True)
    class Meta:    
        model = ServantCategoryShip
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

class CitySerializer(serializers.ModelSerializer):
    class Meta:    
        model = City
        fields = '__all__'
        read_only_fields = ('id',)

class CityAreaSerializer(serializers.ModelSerializer):
    class Meta:    
        model = CityArea
        fields = '__all__'
        read_only_fields = ('id',)
        
class TransportationSerializer(serializers.ModelSerializer):
    servant_name = serializers.CharField(read_only=True)
    cityarea_name = serializers.CharField(read_only=True)
    class Meta:    
        model = Transportation
        fields = '__all__'
        read_only_fields = ('id',)

class CaseSerializer(serializers.ModelSerializer):
    servant_name = serializers.CharField(read_only=True)
    recipient_name = serializers.CharField(read_only=True)
    cityarea_name = serializers.CharField(read_only=True)
    category_CareType = serializers.CharField(read_only=True)
    category_TimeType = serializers.CharField(read_only=True)
    case_date = serializers.CharField(read_only=True)
    basic_price = serializers.CharField(read_only=True)
    hour_wage = serializers.CharField(read_only=True)
    working_hours = serializers.CharField(read_only=True)
    markup_Item = serializers.CharField(read_only=True)
    markup_Item_percent = serializers.CharField(read_only=True)
    markup_price = serializers.CharField(read_only=True)
    total_price = serializers.CharField(read_only=True)
    recipient_gender = serializers.CharField(read_only=True)
    recipient_age = serializers.CharField(read_only=True)
    recipient_weight = serializers.CharField(read_only=True)
    recipient_disease = serializers.CharField(read_only=True)
    recipient_conditions = serializers.CharField(read_only=True)
    recipient_disease_info = serializers.CharField(read_only=True)
    recipient_conditions_info = serializers.CharField(read_only=True)
    service_Item= serializers.CharField(read_only=True)
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
        

