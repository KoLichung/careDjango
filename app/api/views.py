from tracemalloc import start
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q
from django.db.models import Avg , Count ,Sum
from django.shortcuts import get_object_or_404
import datetime
import operator
from functools import reduce
from datetime import date ,timedelta
from modelCore.models import User, City, County,Service,UserWeekDayTime,UserServiceShip ,Language ,UserLanguage , License, UserLicenseShipImage
from modelCore.models import UserServiceLocation, Case, DiseaseCondition,BodyCondition,CaseDiseaseShip,CaseBodyConditionShip ,ChatRoom ,ChatroomUserShip
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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(case__user=user)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        order = self.get_object()
        user = self.request.user
        if order.case.user == user:
            order.related_case = order.case
            order.servants = order.case.servant
            order.related_case.rating_nums= Review.objects.filter(servant=order.case.servant,servant_rating__gte=1).aggregate(rating_nums=Count('servant_rating'))['rating_nums']
            order.related_case.servant_rating = Review.objects.filter(servant=order.case.servant,servant_rating__gte=1).aggregate(servant_rating =Avg('servant_rating'))['servant_rating']
            disease_ids = list(CaseDiseaseShip.objects.filter(case=order.case).values_list('disease', flat=True))
            order.related_case.disease = DiseaseCondition.objects.filter(id__in=disease_ids)
            body_condition_ids = list(CaseBodyConditionShip.objects.filter(case=order.case).values_list('body_condition', flat=True))
            order.related_case.body_condition = BodyCondition.objects.filter(id__in=body_condition_ids)
            serializer = self.get_serializer(order)
            return Response(serializer.data)
        else:
            return Response({'message': "have no authority"})

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

class ChatRoomViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    queryset = ChatRoom.objects.all()
    serializer_class = serializers.ChatRoomSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        chatroom_ids = list(ChatroomUserShip.objects.filter(user=user).values_list('chatroom', flat=True))
        queryset = self.queryset.filter(id__in=chatroom_ids).order_by('-update_at')
        return queryset

    def create(self, request, *args, **kwargs):
        user = self.request.user
        users = request.data.get('users')
        users_list = [int(i) for i in users.split(',')]
        if user.id in users_list:
            chatroom = ChatRoom()
            chatroom.save()
            for user_id in users_list:
                chatroomusership = ChatroomUserShip()
                chatroomusership.user = User.objects.get(id=user_id)
                chatroomusership.chatroom = chatroom
                chatroomusership.save()
            return Response({'message': "Successfully create"})
        else:
            return Response({'message': "have no authority"})

class MessageViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        chatroom= self.request.query_params.get('chatroom')
        user_ids = list(ChatroomUserShip.objects.filter(chatroom=chatroom).values_list('user', flat=True))
        if user.id in user_ids:
            queryset = self.queryset.filter(chatroom=chatroom).order_by('-id')

            for i in range(len(queryset)):
                if queryset[i].user == user:
                    queryset[i].message_is_mine = True
                if queryset[i].case != None:
                    queryset[i].orders = Order.objects.filter(case=queryset[i].case)
            return queryset
        return Response({'message': "have no authority"})

    def create(self, request, *args, **kwargs):
        user = self.request.user
        chatroom_id = self.request.query_params.get('chatroom')
        chatroom = ChatRoom.objects.get(id=chatroom_id)
        user_ids = list(ChatroomUserShip.objects.filter(chatroom=chatroom).values_list('user', flat=True))
        case = request.data.get('case')
        content = request.data.get('content')
        if user.id in user_ids:
            message = Message()
            message.chatroom = chatroom
            message.user = user
            if case != None:
                message.case = Case.objects.get(id=case)
                message.order = Order.objects.filter(case=message.case).order_by('-created_at')[0]
                message.is_this_message_only_case = True
            else:
                message.content = content
            message.save()
            chatroom.update_at = datetime.datetime.now()
            chatroom.save()
            serializer = self.get_serializer(message)
            return Response(serializer.data)
        else:
            return Response({'message': "have no authority"})

class SystemMessageViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = SystemMessage.objects.all()
    serializer_class = serializers.SystemMessageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(user=user).order_by('-id')
        return queryset

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
        order = self.request.query_params.get('order')

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
            start_date = start_datetime.split('T')[0]
            end_date = end_datetime.split('T')[0]
            start_time_int = int(start_end_time.split(':')[0])
            end_time_int = int(start_end_time.split(':')[1])
            weekdays_num_list = weekdays.split(',')
            service_time_condition_1 = Q(is_continuous_time=True)
            # service_time_condition_2 = Q(user_weekday__weekday__in=weekdays_num_list, user_weekday__start_time__lte=start_time_int, user_weekday__end_time__gte=end_time_int)
            # queryset = queryset.filter(service_time_condition_1 | service_time_condition_2).distinct()
            for weekdays_num in weekdays_num_list:
                service_time_condition_2 = Q(user_weekday__weekday=weekdays_num, user_weekday__start_time__lte=start_time_int, user_weekday__end_time__gte=end_time_int)
                queryset = queryset.filter(service_time_condition_1 | service_time_condition_2).distinct()
        # 如果一個 servant 已經在某個時段已經有了 1 個 order, 就沒辦法再接另一個 order
        # 2022-07-10

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
        order_conflict_servants_id = list(orders.values_list('servant', flat=True))
        queryset = queryset.filter(~Q(id__in=order_conflict_servants_id))

        if order == 'rating':
            queryset = queryset.order_by('-rating')
        elif order == 'rating_nums':
            queryset = queryset.filter(servant_reviews__servant_rating__gte=1).annotate(rating_nums=Count('servant_reviews__servant_rating')).order_by('-rating_nums')
        elif order == 'price_low':
            if care_type == 'home':
                queryset = queryset.order_by('home_hour_wage')
                print('low')
            else:
                queryset = queryset.order_by('hospital_hour_wage')
        elif order == 'price_high':
            if care_type == 'home':
                queryset = queryset.order_by('-home_hour_wage')
            else:
                queryset = queryset.order_by('-hospital_hour_wage')
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
            queryset[i].rating_nums = Review.objects.filter(servant=queryset[i],servant_rating__gte=1).aggregate(rating_nums=Count('servant_rating'))['rating_nums']

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
        case.num_offender_rating = Review.objects.filter(order__case=case,case_offender_rating__gte=1).aggregate(num_offender_rating=Count('case_offender_rating'))['num_offender_rating']
        case.avg_offender_rating  = Review.objects.filter(order__case=case,case_offender_rating__gte=1).aggregate(case_offender_rating =Avg('case_offender_rating'))['case_offender_rating']
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
            case.servant_name = case.servant.name
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
            queryset[i].user_rating_nums = queryset.filter(case_offender_rating__gte=1).aggregate(Count('case_offender_rating'))['case_offender_rating__count']
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


