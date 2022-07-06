from rest_framework import serializers

from modelCore.models import User, City, County,Service,UserWeekDayTime,UserServiceShip ,Language ,UserLanguage , License, UserLicenseShipImage
from modelCore.models import UserServiceLocation, Case, DiseaseCondition,BodyCondition,CaseDiseaseShip,CaseBodyConditionShip ,CaseWeekDayTime 
from modelCore.models import CaseServiceShip ,Order ,Review ,PayInfo ,Message ,SystemMessage

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

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'
        read_only_fields = ('id',)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('id',)

class UserServiceLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserServiceLocation
        fields = '__all__'
        read_only_fields = ('id',)

class CaseWeekDayTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseWeekDayTime
        fields = '__all__'
        read_only_fields = ('id',)

class UserWeekDayTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWeekDayTime
        fields = '__all__'
        read_only_fields = ('id',)

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('id',)

class SystemMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemMessage
        fields = '__all__'
        read_only_fields = ('id',)

class ServantSerializer(serializers.ModelSerializer):
    locations = UserServiceLocationSerializer(read_only=True, many=True)
    rate_num = serializers.IntegerField(default=0)
    
    class Meta:
        model = User
        fields = ('id', 'name', 'image', 'rating', 'is_home', 'home_hour_wage', 'home_half_day_wage', 'home_one_day_wage', 'is_hospital', 'hospital_hour_wage', 'hospital_half_day_wage', 'hospital_one_day_wage', 'locations', 'rate_num')
        read_only_fields = ('id',)
        

