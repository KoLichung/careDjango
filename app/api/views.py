from tracemalloc import start
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q
from django.db.models import Avg , Count
from django.shortcuts import get_object_or_404
import datetime
from datetime import date ,timedelta
from modelCore.models import User, City, County,Service,UserWeekDayTime,UserServiceShip ,Language ,UserLanguage , License, UserLicenseShipImage
from modelCore.models import UserServiceLocation, Case, DiseaseCondition,BodyCondition,CaseDiseaseShip,CaseBodyConditionShip 
from modelCore.models import CaseServiceShip ,Order ,Review ,PayInfo ,Message ,SystemMessage , OrderWeekDay ,OrderIncreaseService
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
        
        #以下兩個情形只會有其中一個發生
        if is_continuous_time == 'True':
            queryset = queryset.filter(is_continuous_time=True)

        #所選擇的周間跟時段 要符合 servant 的服務時段
        if weekdays != None:
            weekdays_num_list = weekdays.split(',')
            service_time_condition_1 = Q(is_continuous_time=True)
            service_time_condition_2 = Q(user_weekday__weekday__in=weekdays_num_list, user_weekday__start_time__lte=start_time_int, user_weekday__end_time__gte=end_time_int)
            queryset = queryset.filter(service_time_condition_1 | service_time_condition_2).distinct()

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
        orders = Order.objects.filter(condition1 | condition2 | condition3)
        #2.再從 1 取出週間有交集的訂單
        #這邊考慮把 Order 的 weekday 再寫成一個 model OrderWeekDay, 然後再去比較, 像 user__weekday 一樣
        if weekdays != None:
            weekdays_num_list = weekdays.split(',')
            orders = orders.filter(order_weekday__weekday__in=weekdays_num_list).distinct()
        #3.再從 2 取出時段有交集的訂單
        time_condition_1 = Q(start_time__range=[start_time_int, end_time_int])
        time_condition_2 = Q(end_time__range=[start_time_int, end_time_int])
        time_condition3 = Q(start_time__lte=start_time_int)&Q(end_time__gte=end_time_int)
        orders = orders.filter(time_condition_1 | time_condition_2 | time_condition3)
        order_conflict_servants_id = list(orders.values_list('user', flat=True))
        queryset = queryset.filter(~Q(id__in=order_conflict_servants_id))

        for i in range(len(queryset)):
            queryset[i].locations = UserServiceLocation.objects.filter(user=queryset[i])
            queryset[i].avg_rate = Review.objects.filter(servant=queryset[i],servant_rating__gte=1).aggregate(Avg('servant_rating'))['servant_rating__avg']
        return queryset

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        user.background_image_url = User.objects.get(phone=user).background_image

        service_ids = list(UserServiceShip.objects.filter(user=user).values_list('service', flat=True))
        user.services = Service.objects.filter(id__in=service_ids)

        license_ids = list(UserLicenseShipImage.objects.filter(user=user).values_list('license', flat=True))
        user.licences = License.objects.filter(id__in=license_ids)
        user.avg_rate = Review.objects.filter(servant=user,servant_rating__gte=1).aggregate(Avg('servant_rating'))['servant_rating__avg']
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
            queryset[i].avg_rate = Review.objects.filter(servant=queryset[i],servant_rating__gte=1).aggregate(Avg('servant_rating'))['servant_rating__avg']
            queryset[i].rate_num = Review.objects.filter(servant=queryset[i],servant_rating__gte=1).aggregate(rate_num=Count('servant_rating'))['rate_num']

        return queryset

class CaseSearchViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,):
    queryset = Case.objects.all()
    serializer_class = serializers.CaseSerializer

    def get_queryset(self):
        city = self.request.query_params.get('city')
        county = self.request.query_params.get('county')
        #2022-07-10T00:00:00Z
        start_datetime = self.request.query_params.get('start_datetime')
        end_datetime = self.request.query_params.get('end_datetime')
        care_type= self.request.query_params.get('care_type')
        queryset = self.queryset.filter(is_taken=False)

        if city != None:
            queryset = queryset.filter(city=City.objects.get(id=city))
        if county != None:
            queryset = queryset.filter(county=County.objects.get(id=county))
        if start_datetime != None and end_datetime != None :
            queryset = queryset.filter(start_datetime__gte=start_datetime,end_datetime__lte=end_datetime)
        if care_type == 'home':
            queryset = queryset.filter(care_type='home')
        elif care_type == 'hospital':
            queryset = queryset.filter(care_type='hospital')

        return queryset

    def retrieve(self, request, *args, **kwargs):
        case = self.get_object()
        case.rate_num = Review.objects.filter(order__case=case,servant_rating__gte=1).aggregate(rate_num=Count('servant_rating'))['rate_num']
        case.rated_num = Review.objects.filter(order__case=case,servant_rating__gte=1).aggregate(rated_num=Avg('servant_rating'))['rated_num']
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

class ServantCaseViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,):

    queryset = Case.objects.all()
    serializer_class = serializers.CaseSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        servant = self.request.user
        queryset = self.queryset.filter(servant=servant)

        for i in range(len(queryset)):
            if Review.objects.get(case=queryset[i]).servant_rating != None:
                queryset[i].servant_rating = Review.objects.get(case=queryset[i]).servant_rating
        return queryset

    def retrieve(self, request, *args, **kwargs):
        case = self.get_object()
        servant = self.request.user
        if case.servant == servant:
            case.review = Review.objects.get(case=case)
            if case.care_type == 'home':
                case.hour_wage = case.servant.home_hour_wage
            elif case.care_type == 'hospital':
                case.hour_wage = case.servant.hospital_hour_wage
            
            case.servant_rating = Review.objects.get(case=case).servant_rating
            case.servant_rating = Review.objects.get(case=case).servant_rating
            disease_ids = list(CaseDiseaseShip.objects.filter(case=case).values_list('disease', flat=True))
            case.disease = DiseaseCondition.objects.filter(id__in=disease_ids)
            body_condition_ids = list(CaseBodyConditionShip.objects.filter(case=case).values_list('body_condition', flat=True))
            case.body_condition = BodyCondition.objects.filter(id__in=body_condition_ids)

            service_ids = list(CaseServiceShip.objects.filter(case=case).values_list('service', flat=True)) 
            case.services  = Service.objects.filter(id__in=service_ids)

            # 以下做 order 相關欄位
            order = Order.objects.get(case=case)
            case.work_hours = order.work_hours
            case.base_money = order.base_money
            case.platform_percent = order.platform_percent
            # !!!
            case.platform_money = order.platform_money
            case.total_money = order.total_money
            increase_service_ids = list(CaseServiceShip.objects.filter(case=case,service__is_increase_price=True).values_list('service', flat=True))
            case.increase_money = OrderIncreaseService.objects.filter(order=order,service__id__in=increase_service_ids)

            serializer = self.get_serializer(case)
            return Response(serializer.data)
        else:
            return Response({'message': "have no authority"})

class NeedCaseViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,):
    queryset = Case.objects.all()
    serializer_class = serializers.CaseSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(user=user)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        case = self.get_object()
        user = self.request.user
        if case.user == user:  
            if case.care_type == 'home':
                case.hour_wage = case.servant.home_hour_wage
            elif case.care_type == 'hospital':
                case.hour_wage = case.servant.hospital_hour_wage
            
            case.servant_rating = Review.objects.get(case=case).servant_rating
            case.servant_rating = Review.objects.get(case=case).servant_rating
            disease_ids = list(CaseDiseaseShip.objects.filter(case=case).values_list('disease', flat=True))
            case.disease = DiseaseCondition.objects.filter(id__in=disease_ids)
            body_condition_ids = list(CaseBodyConditionShip.objects.filter(case=case).values_list('body_condition', flat=True))
            case.body_condition = BodyCondition.objects.filter(id__in=body_condition_ids)

            service_ids = list(CaseServiceShip.objects.filter(case=case).values_list('service', flat=True)) 
            case.services  = Service.objects.filter(id__in=service_ids)

            # 以下做 order 相關欄位
            order = Order.objects.get(case=case)
            case.work_hours = order.work_hours
            case.base_money = order.base_money
            case.platform_percent = order.platform_percent
            # !!!!!!
            case.platform_money = order.platform_money
            case.total_money = order.total_money
            increase_service_ids = list(CaseServiceShip.objects.filter(case=case,service__is_increase_price=True).values_list('service', flat=True))
            case.increase_money = OrderIncreaseService.objects.filter(order=order,service__id__in=increase_service_ids)

            serializer = self.get_serializer(case)
            return Response(serializer.data)
        else:
            print('no auth')
            return Response({'message': "have no authority"})

class ReviewViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(case__user=user)
        
        #review_type=unrated, given, received
        review_type = self.request.query_params.get('review_type')

        if review_type == 'unrated':
            queryset = queryset.filter(servant_rating__lt=1)
        elif review_type == 'given':
            queryset = queryset.filter(servant_rating__gte=1)
        elif review_type == 'received':
            queryset = queryset.filter(case_offender_rating__gte=1)  

        for i in range(len(queryset)):
            queryset[i].care_type = queryset[i].case.care_type
            queryset[i].is_continuous_time = queryset[i].case.is_continuous_time
            queryset[i].start_datetime = queryset[i].case.start_datetime
            queryset[i].end_datetime = queryset[i].case.end_datetime
            queryset[i].user_avg_rate = queryset.filter(case_offender_rating__gte=1).aggregate(Avg('case_offender_rating'))['case_offender_rating__avg']
            queryset[i].user_rated_num = queryset.filter(case_offender_rating__gte=1).aggregate(Count('case_offender_rating'))['case_offender_rating__count']
        return queryset

    def retrieve(self, request, *args, **kwargs):
        review = self.get_object()
        user = self.request.user
        if review.case.user == user:
            review.care_type = review.case.care_type
            review.is_continuous_time = review.case.is_continuous_time
            review.start_datetime = review.case.start_datetime
            review.end_datetime = review.case.end_datetime
            serializer = self.get_serializer(review)
            return Response(serializer.data)
        else:
            return Response({'message': "have no authority"})
    
    def update(self, request, *args, **kwargs):
        review = self.get_object()
        user = self.request.user
        servant_rating = request.data.get('servant_rating')
        servant_comment = request.data.get('servant_comment')
        if review.case.user == user:
            review.servant_rating = servant_rating
            review.servant_comment = servant_comment
            review.save()
            serializer = self.get_serializer(review)
            return Response(serializer.data)
        else:
            return Response({'message': "have no authority"})
        
class ServantPutReviewView(APIView):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
            
    def put(self, request, pk):
        review = get_object_or_404(Review.objects.all(),pk=pk)
        servant = self.request.user
        if review.servant == servant:
            case_offender_rating = request.data.get('case_offender_rating')
            case_offender_comment = request.data.get('case_offender_comment')
            review.case_offender_rating = case_offender_rating
            review.case_offender_comment = case_offender_comment
            review.save()
            serializer = serializers.ReviewSerializer(review)
            return Response(serializer.data)
        else:
            return Response({'message': "have no authority"})
