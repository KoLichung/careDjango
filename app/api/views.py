from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from collections import namedtuple
from django.db.models import Q
from django.db.models import Avg
from datetime import datetime
from modelCore.models import User, City, County,Service,UserWeekDayTime,UserServiceShip ,Language ,UserLanguage , License, UserLicenseShipImage
from modelCore.models import UserServiceLocation, Case, DiseaseCondition,BodyCondition,CaseDiseaseShip,CaseBodyConditionShip ,OrderWorkDate 
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
        #8:22
        start_end_time = self.request.query_params.get('start_end_time')
        

        queryset = User.objects.filter(is_servant=True)
        if care_type == 'home':
            queryset = queryset.filter(is_home=True)
        elif care_type == 'hospital':
            queryset = queryset.filter(is_hospital=True)

        if city != None:
            queryset = queryset.filter(user_locations__city=City.objects.get(id=city))
        if county != None:
            queryset = queryset.filter(user_locations__county=County.objects.get(id=county))
        if is_continuous_time == 'True':
            queryset = queryset.filter(is_continuous_time=True)

        # 如果一個 servant 已經在某個時段已經有了 1 個 order, 就沒辦法再接另一個 order
        # 2022-07-10
        if weekdays != None:
            weekdays_num_list = weekdays.split(',')
            start_date = start_datetime.split('T')[0]
            end_date = end_datetime.split('T')[0]
            start_time_int = int(start_end_time.split(':')[0])
            end_time_int = int(start_end_time.split(':')[1])
            queryset = queryset.filter((~Q(servant_workdays__workdate__range=[start_date, end_date],servant_workdays__weekday__in=weekdays_num_list,servant_workdays__start_time__lte=start_time_int,servant_workdays__end_time__gte=start_time_int))&(~Q(servant_workdays__workdate__range=[start_date, end_date],servant_workdays__weekday__in=weekdays_num_list,servant_workdays__start_time__lte=end_time_int,servant_workdays__end_time__gte=end_time_int)))
            for day_num in weekdays_num_list:
                queryset = queryset.filter(user_weekday__weekday=day_num, user_weekday__start_time__lte=start_time_int, user_weekday__end_time__gte=end_time_int)

        for i in range(len(queryset)):
            queryset[i].locations = UserServiceLocation.objects.filter(user=queryset[i])
            queryset[i].rate_num = Review.objects.filter(servant=queryset[i]).aggregate(Avg('servant_rating'))['servant_rating__avg']
        return queryset

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        user.background_image_url = User.objects.get(phone=user).background_image

        service_ids = list(UserServiceShip.objects.filter(user=user).values_list('service', flat=True))
        user.services = Service.objects.filter(id__in=service_ids)

        license_ids = list(UserLicenseShipImage.objects.filter(user=user).values_list('license', flat=True))
        user.licences = License.objects.filter(id__in=license_ids)
        user.rate_num = Review.objects.filter(servant=user).aggregate(Avg('servant_rating'))['servant_rating__avg']
        user.about_me = User.objects.get(phone=user).about_me
        user.reviews = Review.objects.filter(servant=user)[:2]
        serializer = self.get_serializer(user, context={"request":request})
        return Response(serializer.data)