from tracemalloc import start
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from collections import namedtuple
from django.db.models import Q
from django.db.models import Avg , Count
from datetime import datetime
from modelCore.models import User, City, County,Service,UserWeekDayTime,UserServiceShip ,Language ,UserLanguage , License, UserLicenseShipImage
from modelCore.models import UserServiceLocation, Case, DiseaseCondition,BodyCondition,CaseDiseaseShip,CaseBodyConditionShip 
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

class CaseSearchViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin):
    queryset = Case.objects.all()
    serializer_class = serializers.CaseSerializer

    def get_queryset(self):

        city = self.request.query_params.get('city')
        county = self.request.query_params.get('county')
        #2022-07-10T00:00:00Z
        start_datetime = self.request.query_params.get('start_datetime')
        end_datetime = self.request.query_params.get('end_datetime')
        care_type= self.request.query_params.get('care_type')
        queryset = self.queryset

        if city != None:
            queryset = queryset.filter(city=City.objects.get(id=city))
        if county != None:
            queryset = queryset.filter(county=County.objects.get(id=county))
        if (start_datetime != None)&(end_datetime != None) == True:
            queryset = queryset.filter(start_datetime__gte=start_datetime,end_datetime__lte=end_datetime)
        if care_type == 'home':
            queryset = queryset.filter(care_type='home')
        elif care_type == 'hospital':
            queryset = queryset.filter(care_type='hospital')

        return queryset

    def retrieve(self, request, *args, **kwargs):
        case = self.get_object()
        case.reviews_num = Review.objects.filter(order__case=case).aggregate(reviews_num=Count('servant_rating'))['reviews_num']
        case.rated_num = Review.objects.filter(order__case=case).aggregate(rated_num=Avg('servant_rating'))['rated_num']
        if case.is_taken == True:
            case.status = '案件已關閉'
        else:
            case.status = '尚未找到服務者'
        
        disease_ids = list(CaseDiseaseShip.objects.filter(case=case).values_list('disease', flat=True))
        case.disease = DiseaseCondition.objects.filter(id__in=disease_ids)
        body_condition_ids = list(CaseBodyConditionShip.objects.filter(case=case).values_list('body_condition', flat=True))
        case.body_condition = BodyCondition.objects.filter(id__in=body_condition_ids)
        service_ids = list(CaseServiceShip.objects.filter(case=case).values_list('service', flat=True))
        case.services = Service.objects.filter(id__in=service_ids)

        serializer = self.get_serializer(case)
        return Response(serializer.data)

        
        

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
        start_date = start_datetime.split('T')[0]
        end_date = end_datetime.split('T')[0]
        start_time_int = int(start_end_time.split(':')[0])
        end_time_int = int(start_end_time.split(':')[1])

        #所選擇的日期期間/週間/時段, 要在已有的訂單時段之外, 先找出時段內的訂單, 然後找出時段內的人, 最後反過來, 非時段內的人就是可以被篩選
        #1.取出日期期間有交集的訂單
        condition1 = Q(start_datetime__range=[start_date, end_date])
        condition2 = Q(end_datetime__range=[start_date, end_date])
        condition3 = Q(start_datetime__lte=start_date)&Q(end_datetime__gte=end_date)
        orders = Order.objects.filter( condition1 | condition2 | condition3)
        #2.再從 1 取出週間有交集的訂單
        #這邊考慮把 Order 的 weekday 再寫成一個 model OrderWeekDay, 然後再去比較, 像 user__weekday 一樣

        #3.再從 2 取出時段有交集的訂單

        #所選擇的周間跟時段 要符合 servant 的服務時段
        if weekdays != None:
            weekdays_num_list = weekdays.split(',')
            queryset = queryset.filter(user_weekday__weekday__in=weekdays_num_list, user_weekday__start_time__lte=start_time_int, user_weekday__end_time__gte=end_time_int).distinct()

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

class RecommendServantViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,):
    
    queryset = User.objects.all()
    serializer_class = serializers.ServantSerializer

    def get_queryset(self):

        care_type= self.request.query_params.get('care_type')
        city = self.request.query_params.get('city')
        county = self.request.query_params.get('county')

        queryset = User.objects.filter(is_servant=True)
        if care_type == 'home':
            queryset = queryset.filter(is_home=True)
        elif care_type == 'hospital':
            queryset = queryset.filter(is_hospital=True)

        if city != None:
            queryset = queryset.filter(user_locations__city=City.objects.get(id=city))
        if county != None:
            queryset = queryset.filter(user_locations__county=County.objects.get(id=county))
        for i in range(len(queryset)):
            queryset[i].rate_num = Review.objects.filter(servant=queryset[i]).aggregate(Avg('servant_rating'))['servant_rating__avg']
            queryset[i].reviews_num = Review.objects.filter(servant=queryset[i]).aggregate(reviews_num=Count('servant_rating'))['reviews_num']

        return queryset