class CreateCase(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Case.objects.all()
    serializer_class = serializers.CaseSerializer

    def post(self, request, format=None):
        user = self.request.user
        county = self.request.query_params.get('county')
        city = County.objects.get(id=county).city
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        weekday = self.request.query_params.get('weekday')
        start_time = self.request.query_params.get('start_time')
        start_time = start_time.split(':')
        end_time = self.request.query_params.get('end_time')
        end_time = end_time.split(':')

        care_type = request.data.get('care_type')
        is_continuous_time = request.data.get('is_continuous_time')
        name = request.data.get('name')
        gender = request.data.get('gender')
        age = request.data.get('age')
        weight = request.data.get('weight')
        disease = request.data.get('disease')
        disease_remark = request.data.get('disease_remark')
        body_condition = request.data.get('body_condition')
        conditions_remark = request.data.get('conditions_remark')
        service = request.data.get('service')
        emergencycontact_name = request.data.get('emergencycontact_name')
        emergencycontact_relation = request.data.get('emergencycontact_relation')
        emergencycontact_phone = request.data.get('emergencycontact_phone')

        #searvant_ids=1,4,7
        servant_ids = request.data.get('servant_ids')

        case = Case()
        case.user = user
        case.city = city
        case.county = County.objects.get(id=county)

        #start_datetime=2022-07-21
        #s = "2014-04-07"
        #datetime.datetime.strptime(s, "%Y-%m-%d").date()
        case.start_datetime = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        case.end_datetime = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        
        case.weekday = weekday
        case.start_time = int(start_time[0]) + float(int(start_time[1])/60)
        case.end_time = int(end_time[0]) + float(int(end_time[1])/60)
        if name != None:
            case.name = name
        if care_type != None:
            case.care_type = care_type
        if is_continuous_time == "True":
            case.is_continuous_time = True
        else:
            case.is_continuous_time = False
        if gender != None:
            case.gender = gender
        if age != None:
            case.age = age
        if weight != None:
            case.weight = weight
        if disease_remark != None:
            case.disease_remark = disease_remark
        if conditions_remark != None:
            case.conditions_remark = conditions_remark
        if emergencycontact_name != None:
            case.emergencycontact_name = emergencycontact_name
        if emergencycontact_relation != None:
            case.emergencycontact_relation = emergencycontact_relation
        if emergencycontact_phone != None:
            case.emergencycontact_phone = emergencycontact_phone
        case.save()

        if disease != None:
            disease_ids = disease.split(',')
            for disease_id in disease_ids:
                casediseaseship = CaseDiseaseShip()
                casediseaseship.disease = DiseaseCondition.objects.get(id=disease_id)
                casediseaseship.case = case
                casediseaseship.save()

        if body_condition != None:
            body_condition_ids = body_condition.split(',')
            for body_condition_id in body_condition_ids:
                casebodyconditionship = CaseBodyConditionShip()
                casebodyconditionship.body_condition = BodyCondition.objects.get(id=body_condition_id)
                casebodyconditionship.case = case
                casebodyconditionship.save()

        if service != None:
            service_ids = service.split(',')
            for service_id in service_ids:
                caseserviceship = CaseServiceShip()
                caseserviceship.service = Service.objects.get(id=service_id)
                caseserviceship.case = case
                caseserviceship.save()

        disease_idList = list(CaseDiseaseShip.objects.filter(case=case).values_list('disease', flat=True))
        case.disease = DiseaseCondition.objects.filter(id__in=disease_idList)
        body_condition_idList = list(CaseBodyConditionShip.objects.filter(case=case).values_list('body_condition', flat=True))
        case.body_condition = BodyCondition.objects.filter(id__in=body_condition_idList)
        service_idList = list(CaseServiceShip.objects.filter(case=case).values_list('service', flat=True))
        case.services = Service.objects.filter(id__in=service_idList)

        serializer = self.serializer_class(case)
        return Response(serializer.data)

# class ChooseServantViewSet(viewsets.GenericViewSet,
#                     mixins.UpdateModelMixin,
#                     mixins.RetrieveModelMixin,):

#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     queryset = User.objects.all()
#     serializer_class = serializers.CaseSerializer

#     #GET, POST
#     #GET 把 filter 參數傳入, 類似首頁的寫法, Order by rating
#     def retrieve(self, request, *args, **kwargs):
#         case = self.get_object()
#         user = self.request.user
#         case.user_detail = user
#         queryset = User.objects.filter(is_servant=True)
#         if case.care_type == 'home':
#             queryset = queryset.filter(is_home=True)
#         if case.care_type == 'hospital':
#             queryset = queryset.filter(is_hospital=True)
#         #以下兩個情形只會有其中一個發生
#         # start_datetime = case.start_datetime
#         # end_datetime = case.end_datetime
#         if case.is_continuous_time == 'True':
#             queryset = queryset.filter(is_continuous_time=True)

#         #所選擇的周間跟時段 要符合 servant 的服務時段
#         if case.weekday != None:
#             start_date = str(case.start_datetime).split('T')[0]
#             end_date = str(case.end_datetime).split('T')[0]
#             start_time_int = case.start_time
#             end_time_int = case.end_time
#             weekdays_num_list = case.weekday.split(',')
#             service_time_condition_1 = Q(is_continuous_time=True)
#             for weekdays_num in weekdays_num_list:
#                 service_time_condition_2 = Q(user_weekday__weekday=weekdays_num, user_weekday__start_time__lte=start_time_int, user_weekday__end_time__gte=end_time_int)
#                 queryset = queryset.filter(service_time_condition_1 | service_time_condition_2).distinct()

#         # 如果一個 servant 已經在某個時段已經有了 1 個 order, 就沒辦法再接另一個 order
#         # 2022-07-10
       

#         #所選擇的日期期間/週間/時段, 要在已有的訂單時段之外, 先找出時段內的訂單, 然後找出時段內的人, 最後反過來, 非時段內的人就是可以被篩選
#         #1.取出日期期間有交集的訂單
#         condition1 = Q(start_datetime__range=[start_date, end_date])
#         condition2 = Q(end_datetime__range=[start_date, end_date])
#         condition3 = Q(start_datetime__lte=start_date)&Q(end_datetime__gte=end_date)
#         orders = Order.objects.filter(condition1 | condition2 | condition3)
#         #2.再從 1 取出週間有交集的訂單
#         #這邊考慮把 Order 的 weekday 再寫成一個 model OrderWeekDay, 然後再去比較, 像 user__weekday 一樣
#         if case.weekday != None:
#             weekdays_num_list = case.weekday.split(',')
#             orders = orders.filter(order_weekday__weekday__in=weekdays_num_list).distinct()
#         #3.再從 2 取出時段有交集的訂單
#         print(start_time_int,end_time_int)
#         time_condition_1 = Q(start_time__range=[start_time_int, end_time_int])
#         time_condition_2 = Q(end_time__range=[start_time_int, end_time_int])
#         time_condition3 = Q(start_time__lte=start_time_int)&Q(end_time__gte=end_time_int)
#         orders = orders.filter(time_condition_1 | time_condition_2 | time_condition3)
#         order_conflict_servants_id = list(orders.values_list('servant', flat=True))
#         print(order_conflict_servants_id)
#         queryset = queryset.filter(~Q(id__in=order_conflict_servants_id))
#         queryset = queryset.filter(user_locations__county=case.county)
#         case.servant_candidate = queryset
#         serializer = self.serializer_class(case)
#         return Response(serializer.data)

#     def update(self, request, *args, **kwargs):
#         case = self.get_object()
#         servant = request.data.get('servant')
#         if servant != None:
#             case.servant = User.objects.get(id=servant)
#         else:
#             case.delete()
#         serializer = self.serializer_class(case)
#         return Response(serializer.data)

class CreateServantOrder(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def post(self, request, format=None):
        user = self.request.user
        servant_id = self.request.query_params.get('servant_id')
        servant = User.objects.get(id=servant_id)
        county = self.request.query_params.get('county')
        city = County.objects.get(id=county).city
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        weekday = self.request.query_params.get('weekday')
        start_time = self.request.query_params.get('start_time')
        start_time = start_time.split(':')
        end_time = self.request.query_params.get('end_time')
        end_time = end_time.split(':')

        care_type = request.data.get('care_type')
        is_continuous_time = request.data.get('is_continuous_time')
        name = request.data.get('name')
        gender = request.data.get('gender')
        age = request.data.get('age')
        weight = request.data.get('weight')
        disease = request.data.get('disease')
        disease_remark = request.data.get('disease_remark')
        body_condition = request.data.get('body_condition')
        conditions_remark = request.data.get('conditions_remark')
        service = request.data.get('service')
        emergencycontact_name = request.data.get('emergencycontact_name')
        emergencycontact_relation = request.data.get('emergencycontact_relation')
        emergencycontact_phone = request.data.get('emergencycontact_phone')
        is_open_for_search = request.data.get('is_open_for_search')

        case = Case()
        case.user = user
        case.servant = servant
        case.city = city
        case.county = County.objects.get(id=county)

        #start_datetime=2022-07-21
        #s = "2014-04-07"
        #datetime.datetime.strptime(s, "%Y-%m-%d").date()
        case.start_datetime = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        case.end_datetime = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        
        case.weekday = weekday
        case.start_time = int(start_time[0]) + float(int(start_time[1])/60)
        case.end_time = int(end_time[0]) + float(int(end_time[1])/60)
        if name != None:
            case.name = name
        if care_type != None:
            case.care_type = care_type
        if is_continuous_time == "True":
            case.is_continuous_time = True
        else:
            case.is_continuous_time = False
        if gender != None:
            case.gender = gender
        if age != None:
            case.age = age
        if weight != None:
            case.weight = weight
        if disease_remark != None:
            case.disease_remark = disease_remark
        if conditions_remark != None:
            case.conditions_remark = conditions_remark
        if emergencycontact_name != None:
            case.emergencycontact_name = emergencycontact_name
        if emergencycontact_relation != None:
            case.emergencycontact_relation = emergencycontact_relation
        if emergencycontact_phone != None:
            case.emergencycontact_phone = emergencycontact_phone
        if is_open_for_search == "True":
            case.is_open_for_search = True
        else:
            case.is_open_for_search = False
        case.save()

        if disease != None:
            disease_ids = disease.split(',')
            for disease_id in disease_ids:
                casediseaseship = CaseDiseaseShip()
                casediseaseship.disease = DiseaseCondition.objects.get(id=disease_id)
                casediseaseship.case = case
                casediseaseship.save()

        if body_condition != None:
            body_condition_ids = body_condition.split(',')
            for body_condition_id in body_condition_ids:
                casebodyconditionship = CaseBodyConditionShip()
                casebodyconditionship.body_condition = BodyCondition.objects.get(id=body_condition_id)
                casebodyconditionship.case = case
                casebodyconditionship.save()

        if service != None:
            service_ids = service.split(',')
            for service_id in service_ids:
                caseserviceship = CaseServiceShip()
                caseserviceship.service = Service.objects.get(id=service_id)
                caseserviceship.case = case
                caseserviceship.save()

        disease_idList = list(CaseDiseaseShip.objects.filter(case=case).values_list('disease', flat=True))
        case.disease = DiseaseCondition.objects.filter(id__in=disease_idList)
        body_condition_idList = list(CaseBodyConditionShip.objects.filter(case=case).values_list('body_condition', flat=True))
        case.body_condition = BodyCondition.objects.filter(id__in=body_condition_idList)
        service_idList = list(CaseServiceShip.objects.filter(case=case).values_list('service', flat=True))
        case.services = Service.objects.filter(id__in=service_idList)

        order = Order()
        order.case = case
        order.user = case.user
        order.servant = case.servant
        order.state = 'unPaid'
        order.start_datetime = case.start_datetime
        order.end_datetime = case.end_datetime
        order.start_time = order.case.start_time
        order.end_time = order.case.end_time
        order.save()
        weekdays = order.case.weekday.split(',')
        for weekday in weekdays:
            orderWeekday = OrderWeekDay()
            orderWeekday.order = order
            orderWeekday.weekday = weekday
            orderWeekday.save()
        weekday_list = list(OrderWeekDay.objects.filter(order=order).values_list('weekday', flat=True))
        total_hours = 0
        for i in weekday_list:
            total_hours += (days_count([int(i)], order.start_datetime.date(), order.end_datetime.date())) * (order.end_time - order.start_time)
        order.work_hours = total_hours
        if order.case.care_type == 'home':
            order.base_money = order.work_hours * order.case.servant.home_hour_wage
        elif order.case.care_type == 'hospital':
            order.base_money = order.work_hours * order.case.servant.hospital_hour_wage

        # need to change in the future
        order.platform_percent = 15
        order.save()
        Review.objects.create(order=order,case=order.case,servant=order.case.servant)

        for service_id in service_idList:
            if int(service_id) <= 4:
                orderIncreaseService = OrderIncreaseService()
                orderIncreaseService.order = order
                orderIncreaseService.service = Service.objects.get(id=service_id)
                orderIncreaseService.increase_percent = UserServiceShip.objects.get(user=servant,service=Service.objects.get(id=service_id)).increase_percent
                orderIncreaseService.increase_money = (order.base_money) * (orderIncreaseService.increase_percent)/100
                orderIncreaseService.save()

        order.total_money = ((order.base_money) + (OrderIncreaseService.objects.filter(order=order,service__is_increase_price=True).aggregate(Sum('increase_money'))['increase_money__sum'])) * ((100 - order.platform_percent)/100)
        order.platform_money = order.total_money * (order.platform_percent/100)
        order.save()
        order.related_case = case
        # for weekday in 
        serializer = self.serializer_class(order)
        return Response(serializer.data)

def days_count(weekdays: list, start: date, end: date):
    dates_diff = end-start
    days = [start + timedelta(days=i) for i in range(dates_diff.days)]
    return len([day for day in days if day.weekday() in weekdays])