from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

import datetime
from datetime import date ,timedelta
from pytz import timezone
import pytz
from modelCore.models import User, City, County,Service,UserWeekDayTime,UserServiceShip ,Language ,UserLanguage , License, UserLicenseShipImage
from modelCore.models import UserServiceLocation, Case, DiseaseCondition,BodyCondition,CaseDiseaseShip,CaseBodyConditionShip ,CaseWeekDayTime 
from modelCore.models import CaseServiceShip ,Order ,Review ,PayInfo ,Message ,SystemMessage
from api import serializers

class LicenseViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = License.objects.all()
    serializer_class = serializers.LicenseSerializer

class LanguageViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = Language.objects.all()
    serializer_class = serializers.LangaugeSerializer

class ServiceViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = Service.objects.all()
    serializer_class = serializers.ServiceSerializer

class DiseaseConditionViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = DiseaseCondition.objects.all()
    serializer_class = serializers.DiseaseConditionSerializer

class BodyConditionViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = BodyCondition.objects.all()
    serializer_class = serializers.BodyConditionSerializer

class CityViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = City.objects.all()
    serializer_class = serializers.CitySerializer

class CountyViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = County.objects.all()
    serializer_class = serializers.CountySerializer

class CaseViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin):
    queryset = Case.objects.all()
    serializer_class = serializers.CaseSerializer

class OrderViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

class UserServiceLocationViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin):
    queryset = UserServiceLocation.objects.all()
    serializer_class = serializers.UserServiceLocationSerializer

class CaseWeekDayTimeViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin):
    queryset = CaseWeekDayTime.objects.all()
    serializer_class = serializers.CaseWeekDayTimeSerializer

class UserWeekDayTimeViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin):
    queryset = UserWeekDayTime.objects.all()
    serializer_class = serializers.UserWeekDayTimeSerializer

class MessageViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer

class SystemMessageViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = SystemMessage.objects.all()
    serializer_class = serializers.SystemMessageSerializer

class SearchServantViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,):

    queryset = User.objects.all()
    serializer_class = serializers.ServantSerializer

    def get_queryset(self):
        care_type= self.request.query_params.get('care_type')
        city = self.request.query_params.get('city')
        county = self.request.query_params.get('county')
        is_continuous_time = self.request.query_params.get('is_continuous_time')
        #2022-07-10T00:00:00Z
        start_datetime = self.request.query_params.get('start_datetime')
        end_datetime = self.request.query_params.get('end_datetime')
        #1,3,5
        weekdays = self.request.query_params.get('weekdays')
        #0800:2200
        start_end_time = self.request.query_params.get('start_end_time')

        queryset = User.objects.filter(is_servant=True)
        if care_type == 'home':
            queryset = queryset.filter(is_home=True)
        elif care_type == 'hospital':
            queryset = queryset.filter(is_hospital=True)
        else: 
            pass
        if city != None:
            queryset = queryset.filter(user_locations__city=City.objects.get(id=city))
        if county != None:
            queryset = queryset.filter(user_locations__county=County.objects.get(id=county))
        if is_continuous_time == 'True':
            queryset = queryset.filter(is_continuous_time=True)
        else:
            pass
        # queryset = queryset.filter(start_datetime__lte=datetime.date(int(start_datetime.split('-')[0]),int(start_datetime.split('-')[1]),int(start_datetime.split('-')[2])),end_datetime__gte=datetime.date(int(end_datetime.split('-')[0]),int(end_datetime.split('-')[1]),int(end_datetime.split('-')[2])))
        for i in range(len(weekdays.split(','))):
            queryset = queryset.filter(user_weekday__weekday=weekdays.split(',')[i])

        for i in range(len(queryset)):
            queryset[i].locations = UserServiceLocation.objects.filter(user=queryset[i])
            queryset[i].rate_num = 1
        return queryset

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        user.background_image_url = User.objects.get(phone=user).background_image
        user.services = UserServiceShip.objects.filter(user=user)
        user.licences = UserLicenseShipImage.objects.filter(user=user)
        user.about_me = User.objects.get(phone=user).about_me
        user.reviews = Review.objects.filter(servant=user)[:2]
        serializer = self.get_serializer(user, context={"request":request})
        return Response(serializer.data)