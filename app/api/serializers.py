from asyncore import read
from email.policy import default
from unittest import case
from rest_framework import serializers

from modelCore.models import User, City, County,Service,UserWeekDayTime,UserServiceShip ,Language ,UserLanguage , License, UserLicenseShipImage
from modelCore.models import UserServiceLocation, Case, DiseaseCondition,BodyCondition,CaseDiseaseShip,CaseBodyConditionShip ,ChatRoom
from modelCore.models import CaseServiceShip ,Order ,Review ,PayInfo ,Message ,SystemMessage ,OrderIncreaseService

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id',)

class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = '__all__'
        read_only_fields = ('id',)

class LangaugeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'
        read_only_fields = ('id',)

class ServiceSerializer(serializers.ModelSerializer):
    increase_percent = serializers.IntegerField(default=0)
    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ('id',)

class DiseaseConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseCondition
        fields = '__all__'
        read_only_fields = ('id',)

class BodyConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyCondition
        fields = '__all__'
        read_only_fields = ('id',)

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'
        read_only_fields = ('id',)

class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = '__all__'
        read_only_fields = ('id',)

class UserLangaugeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLanguage
        fields = '__all__'
        read_only_fields = ('id',)

class UserServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserServiceShip
        fields = '__all__'
        read_only_fields = ('id',)

class UserServiceLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserServiceLocation
        fields = '__all__'
        read_only_fields = ('id',)

class UserWeekDayTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWeekDayTime
        fields = '__all__'
        read_only_fields = ('id',)

class ReviewSerializer(serializers.ModelSerializer):
    care_type = serializers.CharField(default='')
    is_continuous_time = serializers.CharField(default='')
    start_datetime = serializers.CharField(default='')
    end_datetime = serializers.CharField(default='')
    user_avg_rate = serializers.IntegerField(default=0)
    user_rating_nums= serializers.IntegerField(default=0)
    servant_name = serializers.CharField(default='')
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('id',)

class ServantSerializer(serializers.ModelSerializer):
    locations = UserServiceLocationSerializer(read_only=True, many=True)
    avg_rate = serializers.IntegerField(default=0)
    background_image_url = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    services = ServiceSerializer(read_only=True, many=True)
    licences = LicenseSerializer(read_only=True, many=True)
    about_me = serializers.CharField(default='')
    reviews = ReviewSerializer(read_only=True, many=True)
    rating_nums = serializers.IntegerField(default=0)
    
    class Meta:
        model = User
        fields = ('id', 'name', 'image', 'servant_avg_rating', 'is_home', 'home_hour_wage', 'home_half_day_wage', 'home_one_day_wage', 'is_hospital', 'hospital_hour_wage', 'hospital_half_day_wage', 'hospital_one_day_wage', 'locations', 'rating_nums', 'background_image_url', 'services', 'licences', 'about_me', 'reviews','avg_rate')
        read_only_fields = ('id',)

class OrderIncreaseServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderIncreaseService
        fields = '__all__'
        read_only_fields = ('id',)

class CaseSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(read_only=True, many=True)
    disease = DiseaseConditionSerializer(read_only=True, many=True)
    body_condition = BodyConditionSerializer(read_only=True, many=True)
    review = ReviewSerializer(read_only=True, many=False)
    rating_nums = serializers.IntegerField(default=0)
    servant_rating = serializers.IntegerField(default=0)
    avg_offender_rating = serializers.FloatField(default=0)
    status = serializers.CharField(default='')
    hour_wage = serializers.IntegerField(default=0)
    work_hours = serializers.IntegerField(default=0)
    base_money = serializers.IntegerField(default=0)
    platform_percent = serializers.FloatField(default=0)
    platform_money = serializers.IntegerField(default=0)
    total_money = serializers.IntegerField(default=0)
    increase_money = OrderIncreaseServiceSerializer(read_only=True, many=True)
    user_detail = UserSerializer(read_only=True)
    servant_candidate = UserSerializer(read_only=True, many=True)
    num_offender_rating = serializers.IntegerField(default=0)
    servant_name = serializers.CharField(default='')

    class Meta:
        model = Case
        fields = '__all__'
        read_only_fields = ('id',)

class OrderSerializer(serializers.ModelSerializer):
    related_case = CaseSerializer(read_only=True)
    servants = ServantSerializer(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('id',)

class MessageSerializer(serializers.ModelSerializer):
    message_is_mine = serializers.BooleanField(default=False)
    order = OrderSerializer(read_only=True)
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('id',)

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'
        read_only_fields = ('id',)

class SystemMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemMessage
        fields = '__all__'
        read_only_fields = ('id',)