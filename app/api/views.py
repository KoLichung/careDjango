from tracemalloc import start
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response    
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q
from django.db.models import Avg , Count ,Sum
from django.shortcuts import get_object_or_404
import datetime
import pytz
from functools import reduce
from datetime import date ,timedelta
from modelCore.models import User, City, County,Service,UserWeekDayTime,UserServiceShip ,Language ,UserLanguage , License, UserLicenseShipImage
from modelCore.models import UserServiceLocation, Case, DiseaseCondition,BodyCondition,CaseDiseaseShip,CaseBodyConditionShip ,ChatRoom ,ChatroomUserShip
from modelCore.models import CaseServiceShip ,Order ,Review ,PayInfo ,ChatroomMessage ,SystemMessage , OrderWeekDay ,OrderIncreaseService
from modelCore.models import BlogPost, BlogPostCategoryShip, BlogCategory
from api import serializers
from messageApp.tasks import *
from app.pagination import LargeResultsSetPagination

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
        queryset = self.queryset
        is_mine = self.request.query_params.get('is_mine')
        if is_mine == 'true' or is_mine == 'True':
            queryset = self.queryset.filter(case__user=user)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        order = self.get_object()
        user = self.request.user

        order.related_case = order.case
        order.related_case.user_detail = order.case.user

        service_ids = list(CaseServiceShip.objects.filter(case=order.related_case).values_list('service', flat=True))
        order.related_case.services = Service.objects.filter(id__in=service_ids)

        # order.servant = order.case.servant
        # order.servant.rating_nums = Review.objects.filter(servant=order.servant,servant_rating__gte=1).aggregate(rating_nums=Count('servant_rating'))['rating_nums']

        order.increase_services = order.order_increase_services

        order.related_case.rating_nums= Review.objects.filter(servant=order.case.servant,servant_rating__gte=1).aggregate(rating_nums=Count('servant_rating'))['rating_nums']
        order.related_case.servant_rating = Review.objects.filter(servant=order.case.servant,servant_rating__gte=1).aggregate(servant_rating =Avg('servant_rating'))['servant_rating']
        disease_ids = list(CaseDiseaseShip.objects.filter(case=order.case).values_list('disease', flat=True))
        order.related_case.disease = DiseaseCondition.objects.filter(id__in=disease_ids)
        body_condition_ids = list(CaseBodyConditionShip.objects.filter(case=order.case).values_list('body_condition', flat=True))
        order.related_case.body_condition = BodyCondition.objects.filter(id__in=body_condition_ids)
        serializer = self.get_serializer(order)
        return Response(serializer.data)


class UserServiceLocationViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin):
    queryset = UserServiceLocation.objects.all()
    serializer_class = serializers.UserServiceLocationSerializer

    def get_queryset(self):
        queryset = self.queryset

        user_id = self.request.query_params.get('user_id')
        user = User.objects.get(id=user_id)
        queryset = queryset.filter(user=user)
        return queryset

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

        for i in range(len(queryset)):
            try:
                other_side_user = ChatroomUserShip.objects.filter(chatroom=queryset[i]).filter(~Q(user=self.request.user)).first().user
                queryset[i].other_side_image_url = other_side_user.image
                queryset[i].other_side_name = other_side_user.name
                # print(other_side_user.name)
                # print(ChatroomMessage.objects.all())
            
                if ChatroomMessage.objects.filter(chatroom=queryset[i]).count()!=0:
                    last_message = ChatroomMessage.objects.filter(chatroom=queryset[i]).order_by('-id').first()
                    if last_message.is_this_message_only_case:
                        queryset[i].last_message = '點我讀取案件訂單訊息！'
                    else:
                        queryset[i].last_message = last_message.content[0:15]
                
                chat_rooms_not_read_messages = ChatroomMessage.objects.filter(chatroom=queryset[i],is_read_by_other_side=False).filter(~Q(user=user))
                queryset[i].unread_num = chat_rooms_not_read_messages.count()
            except:
                # queryset.exclude(id=queryset[i].id)
                queryset[i].last_message = '對方用戶已刪除！'

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

class MessageViewSet(APIView):
    # queryset = Message.objects.all()
    # serializer_class = serializers.MessageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        user = self.request.user
        chatroom= self.request.query_params.get('chatroom')
        user_ids = list(ChatroomUserShip.objects.filter(chatroom=chatroom).values_list('user', flat=True))
  
        if user.id in user_ids:
            queryset = ChatroomMessage.objects.filter(chatroom=chatroom).order_by('id')

            #update is_read_by_other_side
            queryset.filter(~Q(user=user)).update(is_read_by_other_side=True)

            for i in range(len(queryset)):
                if queryset[i].user == user:
                    queryset[i].message_is_mine = True
                # if queryset[i].case != None:
                #     queryset[i].orders = Order.objects.filter(case=queryset[i].case)
                if queryset[i].case != None and queryset[i].is_this_message_only_case:
                    queryset[i].case_detail = queryset[i].case

            serializer = serializers.MessageSerializer(queryset, many=True)

            # 把聊天室中兩人發過的案子都撈出來
            # 如果其中一人接了對方其中一個案子, 即可發圖片
            is_send_image = False
            cases = Case.objects.filter(user__in = user_ids)
            for case in cases:
                if case.servant != None and case.servant.id in user_ids:
                    is_send_image = True

            return Response({'is_send_image':is_send_image,'messages': serializer.data})
 
        return Response({'message': "have no authority"})

    # 上傳聊天室訊息 文字/圖片
    def post(self, request):
        user = self.request.user
        chatroom_id = self.request.query_params.get('chatroom')
        case = request.data.get('case')
        content = request.data.get('content')
        image = request.data.get('image')

        chatroom = ChatRoom.objects.get(id=chatroom_id)
        user_ids = list(ChatroomUserShip.objects.filter(chatroom=chatroom).values_list('user', flat=True))
        chatroom_users = User.objects.filter(id__in=user_ids)

        if user in chatroom_users:
            other_side_user = chatroom_users.exclude(phone=user.phone)[0]
            message = ChatroomMessage()
            message.chatroom = chatroom
            message.user = user
            if case != None:
                message.case = Case.objects.get(id=case)
                message.order = Order.objects.filter(case=message.case).order_by('-created_at')[0]
                message.is_this_message_only_case = True
            
            if content != None:
                message.content = content
                title = '新訊息'
                sendFCMMessage(other_side_user,title,content)
            
            # upload image
            if image != None:
                message.image = image
                title = '新訊息'
                content =  user.name + '傳送了一張新圖片'
                sendFCMMessage(other_side_user,title,content)
            message.save()
            chatroom.update_at = datetime.datetime.now()
            chatroom.save()
            serializer = serializers.MessageSerializer(message)
            return Response(serializer.data)
        else:
            return Response({'message': "have no authority"})


# class MessageViewSet(viewsets.GenericViewSet,
#                     mixins.ListModelMixin,
#                     mixins.CreateModelMixin):
#     queryset = Message.objects.all()
#     serializer_class = serializers.MessageSerializer
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)

#     def get_queryset(self):
#         user = self.request.user
#         chatroom= self.request.query_params.get('chatroom')
#         user_ids = list(ChatroomUserShip.objects.filter(chatroom=chatroom).values_list('user', flat=True))
#         if user.id in user_ids:
#             queryset = self.queryset.filter(chatroom=chatroom).order_by('id')

#             #update is_read_by_other_side
#             queryset.filter(~Q(user=user)).update(is_read_by_other_side=True)

#             for i in range(len(queryset)):
#                 if queryset[i].user == user:
#                     queryset[i].message_is_mine = True
#                 if queryset[i].case != None:
#                     queryset[i].orders = Order.objects.filter(case=queryset[i].case)
#                 if queryset[i].case != None and queryset[i].is_this_message_only_case:
#                     queryset[i].case_detail = queryset[i].case
                
#             return queryset
#         return Response({'message': "have no authority"})

#     def create(self, request, *args, **kwargs):
#         user = self.request.user
#         chatroom_id = self.request.query_params.get('chatroom')
#         case = request.data.get('case')
#         content = request.data.get('content')
#         image = request.data.get('image')

#         chatroom = ChatRoom.objects.get(id=chatroom_id)
#         user_ids = list(ChatroomUserShip.objects.filter(chatroom=chatroom).values_list('user', flat=True))

#         if user.id in user_ids:
#             message = Message()
#             message.chatroom = chatroom
#             message.user = user
#             if case != None:
#                 message.case = Case.objects.get(id=case)
#                 message.order = Order.objects.filter(case=message.case).order_by('-created_at')[0]
#                 message.is_this_message_only_case = True
            
#             if content != None:
#                 message.content = content
            
#             # upload image
#             if image != None:
#                 message.image = image

#             message.save()
#             chatroom.update_at = datetime.datetime.now()
#             chatroom.save()
#             serializer = self.get_serializer(message)
#             return Response(serializer.data)
#         else:
#             return Response({'message': "have no authority"})

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
        is_continuous_time = self.request.query_params.get('is_continuous_time')

        is_random = self.request.query_params.get('is_random')

        #2022-07-10T00:00:00Z
        start_datetime = self.request.query_params.get('start_datetime')
        end_datetime = self.request.query_params.get('end_datetime')
        #1,3,5
        weekdays = self.request.query_params.get('weekdays')
        #8:22
        start_end_time = self.request.query_params.get('start_end_time')
        order = self.request.query_params.get('order')

        queryset = User.objects.filter(is_servant_passed=True)
        if care_type == 'home':
            queryset = queryset.filter(is_home=True)
        elif care_type == 'hospital':
            queryset = queryset.filter(is_hospital=True)

        if city != None:
            queryset = queryset.filter(user_locations__city=City.objects.get(id=city))

        if start_datetime != None:
            start_date = start_datetime.split('T')[0]
            end_date = end_datetime.split('T')[0]
            start_time_int = int(start_end_time.split(':')[0])
            end_time_int = int(start_end_time.split(':')[1])
            #以下兩個情形只會有其中一個發生
            if is_continuous_time == 'True':
                queryset = queryset.filter(is_continuous_time=True)
            
            #所選擇的周間跟時段 要符合 servant 的服務時段
            elif weekdays != None:
                
                
                weekdays_num_list = weekdays.split(',')
                service_time_condition_1 = Q(is_continuous_time=True)
                # service_time_condition_2 = Q(user_weekday__weekday__in=weekdays_num_list, user_weekday__start_time__lte=start_time_int, user_weekday__end_time__gte=end_time_int)
                # queryset = queryset.filter(service_time_condition_1 | service_time_condition_2).distinct()
                for weekdays_num in weekdays_num_list:
                    service_time_condition_2 = Q(user_weekday__weekday=weekdays_num, user_weekday__start_time__lte=start_time_int, user_weekday__end_time__gte=end_time_int)
                    queryset = queryset.filter(service_time_condition_1 | service_time_condition_2).distinct()
            
            #情況：如果一個 servant 已經在某個時段已經有了 1 個 order, 就沒辦法再接另一個 order
            #方法：
            #所選擇的日期期間/週間/時段, 
            #要在已有的訂單時段之外, 先找出時段內, 且狀態是 'paid' 的訂單, 
            #然後找出時段內的人, 
            #最後反過來, 非時段內的人就是可以被篩選
            
            #1.取出日期期間有交集的訂單, 且訂單狀態是 paid
            condition1 = Q(start_datetime__range=[start_date, end_date])
            condition2 = Q(end_datetime__range=[start_date, end_date])
            condition3 = Q(start_datetime__lte=start_date)&Q(end_datetime__gte=end_date)

            orders = Order.objects.filter(state='paid').filter(condition1 | condition2 | condition3).distinct()
            #2.再從 1 取出週間有交集的訂單
            #這邊考慮把 Order 的 weekday 再寫成一個 model OrderWeekDay, 然後再去比較, 像 user__weekday 一樣
            if weekdays != None:
                weekdays_num_list = weekdays.split(',')
                
                weekday_condition_1 = Q(order_weekdays__weekday__in=weekdays_num_list)
                weedkay_condition_2 =  Q(case__is_continuous_time=True)
                # orders = orders.filter(order_condition_1 | order_condition_2).distinct()
            #3.再從 2 取出時段有交集的訂單
            time_condition_1 = Q(start_time__range=[start_time_int, end_time_int])
            time_condition_2 = Q(end_time__range=[start_time_int, end_time_int])
            time_condition3 = Q(start_time__lte=start_time_int)&Q(end_time__gte=end_time_int)
            order_condition_1 = Q((weekday_condition_1) & (time_condition_1 | time_condition_2 | time_condition3))
            order_condition_2 = Q((weedkay_condition_2) & (time_condition_1 | time_condition_2 | time_condition3))
            orders = orders.filter(order_condition_1|order_condition_2).distinct()
            # orders = Order.objects.filter(order_condition_2)
            print(orders)
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
                queryset[i].languages = UserLanguage.objects.filter(user=queryset[i])
                queryset[i].avg_rate = Review.objects.filter(servant=queryset[i],servant_rating__gte=1).aggregate(Avg('servant_rating'))['servant_rating__avg']
                queryset[i].rating_nums = Review.objects.filter(servant=queryset[i],servant_rating__gte=1).aggregate(rating_nums=Count('servant_rating'))['rating_nums']
        
        
        # from django.db.models import Case, When

        # ids = list(queryset.values_list('id', flat=True))

        # print(random.shuffle(ids))

        if is_random == 'true':
            results = list(queryset)
            random.shuffle(results)
            return results
        else:
            return queryset

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        user.background_image_url = User.objects.get(phone=user).background_image

        service_ids = list(UserServiceShip.objects.filter(user=user).values_list('service', flat=True))
        user.services = Service.objects.filter(id__in=service_ids)

        for i in range(len(user.services)):
            if user.services[i].id <= 4:
                user.services[i].increase_percent = UserServiceShip.objects.get(user=user, service=user.services[i]).increase_percent

        # license_ids = list(UserLicenseShipImage.objects.filter(user=user).values_list('license', flat=True))
        # user.licences = License.objects.filter(id__in=license_ids)

        user.licences = UserLicenseShipImage.objects.filter(user=user)

        # language_ids = list(UserLanguage.objects.filter(user=user).values_list('language', flat=True))
        # user.languages = Language.objects.filter(id__in=language_ids)

        user.languages = UserLanguage.objects.filter(user=user)

        user.avg_rate = Review.objects.filter(servant=user,servant_rating__gte=1).aggregate(Avg('servant_rating'))['servant_rating__avg']
        user.rating_nums = Review.objects.filter(servant=user,servant_rating__gte=1).aggregate(rating_nums=Count('servant_rating'))['rating_nums']
        user.about_me = User.objects.get(phone=user).about_me
        user.reviews = Review.objects.filter(servant=user).filter(~Q(servant_rating=0))
        serializer = self.get_serializer(user, context={"request":request})
        
        return Response(serializer.data)

class RecommendServantViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,):
    
    queryset = User.objects.all()
    serializer_class = serializers.ServantSerializer

    def get_queryset(self):

        care_type= self.request.query_params.get('care_type')
        city = self.request.query_params.get('city')

        is_random = self.request.query_params.get('is_random')

        queryset = User.objects.filter(is_servant_passed=True)
        
        user_ids = list(UserServiceLocation.objects.all().values_list('user', flat=True).distinct())
        queryset = queryset.filter(id__in=user_ids)

        if care_type == 'home':
            queryset = queryset.filter(is_home=True)
        elif care_type == 'hospital':
            queryset = queryset.filter(is_hospital=True)

        if city != None:
            queryset = queryset.filter(user_locations__city=City.objects.get(id=city)).distinct()


        for i in range(len(queryset)):
            queryset[i].avg_rate = Review.objects.filter(servant=queryset[i],servant_rating__gte=1).aggregate(Avg('servant_rating'))['servant_rating__avg']
            queryset[i].rating_nums = Review.objects.filter(servant=queryset[i],servant_rating__gte=1).aggregate(rating_nums=Count('servant_rating'))['rating_nums']
            queryset[i].locations = UserServiceLocation.objects.filter(user=queryset[i])

        if is_random == 'true':
            results = list(queryset)
            random.shuffle(results)
            return results
        else:
            return queryset

class CaseSearchViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,):
    queryset = Case.objects.all()
    serializer_class = serializers.CaseSerializer

    def get_queryset(self):
        city = self.request.query_params.get('city')
        #2022-07-10T00:00:00Z
        start_datetime = self.request.query_params.get('start_datetime')
        # end_datetime = self.request.query_params.get('end_datetime')
        care_type= self.request.query_params.get('care_type')
        queryset = self.queryset.filter(is_taken=False).filter(is_open_for_search=True).filter(~Q(user=None)).order_by('-id')

        if city != None:
            queryset = queryset.filter(city=City.objects.get(id=city))

        # if start_datetime != None and end_datetime != None :
        #     queryset = queryset.filter(start_datetime__gte=start_datetime,end_datetime__lte=end_datetime)

        now = datetime.datetime.now() + timedelta(hours=8)
        now_day = datetime.datetime(now.year , now.month , now.day , 0 , 0)

        if start_datetime != None:
            queryset = queryset.filter(start_datetime__gte=start_datetime)

        if start_datetime == None:
            queryset = queryset.filter(start_datetime__gte=now_day)
        
        if care_type == 'home':
            queryset = queryset.filter(care_type='home')
        elif care_type == 'hospital':
            queryset = queryset.filter(care_type='hospital')

        return queryset

    def retrieve(self, request, *args, **kwargs):
        case = self.get_object()
        case.num_offender_rating = Review.objects.filter(order__case=case,case_offender_rating__gte=1).aggregate(num_offender_rating=Count('case_offender_rating'))['num_offender_rating']
        case.avg_offender_rating  = Review.objects.filter(order__case=case,case_offender_rating__gte=1).aggregate(case_offender_rating =Avg('case_offender_rating'))['case_offender_rating']
        # if case.is_taken == True:
        #     case.status = '案件已關閉'
        # else:
        #     case.status = '尚未找到服務者'
        
        disease_ids = list(CaseDiseaseShip.objects.filter(case=case).values_list('disease', flat=True))
        case.disease = DiseaseCondition.objects.filter(id__in=disease_ids)
        body_condition_ids = list(CaseBodyConditionShip.objects.filter(case=case).values_list('body_condition', flat=True))
        case.body_condition = BodyCondition.objects.filter(id__in=body_condition_ids)
        service_ids = list(CaseServiceShip.objects.filter(case=case).values_list('service', flat=True))
        case.services = Service.objects.filter(id__in=service_ids)
        case.user_detail = case.user

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
        queryset = self.queryset.filter(servant=servant).order_by('-start_datetime')

        for i in range(len(queryset)):
            reviews = Review.objects.filter(case=queryset[i])
            for reiview in reviews:
                if reiview.servant_rating != None:
                    queryset[i].servant_rating = reiview.servant_rating
        return queryset

    def retrieve(self, request, *args, **kwargs):
        case = self.get_object()
        servant = self.request.user
        if case.servant == servant:
            reviews = Review.objects.filter(case=case)
            for review in reviews:
                if review.order.state == 'paid' or review.order.state == 'cancelOrEarlyEnd':
                    case.review = review
                    case.servant_rating = review.servant_rating

            if case.care_type == 'home':
                case.hour_wage = case.servant.home_hour_wage
            elif case.care_type == 'hospital':
                case.hour_wage = case.servant.hospital_hour_wage
            
            disease_ids = list(CaseDiseaseShip.objects.filter(case=case).values_list('disease', flat=True))
            case.disease = DiseaseCondition.objects.filter(id__in=disease_ids)
            body_condition_ids = list(CaseBodyConditionShip.objects.filter(case=case).values_list('body_condition', flat=True))
            case.body_condition = BodyCondition.objects.filter(id__in=body_condition_ids)

            service_ids = list(CaseServiceShip.objects.filter(case=case).values_list('service', flat=True)) 
            case.services  = Service.objects.filter(id__in=service_ids)

            # 以下做 order 相關欄位
            orders = Order.objects.filter(case=case)
            for order in orders:
                if order.state == 'paid' or order.state == 'cancelOrEarlyEnd':
                    case.order = order
                    case.order.increase_services = OrderIncreaseService.objects.filter(order=order)

            # case.work_hours = order.work_hours
            # case.base_money = order.base_money
            # case.platform_percent = order.platform_percent
            # # !!!
            # case.platform_money = order.platform_money
            # case.total_money = order.total_money
            # increase_service_ids = list(CaseServiceShip.objects.filter(case=case,service__is_increase_price=True).values_list('service', flat=True))
            # case.increase_money = OrderIncreaseService.objects.filter(order=order,service__id__in=increase_service_ids)

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
        queryset = self.queryset.filter(user=user).order_by('-start_datetime')
        
        for i in range(len(queryset)):
            # language_ids = list(UserLanguage.objects.filter(user=queryset[i].user.id).values_list('language', flat=True))
            # queryset[i].servant.languages = Language.objects.filter(id__in=language_ids)
            
            if queryset[i].servant != None:
                queryset[i].servant.languages = UserLanguage.objects.filter(user=queryset[i].user.id)

        return queryset

    def retrieve(self, request, *args, **kwargs):
        case = self.get_object()
        user = self.request.user
        if case.user == user:  
            if case.servant != None:
                if case.care_type == 'home':
                    case.hour_wage = case.servant.home_hour_wage
                elif case.care_type == 'hospital':
                    case.hour_wage = case.servant.hospital_hour_wage
                
                case.servant.languages = UserLanguage.objects.filter(user=user)
            
            if Review.objects.filter(case=case).count()!=0:
                reviews = Review.objects.filter(case=case)
                for review in reviews:
                    if review.order.state == 'paid' or review.order.state == 'cancelOrEarlyEnd':
                        case.servant_rating = review.servant_rating
                        case.review = review

            disease_ids = list(CaseDiseaseShip.objects.filter(case=case).values_list('disease', flat=True))
            case.disease = DiseaseCondition.objects.filter(id__in=disease_ids)

            body_condition_ids = list(CaseBodyConditionShip.objects.filter(case=case).values_list('body_condition', flat=True))
            case.body_condition = BodyCondition.objects.filter(id__in=body_condition_ids)

            service_ids = list(CaseServiceShip.objects.filter(case=case).values_list('service', flat=True)) 
            case.services  = Service.objects.filter(id__in=service_ids)
            
            # language_ids = list(UserLanguage.objects.filter(user=user).values_list('language', flat=True))
            # case.servant.languages = Language.objects.filter(id__in=language_ids)

            if Order.objects.filter(case=case).count()!=0:
                orders = Order.objects.filter(case=case)
                for order in orders:
                    if order.state == 'paid' or order.state == 'cancelOrEarlyEnd':
                        case.order = order
                        case.order.increase_services = OrderIncreaseService.objects.filter(order=order)

            # 以下做 order 相關欄位
            # order = Order.objects.get(case=case)
            # case.work_hours = order.work_hours
            # case.base_money = order.base_money
            # case.platform_percent = order.platform_percent
            # # !!!!!!
            # case.platform_money = order.platform_money
            # case.total_money = order.total_money
            # increase_service_ids = list(CaseServiceShip.objects.filter(case=case,service__is_increase_price=True).values_list('service', flat=True))
            # case.increase_money = OrderIncreaseService.objects.filter(order=order,service__id__in=increase_service_ids)

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
        
        ids = []
        for i in range(len(queryset)):
            if queryset[i].order.state == 'paid' or queryset[i].order.state == 'cancelOrEarlyEnd':
                ids.append(queryset[i].id)

        queryset = queryset.filter(id__in=ids)

        #filter後面(review = review 是？)
        # reviews = Review.objects.filter(review=review)
        # for review in reviews:
        #     if review.order.state == 'paid':
                #review.review = review
                #review.servant_rating = review.servant_rating
       

        #review_type=unrated, given, received
        review_type = self.request.query_params.get('review_type')

        if review_type == 'unrated':
            queryset = queryset.filter(servant_rating__lt=1)
        elif review_type == 'given':
            queryset = queryset.filter(servant_rating__gte=1)
        elif review_type == 'received':
            queryset = queryset.filter(case_offender_rating__gte=1)  

        for i in range(len(queryset)):
            # queryset[i].care_type = queryset[i].case.care_type
            # queryset[i].is_continuous_time = queryset[i].case.is_continuous_time

            queryset[i].start_datetime = queryset[i].case.start_datetime
            queryset[i].end_datetime = queryset[i].case.end_datetime
            queryset[i].user_avg_rate = queryset.filter(case_offender_rating__gte=1).aggregate(Avg('case_offender_rating'))['case_offender_rating__avg']
            queryset[i].user_rating_nums = queryset.filter(case_offender_rating__gte=1).aggregate(Count('case_offender_rating'))['case_offender_rating__count']
        return queryset

    #從資料庫取回要顯示的資料？
    def retrieve(self, request, *args, **kwargs):
        review = self.get_object()
        user = self.request.user
        if review.case.user == user: 
            # review.care_type = review.case.care_type
            # review.is_continuous_time = review.case.is_continuous_time
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
            review.servant_rating_created_at = datetime.datetime.now()
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
            review.case_offender_rating_created_at = datetime.datetime.now()
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
        county_id = self.request.query_params.get('county')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        start_time = self.request.query_params.get('start_time')
        start_time = start_time.split(':')
        end_time = self.request.query_params.get('end_time')
        end_time = end_time.split(':')
        
        #home, hospital
        care_type = request.data.get('care_type')
        is_continuous_time = request.data.get('is_continuous_time')
        name = request.data.get('name')
        #M, F
        gender = request.data.get('gender')
        age = request.data.get('age')
        weight = request.data.get('weight')
        #1,2,4
        disease = request.data.get('disease')
        disease_remark = request.data.get('disease_remark')
        #1,4,6
        body_condition = request.data.get('body_condition')
        conditions_remark = request.data.get('conditions_remark')
        #1,7,9
        service = request.data.get('service')
        
        weekday = request.data.get('weekday')

        road_name = request.data.get('road_name')
        hospital_name = request.data.get('hospital_name')

        emergencycontact_name = request.data.get('emergencycontact_name')
        emergencycontact_relation = request.data.get('emergencycontact_relation')
        emergencycontact_phone = request.data.get('emergencycontact_phone')

        #searvant_ids=1,4,7 => 要產生 message, order
        servant_ids = request.data.get('servant_ids')

        case = Case()
        case.created_at = datetime.datetime.now()
        case.user = user
        case.county = County.objects.get(id=county_id)
        case.city = case.county.city
        
        if care_type == 'home' and request.data.get('road_name')!=None:
            case.road_name = request.data.get('road_name')
        elif care_type == 'hospital' and request.data.get('hospital_name')!=None:
            case.hospital_name = request.data.get('hospital_name')

        #start_datetime=2022-07-21
        #s = "2014-04-07"
        #datetime.datetime.strptime(s, "%Y-%m-%d").date()
        case.start_datetime = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        case.end_datetime = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        
        # weekday = 1,3,5
        case.weekday = weekday

        case.start_time = int(start_time[0]) + float(int(start_time[1])/60)
        case.end_time = int(end_time[0]) + float(int(end_time[1])/60)
        if name != None:
            case.name = name
        if care_type != None:
            case.care_type = care_type
        if is_continuous_time == 'True' or is_continuous_time == 'true':
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
        if road_name != None:
            case.road_name = road_name
        if hospital_name != None:
            case.hospital_name = hospital_name
        if emergencycontact_name != None:
            case.emergencycontact_name = emergencycontact_name
        if emergencycontact_relation != None:
            case.emergencycontact_relation = emergencycontact_relation
        if emergencycontact_phone != None:
            case.emergencycontact_phone = emergencycontact_phone

        case.is_open_for_search = True
        case.save()

        if disease != None and disease != '':
            disease_ids = disease.split(',')
            for disease_id in disease_ids:
                casediseaseship = CaseDiseaseShip()
                casediseaseship.disease = DiseaseCondition.objects.get(id=disease_id)
                casediseaseship.case = case
                casediseaseship.save()

        if body_condition != None and body_condition != '':
            body_condition_ids = body_condition.split(',')
            for body_condition_id in body_condition_ids:
                casebodyconditionship = CaseBodyConditionShip()
                casebodyconditionship.body_condition = BodyCondition.objects.get(id=body_condition_id)
                casebodyconditionship.case = case
                casebodyconditionship.save()
        
        service_ids = []
        if service != None and service != '':
            service_ids = service.split(',')
            for service_id in service_ids:
                caseserviceship = CaseServiceShip()
                caseserviceship.service = Service.objects.get(id=service_id)
                caseserviceship.case = case
                caseserviceship.save()

        # 這邊要針對個別 servant 產生訂單~ 要有系統訊息, 推播訊息, 並檢查 transferFee, roadName, hospitalName 等新欄位
        if servant_ids != None and servant_ids!= '':
            servant_id_list = servant_ids.split(',')
            for servant_id in servant_id_list:
                servant = User.objects.get(id=servant_id)
                
                order = Order()
                order.created_at = datetime.datetime.now()
                order.case = case
                order.user = case.user
                order.servant = servant
                order.state = 'unPaid'
                order.start_datetime = case.start_datetime
                order.end_datetime = case.end_datetime
                order.start_time = order.case.start_time
                order.end_time = order.case.end_time

                if order.case.care_type == 'home':
                    order.that_time_hour_wage = servant.home_hour_wage
                    order.that_time_half_day_wage = servant.home_half_day_wage
                    order.that_time_one_day_wage = servant.home_one_day_wage
                else:
                    order.that_time_hour_wage = servant.hospital_hour_wage
                    order.that_time_half_day_wage = servant.hospital_half_day_wage
                    order.that_time_one_day_wage = servant.hospital_one_day_wage

                order.save()

                transfer_fee = UserServiceLocation.objects.get(user=order.servant,city=order.case.city).transfer_fee
                order.transfer_fee = transfer_fee
                if order.case.is_continuous_time == False:
                    weekdays = order.case.weekday.split(',')
                    for weekday in weekdays:
                        orderWeekday = OrderWeekDay()
                        orderWeekday.order = order
                        orderWeekday.weekday = weekday
                        orderWeekday.save()

                    weekday_list = list(OrderWeekDay.objects.filter(order=order).values_list('weekday', flat=True))
                    
                    days = days_count(weekday_list, order.start_datetime.date(), order.end_datetime.date())
                    number_of_transfer = days
                    total_hours = days * (order.end_time - order.start_time)

                    order.work_hours = total_hours
                    order.number_of_transfer = number_of_transfer
                    order.amount_transfer_fee = transfer_fee * number_of_transfer
                    one_day_work_hours = order.end_time - order.start_time
                    if order.case.care_type == 'home':
                        if one_day_work_hours < 12:
                            wage = servant.home_hour_wage
                        elif one_day_work_hours >=12 and one_day_work_hours < 24:
                            wage = round(servant.home_half_day_wage/12)
                    elif order.case.care_type == 'hospital':
                        if one_day_work_hours < 12:
                            wage = servant.hospital_hour_wage
                        elif one_day_work_hours >=12 and one_day_work_hours < 24:
                            wage = round(servant.hospital_half_day_wage/12)
                else:
                    order.number_of_transfer = 1
                    order.amount_transfer_fee = transfer_fee * 1
                    
                    total_hours = continuous_time_cal(order)
                    order.work_hours = total_hours

                    if order.case.care_type == 'home':
                        if total_hours < 12:
                            wage = servant.home_hour_wage
                        elif total_hours >=12 and total_hours < 24:
                            wage = round(servant.home_half_day_wage/12)
                        else:
                            wage = round(servant.home_one_day_wage/24)
                    elif order.case.care_type == 'hospital':
                        if total_hours < 12:
                            wage = servant.hospital_hour_wage
                        elif total_hours >=12 and total_hours < 24:
                            wage = round(servant.hospital_half_day_wage/12)
                        else:
                            wage = round(servant.hospital_one_day_wage/24)
                order.wage_hour =wage
                order.base_money = round(order.work_hours * wage)

                # need to change in the future
                order.platform_percent = platform_percent_cal(servant,order)
                order.newebpay_percent = get_newebpay_percent()
                order.save()
                Review.objects.create(order=order,case=order.case,servant=order.servant)
                
                total_increase_money = 0
                for service_id in service_ids:
                    if int(service_id) <= 4:
                        orderIncreaseService = OrderIncreaseService()
                        orderIncreaseService.order = order
                        orderIncreaseService.service = Service.objects.get(id=service_id)
                        if UserServiceShip.objects.filter(user=servant,service=Service.objects.get(id=service_id)).count() > 0:
                            orderIncreaseService.increase_percent = UserServiceShip.objects.get(user=servant,service=Service.objects.get(id=service_id)).increase_percent
                        else:
                            orderIncreaseService.increase_percent = 0
                        orderIncreaseService.increase_money = round((order.base_money) * (orderIncreaseService.increase_percent)/100)
                        orderIncreaseService.save()

                        total_increase_money = total_increase_money + orderIncreaseService.increase_money

                total_service_money =  order.base_money + total_increase_money
                order.total_money = total_service_money + order.amount_transfer_fee

                order.newebpay_money = round(order.total_money * (order.newebpay_percent/100))
                order.platform_money = round(order.total_money * (order.platform_percent/100))

                order.servant_money = order.total_money - order.newebpay_money - order.platform_money
                order.save()

                receiveBooking(servant,order)
                chatroom_ids1 = list(ChatroomUserShip.objects.filter(user=case.user).values_list('chatroom', flat=True))
                chatroom_ids2 = list(ChatroomUserShip.objects.filter(user=servant).values_list('chatroom', flat=True))
                chatroom_set = set(chatroom_ids1).intersection(set(chatroom_ids2))
                print(chatroom_set,1)
                if list(chatroom_set) != []:
                    chatroom_id = list(chatroom_set)[0]
                    print(chatroom_id,2)
                    chatroom = ChatRoom.objects.get(id=chatroom_id)
                    message = ChatroomMessage(user=user,case=case,chatroom=chatroom,order=order,is_this_message_only_case=True)
                    message.save()
                elif list(chatroom_set) == []:
                    chatroom = ChatRoom()
                    chatroom.save()
                    # print(chatroom_id,3)
                    ChatroomUserShip.objects.create(user=user,chatroom=chatroom)
                    ChatroomUserShip.objects.create(user=servant,chatroom=chatroom)
                    message = ChatroomMessage(user=user,case=case,chatroom=chatroom,order=order,is_this_message_only_case=True)
                    message.save()
                chatroom.update_at = datetime.datetime.now()
                chatroom.save()

        disease_idList = list(CaseDiseaseShip.objects.filter(case=case).values_list('disease', flat=True))
        case.disease = DiseaseCondition.objects.filter(id__in=disease_idList)
        body_condition_idList = list(CaseBodyConditionShip.objects.filter(case=case).values_list('body_condition', flat=True))
        case.body_condition = BodyCondition.objects.filter(id__in=body_condition_idList)
        service_idList = list(CaseServiceShip.objects.filter(case=case).values_list('service', flat=True))
        case.services = Service.objects.filter(id__in=service_idList)

        serializer = self.serializer_class(case)
        return Response(serializer.data)

class CreateServantOrder(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

    #要有系統訊息, 推播訊息, 並檢查 transferFee,roadName, hospitalName 等新欄位
    def post(self, request, format=None):
        user = self.request.user
        servant_id = self.request.query_params.get('servant_id')
        servant = User.objects.get(id=servant_id)
        county_id = self.request.query_params.get('county')
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
        road_name = request.data.get('road_name')
        hospital_name = request.data.get('hospital_name')
        emergencycontact_name = request.data.get('emergencycontact_name')
        emergencycontact_relation = request.data.get('emergencycontact_relation')
        emergencycontact_phone = request.data.get('emergencycontact_phone')
        is_open_for_search = request.data.get('is_open_for_search')

        case = Case()
        case.created_at = datetime.datetime.now()
        case.user = user
        # case.servant = servant
        case.county = County.objects.get(id=county_id)
        case.city = case.county.city

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
        if is_continuous_time == "True" or is_continuous_time == "true":
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
        if road_name != None:
            case.road_name = road_name
        if hospital_name != None:
            case.hospital_name = hospital_name
        if emergencycontact_name != None:
            case.emergencycontact_name = emergencycontact_name
        if emergencycontact_relation != None:
            case.emergencycontact_relation = emergencycontact_relation
        if emergencycontact_phone != None:
            case.emergencycontact_phone = emergencycontact_phone
        if is_open_for_search == "True" or is_continuous_time == "true":
            case.is_open_for_search = True
        else:
            case.is_open_for_search = False
        case.save()

        if disease != None and disease != '':
            disease_ids = disease.split(',')
            for disease_id in disease_ids:
                casediseaseship = CaseDiseaseShip()
                casediseaseship.disease = DiseaseCondition.objects.get(id=disease_id)
                casediseaseship.case = case
                casediseaseship.save()

        if body_condition != None and body_condition != '':
            body_condition_ids = body_condition.split(',')
            for body_condition_id in body_condition_ids:
                casebodyconditionship = CaseBodyConditionShip()
                casebodyconditionship.body_condition = BodyCondition.objects.get(id=body_condition_id)
                casebodyconditionship.case = case
                casebodyconditionship.save()

        if service != None and service != '':
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
        order.created_at = datetime.datetime.now()
        order.case = case
        order.user = case.user
        order.servant = servant
        order.state = 'unPaid'
        order.start_datetime = case.start_datetime
        order.end_datetime = case.end_datetime
        order.start_time = order.case.start_time
        order.end_time = order.case.end_time

        if order.case.care_type == 'home':
            order.that_time_hour_wage = servant.home_hour_wage
            order.that_time_half_day_wage = servant.home_half_day_wage
            order.that_time_one_day_wage = servant.home_one_day_wage
        else:
            order.that_time_hour_wage = servant.hospital_hour_wage
            order.that_time_half_day_wage = servant.hospital_half_day_wage
            order.that_time_one_day_wage = servant.hospital_one_day_wage

        order.save()

        order.save()
        transfer_fee = UserServiceLocation.objects.get(user=order.servant,city=order.case.city).transfer_fee
        order.transfer_fee = transfer_fee
       
        if order.case.is_continuous_time == False:
            weekdays = order.case.weekday.split(',')
            for weekday in weekdays:
                orderWeekday = OrderWeekDay()
                orderWeekday.order = order
                orderWeekday.weekday = weekday
                orderWeekday.save()

            weekday_list = list(OrderWeekDay.objects.filter(order=order).values_list('weekday', flat=True))

            days = days_count(weekday_list, order.start_datetime.date(), order.end_datetime.date())
            number_of_transfer = days
            total_hours = days * (order.end_time - order.start_time)

            # total_hours = 0
            # number_of_transfer = 0
            # for i in weekday_list:
            #     number_of_transfer 
            #     total_hours += (days_count([int(i)], order.start_datetime.date(), order.end_datetime.date())) * (order.end_time - order.start_time)

            order.work_hours = total_hours
            order.number_of_transfer = number_of_transfer
            order.amount_transfer_fee = transfer_fee * number_of_transfer
            one_day_work_hours = order.end_time - order.start_time
            if order.case.care_type == 'home':
                if one_day_work_hours < 12:
                    wage = order.servant.home_hour_wage
                elif one_day_work_hours >=12 and one_day_work_hours < 24:
                    wage = round(order.servant.home_half_day_wage/12)
            elif order.case.care_type == 'hospital':
                if one_day_work_hours < 12:
                    wage = order.servant.hospital_hour_wage
                elif one_day_work_hours >=12 and one_day_work_hours < 24:
                    wage = round(order.servant.hospital_half_day_wage/12)
        else:
            order.number_of_transfer = 1
            order.amount_transfer_fee = transfer_fee * 1
            # diff = order.end_datetime - order.start_datetime
            # days, seconds = diff.days, diff.seconds
            # hours = days * 24 + seconds // 3600
            # minutes = (seconds % 3600) // 60
            total_hours = continuous_time_cal(order)
            order.work_hours = total_hours
            if order.case.care_type == 'home':
                if total_hours < 12:
                    wage = order.servant.home_hour_wage
                elif total_hours >=12 and total_hours < 24:
                    wage = round(order.servant.home_half_day_wage/12)
                else:
                    wage = round(order.servant.home_one_day_wage/24)
            elif order.case.care_type == 'hospital':
                if total_hours < 12:
                    wage = order.servant.hospital_hour_wage
                elif total_hours >=12 and total_hours < 24:
                    wage = round(order.servant.hospital_half_day_wage/12)
                else:
                    wage = round(order.servant.hospital_one_day_wage/24)
        order.wage_hour =wage
        order.base_money = round(order.work_hours * wage)

        # need to change in the future
        order.platform_percent = platform_percent_cal(servant,order)
        order.newebpay_percent = get_newebpay_percent()
        order.save()
        Review.objects.create(order=order,case=order.case,servant=order.servant)

        total_increase_money = 0
        if service != None and service != '':
            for service_id in service_idList:
                if int(service_id) <= 4:
                    orderIncreaseService = OrderIncreaseService()
                    orderIncreaseService.order = order
                    orderIncreaseService.service = Service.objects.get(id=service_id)
                    if UserServiceShip.objects.filter(user=servant,service=Service.objects.get(id=service_id)).count() > 0:
                        orderIncreaseService.increase_percent = UserServiceShip.objects.get(user=servant,service=Service.objects.get(id=service_id)).increase_percent
                    else:
                        orderIncreaseService.increase_percent = 0
                    orderIncreaseService.increase_money = round((order.base_money) * (orderIncreaseService.increase_percent)/100)
                    orderIncreaseService.save()

                    total_increase_money = total_increase_money + orderIncreaseService.increase_money

        total_service_money =  order.base_money + total_increase_money
        order.total_money = total_service_money + order.amount_transfer_fee
        
        order.newebpay_money = round(order.total_money * (order.newebpay_percent/100))
        order.platform_money = round(order.total_money * (order.platform_percent/100))

        order.servant_money = order.total_money - order.newebpay_money - order.platform_money
        order.save()

        receiveBooking(servant,order)
        chatroom_ids1 = list(ChatroomUserShip.objects.filter(user=case.user).values_list('chatroom', flat=True))
        chatroom_ids2 = list(ChatroomUserShip.objects.filter(user=servant).values_list('chatroom', flat=True))
        chatroom_set = set(chatroom_ids1).intersection(set(chatroom_ids2))
        print(chatroom_set,1)

        if list(chatroom_set) != []:
            chatroom_id = list(chatroom_set)[0]
            # print(chatroom_id,2)
            chatroom = ChatRoom.objects.get(id=chatroom_id)
            message = ChatroomMessage(user=user,case=case,order=order,chatroom=chatroom,is_this_message_only_case=True)
            message.save()
        elif list(chatroom_set) == []:
            chatroom = ChatRoom()
            chatroom.save()
            # print(chatroom_id,3)
            ChatroomUserShip.objects.create(user=user,chatroom=chatroom)
            ChatroomUserShip.objects.create(user=servant,chatroom=chatroom)
            message = ChatroomMessage(user=user,case=case,order=order,chatroom=chatroom,is_this_message_only_case=True)
            message.save()

        chatroom.update_at = datetime.datetime.now()
        chatroom.save()
        order.related_case = case
        # for weekday in 
        serializer = self.serializer_class(order)
        return Response(serializer.data)

class ApplyCase(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        servant = self.request.user
        case_id = request.data.get('case_id')

        if servant.is_servant_passed:
            case = Case.objects.get(id=case_id)

            if Order.objects.filter(case=case, servant=servant, state='unPaid').count()!=0:
                return Response({'message': "您已經申請過此案，請等待聊聊回應！"})

            if servant == case.user:
                return Response({'message': "不能申請自己發的案！"})

            # 底下的 order.transfer_fee 會用到這邊的 transfer_fee
            if UserServiceLocation.objects.filter(user=servant,city=case.city).count()!= 0:
                transfer_fee = UserServiceLocation.objects.get(user=servant,city=case.city).transfer_fee
            else:
                return Response({'message': "您不符合接案資格，請至會員中心更新您的服務地區。"})

            if case.care_type == 'home' and servant.is_home == False:
                return Response({'message': "您不符合接案資格，請至會員中心更新您的服務類型。"})
            elif case.care_type == 'hospital' and servant.is_hospital == False:
                return Response({'message': "您不符合接案資格，請至會員中心更新您的服務類型。"})

            order = Order()
            order.created_at = datetime.datetime.now()
            order.case = case
            order.user = case.user
            order.servant = servant
            order.state = 'unPaid'
            order.start_datetime = case.start_datetime
            order.end_datetime = case.end_datetime
            order.start_time = order.case.start_time
            order.end_time = order.case.end_time

            order.transfer_fee = transfer_fee

            if order.case.care_type == 'home':
                order.that_time_hour_wage = servant.home_hour_wage
                order.that_time_half_day_wage = servant.home_half_day_wage
                order.that_time_one_day_wage = servant.home_one_day_wage
            else:
                order.that_time_hour_wage = servant.hospital_hour_wage
                order.that_time_half_day_wage = servant.hospital_half_day_wage
                order.that_time_one_day_wage = servant.hospital_one_day_wage

            order.save()
            
            # 計算連續時間 或 非連續時間費用
            if order.case.is_continuous_time == False:
                weekdays = order.case.weekday.split(',')
                for weekday in weekdays:
                    orderWeekday = OrderWeekDay()
                    orderWeekday.order = order
                    orderWeekday.weekday = weekday
                    orderWeekday.save()
                
                weekday_list = list(OrderWeekDay.objects.filter(order=order).values_list('weekday', flat=True))

                days = days_count(weekday_list, order.start_datetime.date(), order.end_datetime.date())
                number_of_transfer = days
                total_hours = days * (order.end_time - order.start_time)
                
                order.work_hours = total_hours
                order.number_of_transfer = number_of_transfer
                order.amount_transfer_fee = transfer_fee * number_of_transfer
                one_day_work_hours = order.end_time - order.start_time
                if order.case.care_type == 'home':
                    if servant.is_home:
                        if one_day_work_hours < 12:
                            wage = order.servant.home_hour_wage
                        elif one_day_work_hours >=12 and one_day_work_hours < 24:
                            wage = round(order.servant.home_half_day_wage/12)
                    else:
                        return Response({'message': "您不符合接案資格，請至會員中心更新您的服務類型及地區。"})
                elif order.case.care_type == 'hospital':
                    if servant.is_hospital:
                        if one_day_work_hours < 12:
                            wage = order.servant.hospital_hour_wage
                        elif one_day_work_hours >=12 and one_day_work_hours < 24:
                            wage = round(order.servant.hospital_half_day_wage/12)
                    else:
                        return Response({'message': "您不符合接案資格，請至會員中心更新您的服務類型及地區。"})
            else:
                order.number_of_transfer = 1
                order.amount_transfer_fee = transfer_fee * 1
                # diff = order.end_datetime - order.start_datetime
                # days, seconds = diff.days, diff.seconds
                # hours = days * 24 + seconds // 3600
                # minutes = (seconds % 3600) // 60
                total_hours = continuous_time_cal(order)
                order.work_hours = total_hours
                if order.case.care_type == 'home':
                    if servant.is_home:
                        if total_hours < 12:
                            wage = order.servant.home_hour_wage
                        elif total_hours >=12 and total_hours < 24:
                            wage = round(order.servant.home_half_day_wage/12)
                        else:
                            wage = round(order.servant.home_one_day_wage/24)
                    else:
                        return Response({'message': "您不符合接案資格，請至會員中心更新您的服務類型及地區。"})
                elif order.case.care_type == 'hospital':
                    if servant.is_hospital:
                        if total_hours < 12:
                            wage = order.servant.hospital_hour_wage
                        elif total_hours >=12 and total_hours < 24:
                            wage = round(order.servant.hospital_half_day_wage/12)
                        else:
                            wage = round(order.servant.hospital_one_day_wage/24)
                    else:
                        return Response({'message': "您不符合接案資格，請至會員中心更新您的服務類型及地區。"})
            
            order.wage_hour =wage
            order.base_money = round(order.work_hours * wage)

            order.platform_percent = platform_percent_cal(servant,order)
            order.newebpay_percent = get_newebpay_percent()
            order.save()
            Review.objects.create(order=order,case=order.case,servant=order.servant)

            # 計算加價費用
            total_increase_money = 0

            case_services = CaseServiceShip.objects.filter(case=case)
            for case_service in case_services:
                if case_service.service.id <= 4:
                    orderIncreaseService = OrderIncreaseService()
                    orderIncreaseService.order = order
                    orderIncreaseService.service = case_service.service
                    if UserServiceShip.objects.filter(user=servant,service=case_service.service).count() > 0:
                        orderIncreaseService.increase_percent = UserServiceShip.objects.get(user=servant,service=case_service.service).increase_percent
                    else:
                        orderIncreaseService.increase_percent = 0
                    orderIncreaseService.increase_money = round((order.base_money) * (orderIncreaseService.increase_percent)/100)
                    orderIncreaseService.save()

                    total_increase_money = total_increase_money + orderIncreaseService.increase_money

            total_service_money =  order.base_money + total_increase_money
            order.total_money = total_service_money + order.amount_transfer_fee

            order.newebpay_money = round(order.total_money * (order.newebpay_percent/100))
            order.platform_money = round(order.total_money * (order.platform_percent/100))

            order.servant_money = order.total_money - order.newebpay_money - order.platform_money
            order.save()

            # 產生 chatroom message
            # receiveBooking(servant,order)
            chatroom_ids1 = list(ChatroomUserShip.objects.filter(user=case.user).values_list('chatroom', flat=True))
            chatroom_ids2 = list(ChatroomUserShip.objects.filter(user=servant).values_list('chatroom', flat=True))
            chatroom_set = set(chatroom_ids1).intersection(set(chatroom_ids2))
            print(chatroom_set,1)

            if list(chatroom_set) != []:
                chatroom_id = list(chatroom_set)[0]
                # print(chatroom_id,2)
                chatroom = ChatRoom.objects.get(id=chatroom_id)
                message = ChatroomMessage(user=servant,case=case,order=order,chatroom=chatroom,is_this_message_only_case=True)
                message.save()
            elif list(chatroom_set) == []:
                chatroom = ChatRoom()
                chatroom.save()
                # print(chatroom_id,3)
                ChatroomUserShip.objects.create(user=case.user,chatroom=chatroom)
                ChatroomUserShip.objects.create(user=servant,chatroom=chatroom)
                message = ChatroomMessage(user=servant,case=case,order=order,chatroom=chatroom,is_this_message_only_case=True)
                message.save()

            chatroom.update_at = datetime.datetime.now()
            chatroom.save()

            return Response({'message': "您已經向委託人發出接案訊息，請等待聊聊回覆~"})
        else:
            return Response({'message': "您不是服務者，無法向委託人發出接案訊息。"})


class BlogCategoryViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = BlogCategory.objects.all()
    serializer_class = serializers.BlogCategorySerializer

class BlogPostViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin):
    queryset = BlogPost.objects.all()
    serializer_class = serializers.BlogPostListSerializer

    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')
        if category_id != None:
            theCategory = BlogCategory.objects.get(id=category_id)
            post_ids = list(BlogPostCategoryShip.objects.filter(category=theCategory).values_list('post', flat=True))
            queryset = self.queryset.filter(id__in=post_ids,state="publish").order_by('-publish_date')
        else:
            queryset = self.queryset.filter(state="publish").order_by('-publish_date')

        for i in range(len(queryset)):
            ids = list(BlogPostCategoryShip.objects.filter(post=queryset[i]).values_list('category', flat=True))
            queryset[i].categories = BlogCategory.objects.filter(id__in=ids)
            
        return queryset

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        ids = list(BlogPostCategoryShip.objects.filter(post=post).values_list('category', flat=True))
        post.categories = BlogCategory.objects.filter(id__in=ids)
        serializer = serializers.BlogPostSerializer(post)
        return Response(serializer.data)

class EarlyTermination(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def post(self, request, format=None):
        from newebpayApi.tasks import approprivate_money_to_store, debit_money_to_platform, backboard_refound

        user = self.request.user
        end_datetime = self.request.query_params.get('end_datetime')
        order_id = self.request.query_params.get('order_id')
        order = Order.objects.get(id=order_id)
        service_idList = list(CaseServiceShip.objects.filter(case=order.case).values_list('service', flat=True))
        end_date = end_datetime.split(',')[0]
        end_time = end_datetime.split(',')[1]
        EndDate = datetime.datetime.strptime(end_date,'%Y-%m-%d').date()
        EndTime = datetime.datetime.strptime(end_time,'%H:%M').time()
        print(EndDate,EndTime)
        end_datetime = datetime.datetime.combine(EndDate,EndTime)
        timezone = pytz.timezone('UTC')
        aware_datetime = timezone.localize(end_datetime) 
        if aware_datetime >= order.start_datetime:
            order.end_datetime = aware_datetime
            order.end_time = round(EndTime.hour+EndTime.minute/60,1)
            # order.save()

            transfer_fee = UserServiceLocation.objects.get(user=order.servant,city=order.case.city).transfer_fee
            order.transfer_fee = transfer_fee
            if order.case.is_continuous_time == False:
                weekday_list = list(OrderWeekDay.objects.filter(order=order).values_list('weekday', flat=True))
                
                days = days_count(weekday_list, order.start_datetime.date(), order.end_datetime.date())
                number_of_transfer = days
                total_hours = days * (order.end_time - order.start_time)
                one_day_work_hours = order.end_time - order.start_time
                
                # 非連續時間提前結束+50％當天工作時數
                order.work_hours = total_hours + (one_day_work_hours / 2) 
                order.number_of_transfer = number_of_transfer
                order.amount_transfer_fee = transfer_fee * number_of_transfer
                
                if order.case.care_type == 'home':
                    if one_day_work_hours < 12:
                        if order.that_time_hour_wage != None and order.that_time_hour_wage != 0:
                            wage = order.that_time_hour_wage 
                        else:
                            wage = order.servant.home_hour_wage
                    elif one_day_work_hours >=12 and one_day_work_hours < 24:
                        if order.that_time_half_day_wage != None and order.that_time_half_day_wage != 0:
                            wage = round(order.that_time_half_day_wage/12)
                        else:
                            wage = round(order.servant.home_half_day_wage/12)
                elif order.case.care_type == 'hospital':
                    if one_day_work_hours < 12:
                        if order.that_time_hour_wage != None and order.that_time_hour_wage != 0:
                            wage = order.that_time_hour_wage
                        else:
                            wage = order.servant.hospital_hour_wage
                    elif one_day_work_hours >=12 and one_day_work_hours < 24:
                        if order.that_time_half_day_wage != None and order.that_time_half_day_wage != 0:
                            wage = round(order.that_time_half_day_wage/12)
                        else:
                            wage = round(order.servant.hospital_half_day_wage/12)
            else:
                order.number_of_transfer = 1
                order.amount_transfer_fee = transfer_fee * 1
                # diff = order.end_datetime - order.start_datetime
                # days, seconds = diff.days, diff.seconds
                # hours = days * 24 + seconds // 3600
                # minutes = (seconds % 3600) // 60
                total_hours = continuous_time_cal(order)

                # 連續時間提前結束+12hr
                order.work_hours = total_hours + 12 
                if order.case.care_type == 'home':
                    if total_hours < 12:
                        if order.that_time_hour_wage != None and order.that_time_hour_wage != 0:
                            wage = order.that_time_hour_wage 
                        else:
                            wage = order.servant.home_hour_wage
                    elif total_hours >=12 and total_hours < 24:
                        if order.that_time_half_day_wage != None and order.that_time_half_day_wage != 0:
                            wage = round(order.that_time_half_day_wage/12)
                        else:
                            wage = round(order.servant.home_half_day_wage/12)
                    else:
                        if order.that_time_one_day_wage != None and order.that_time_one_day_wage != 0:
                            wage = round(order.that_time_one_day_wage/24)
                        else:
                            wage = round(order.servant.home_one_day_wage/24)
                elif order.case.care_type == 'hospital':
                    if total_hours < 12:
                        if order.that_time_hour_wage != None and order.that_time_hour_wage != 0:
                            wage = order.that_time_hour_wage 
                        else:
                            wage = order.servant.hospital_hour_wage
                    elif total_hours >=12 and total_hours < 24:
                        if order.that_time_half_day_wage != None and order.that_time_half_day_wage != 0:
                            wage = round(order.that_time_half_day_wage/12)
                        else:
                            wage = round(order.servant.hospital_half_day_wage/12)
                    else:
                        if order.that_time_one_day_wage != None and order.that_time_one_day_wage != 0:
                            wage = round(order.that_time_one_day_wage/24)
                        else:
                            wage = round(order.servant.hospital_one_day_wage/24)
            order.wage_hour =wage
            order.base_money = round(order.work_hours * wage)
            # order.save()
            
            # 把之前的 OrderIncreaseService 刪除, 重新產生
            OrderIncreaseService.objects.filter(order=order).delete()
            
            total_increase_money = 0
            for service_id in service_idList:
                if int(service_id) <= 4:
                    orderIncreaseService = OrderIncreaseService()
                    orderIncreaseService.order = order
                    orderIncreaseService.service = Service.objects.get(id=service_id)
                    orderIncreaseService.increase_percent = UserServiceShip.objects.get(user=order.servant,service=Service.objects.get(id=service_id)).increase_percent
                    orderIncreaseService.increase_money = round((order.base_money) * (orderIncreaseService.increase_percent)/100)
                    orderIncreaseService.save()

                    total_increase_money = total_increase_money + orderIncreaseService.increase_money

            total_service_money =  order.base_money + total_increase_money
            newTotalMoney = total_service_money + order.amount_transfer_fee

            back_money = order.total_money - newTotalMoney

            order.total_money = newTotalMoney
            order.newebpay_money = round(order.total_money * (order.newebpay_percent/100))
            order.platform_money = round(order.total_money * (order.platform_percent/100))
            order.servant_money = order.total_money - order.newebpay_money - order.platform_money

            return_message = approprivate_money_to_store(order.id)
            if return_message == 'SUCCESS':
                backboard_refound(order.id, back_money)
                debit_money_to_platform(order.id, order.platform_money)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            order.case.state = "endEarly"
            order.case.save()

            order.state = 'cancelOrEarlyEnd'
            order.is_early_termination = True
            order.save()

            orderEarlyTermination(order.servant,order)
            chatroom_ids1 = list(ChatroomUserShip.objects.filter(user=order.user).values_list('chatroom', flat=True))
            chatroom_ids2 = list(ChatroomUserShip.objects.filter(user=order.servant).values_list('chatroom', flat=True))
            chatroom_set = set(chatroom_ids1).intersection(set(chatroom_ids2))
            if list(chatroom_set) != []:
                chatroom_id = list(chatroom_set)[0]
                print(chatroom_id)
                chatroom = ChatRoom.objects.get(id=chatroom_id)
                message = ChatroomMessage(user=user,case=order.case,order=order,chatroom=chatroom,is_this_message_only_case=True)
                message.save()
            elif list(chatroom_set) == []:
                chatroom = ChatRoom()
                chatroom.save()
                ChatroomUserShip.objects.create(user=order.user,chatroom=chatroom)
                ChatroomUserShip.objects.create(user=order.servant,chatroom=chatroom)
                message = ChatroomMessage(user=user,case=order.case,order=order,chatroom=chatroom,is_this_message_only_case=True)
                message.save()
                
            chatroom.update_at = datetime.datetime.now()
            chatroom.save()
            serializer = self.serializer_class(order)
            return Response(serializer.data)

        elif aware_datetime < order.start_datetime:
            orderCancel(order.servant,order)
            order.state = 'cancelOrEarlyEnd'
            # order.save()
            
            timediff = order.start_datetime - aware_datetime
            timediff_in_hours = int(timediff.total_seconds() / 3600)

            if timediff_in_hours >= 48:
                return_message = approprivate_money_to_store(order.id)
                if return_message == 'SUCCESS':
                    backboard_refound(order.id, order.total_money)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                    
                order.work_hours = 0
                order.base_money = 0
                order.number_of_transfer = 0
                order.amount_transfer_fee = 0
                order.total_money = 0
                order.newebpay_money = 0
                order.platform_money = 0
                order.servant_money = 0

                order.case.state = "Canceled"
                order.case.save()

                order.save()
            elif timediff_in_hours < 48 and timediff_in_hours >= 24:
                # 收取一日費用之 50%
                back_money = order.total_money

                if order.case.is_continuous_time == True:
                    servant_money = order.wage_hour * 24 * 1/2

                    order.work_hours = 12
                    order.base_money = servant_money
                    order.total_money = servant_money
                else:
                    days = (order.end_datetime - order.start_datetime).days
                    one_day_hours = order.work_hours / days
                    servant_money =  round(order.wage_hour * one_day_hours * 1/2)
                    
                    order.work_hours = round(one_day_hours * 1/2, 1)
                    order.base_money = servant_money
                    order.total_money = servant_money

                order.number_of_transfer = 0
                order.amount_transfer_fee = 0

                order.newebpay_money = round(order.total_money * (order.newebpay_percent/100))
                order.platform_money = round(order.total_money * (order.platform_percent/100))
                order.servant_money = order.total_money - order.newebpay_money - order.platform_money

                back_money = back_money - order.total_money
                
                return_message = approprivate_money_to_store(order.id)
                if return_message == 'SUCCESS':
                    backboard_refound(order.id, back_money)
                    debit_money_to_platform(order.id, order.platform_money)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                order.save()

                order.case.state = "Canceled"
                order.case.save()

            elif timediff_in_hours < 24 and timediff_in_hours >= 3:
                # 收取一日費用之 100%
                back_money = order.total_money

                if order.case.is_continuous_time == True:
                    servant_money = order.wage_hour * 24

                    order.work_hours = 24
                    order.base_money = servant_money
                    order.total_money = servant_money
                else:
                    days = (order.end_datetime - order.start_datetime).days
                    one_day_hours = order.work_hours / days
                    servant_money =  order.wage_hour * one_day_hours

                    order.work_hours = one_day_hours
                    order.base_money = servant_money
                    order.total_money = servant_money

                order.number_of_transfer = 0
                order.amount_transfer_fee = 0

                order.newebpay_money = round(order.total_money * (order.newebpay_percent/100))
                order.platform_money = round(order.total_money * (order.platform_percent/100))
                order.servant_money = order.total_money - order.newebpay_money - order.platform_money

                back_money = back_money - order.total_money

                return_message = approprivate_money_to_store(order.id)
                if return_message == 'SUCCESS':
                    backboard_refound(order.id, back_money)
                    debit_money_to_platform(order.id, order.platform_money)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                order.save()

                order.case.state = "Canceled"
                order.case.save()

            elif timediff_in_hours < 3 :
                # 收取一日費用之 100% + 交通費
                back_money = order.total_money

                if order.case.is_continuous_time == True:
                    servant_money = order.wage_hour * 24

                    order.work_hours = 24
                    order.base_money = servant_money
                else:
                    days = (order.end_datetime - order.start_datetime).days
                    one_day_hours = order.work_hours / days
                    servant_money =  order.wage_hour * one_day_hours

                    order.work_hours = one_day_hours
                    order.base_money = servant_money

                order.number_of_transfer = 1
                order.amount_transfer_fee = order.number_of_transfer * order.transfer_fee

                order.total_money = round(servant_money) + order.amount_transfer_fee
                
                order.newebpay_money = round(order.total_money * (order.newebpay_percent/100))
                order.platform_money = round(order.total_money * (order.platform_percent/100))
                order.servant_money = order.total_money - order.newebpay_money - order.platform_money

                back_money = back_money - order.total_money

                return_message = approprivate_money_to_store(order.id)
                if return_message == 'SUCCESS':
                    backboard_refound(order.id, back_money)
                    debit_money_to_platform(order.id, order.platform_money)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                order.save()

                order.case.state = "Canceled"
                order.case.save()

            chatroom_ids1 = list(ChatroomUserShip.objects.filter(user=order.user).values_list('chatroom', flat=True))
            chatroom_ids2 = list(ChatroomUserShip.objects.filter(user=order.servant).values_list('chatroom', flat=True))
            chatroom_set = set(chatroom_ids1).intersection(set(chatroom_ids2))
            if list(chatroom_set) != []:
                chatroom_id = list(chatroom_set)[0]
                print(chatroom_id)
                chatroom = ChatRoom.objects.get(id=chatroom_id)
                message = ChatroomMessage(user=user, case=order.case, order=order, chatroom=chatroom,is_this_message_only_case=True)
                message.save()
            elif list(chatroom_set) == []:
                chatroom = ChatRoom()
                chatroom.save()
                ChatroomUserShip.objects.create(user=order.user,chatroom=chatroom)
                ChatroomUserShip.objects.create(user=order.servant,chatroom=chatroom)
                message = ChatroomMessage(user=user,case=order.case, order=order, chatroom=chatroom,is_this_message_only_case=True)
                message.save()
                
            chatroom.update_at = datetime.datetime.now()
            chatroom.save()
            serializer = self.serializer_class(order)
            return Response(serializer.data)

class EditCase(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Case.objects.all()
    serializer_class = serializers.CaseSerializer

    def post(self, request, format=None):
        user = self.request.user
        case_id = self.request.query_params.get('case_id')
        countyId = self.request.query_params.get('county')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        weekday = self.request.query_params.get('weekday')
        start_time = self.request.query_params.get('start_time')
        start_time = start_time.split(':')
        end_time = self.request.query_params.get('end_time')
        end_time = end_time.split(':')
        servant_id = request.query_params.get('servant_id')

        #home, hospital
        care_type = request.data.get('care_type')
        is_continuous_time = request.data.get('is_continuous_time')
        name = request.data.get('name')
        #M, F
        gender = request.data.get('gender')
        age = request.data.get('age')
        weight = request.data.get('weight')
        #1,2,4
        disease = request.data.get('disease')
        disease_remark = request.data.get('disease_remark')
        #1,4,6
        body_condition = request.data.get('body_condition')
        conditions_remark = request.data.get('conditions_remark')
        #1,7,9
        service = request.data.get('service')

        road_name = request.data.get('road_name')
        hospital_name = request.data.get('hospital_name')

        emergencycontact_name = request.data.get('emergencycontact_name')
        emergencycontact_relation = request.data.get('emergencycontact_relation')
        emergencycontact_phone = request.data.get('emergencycontact_phone')

        case = Case.objects.get(id=case_id)
        if case.user == user:
            case.county = County.objects.get(id=countyId)
            case.city = case.county.city
            
            if care_type == 'home' and request.data.get('road_name')!=None:
                case.road_name = request.data.get('road_name')
            elif care_type == 'hospital' and request.data.get('hospital_name')!=None:
                case.hospital_name = request.data.get('hospital_name')

            #start_datetime=2022-07-21
            #s = "2014-04-07"
            #datetime.datetime.strptime(s, "%Y-%m-%d").date()
            case.start_datetime = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            case.end_datetime = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            
            # weekday = 1,3,5
            case.weekday = weekday

            case.start_time = int(start_time[0]) + float(int(start_time[1])/60)
            case.end_time = int(end_time[0]) + float(int(end_time[1])/60)
            if name != None:
                case.name = name
            if care_type != None:
                case.care_type = care_type
            if is_continuous_time == 'True' or is_continuous_time == 'true':
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
            if road_name != None:
                case.road_name = road_name
            if hospital_name != None:
                case.hospital_name = hospital_name
            if emergencycontact_name != None:
                case.emergencycontact_name = emergencycontact_name
            if emergencycontact_relation != None:
                case.emergencycontact_relation = emergencycontact_relation
            if emergencycontact_phone != None:
                case.emergencycontact_phone = emergencycontact_phone
            case.save()

            if disease != None and disease != '':
                disease_ids = disease.split(',')
                case_disease_ships = CaseDiseaseShip.objects.filter(case=case)

                for disease_id in disease_ids:
                    if CaseDiseaseShip.objects.filter(case=case,disease=DiseaseCondition.objects.get(id=disease_id)).count() == 0:
                        casediseaseship = CaseDiseaseShip()
                    else:
                        casediseaseship = CaseDiseaseShip.objects.get(case=case,disease=DiseaseCondition.objects.get(id=disease_id))
                    casediseaseship.disease = DiseaseCondition.objects.get(id=disease_id)
                    casediseaseship.case = case
                    casediseaseship.save()
                for case_disease_ship in case_disease_ships:
                    if str(case_disease_ship.disease.id) not in disease_ids:
                        case_disease_ship.delete()
            else:
                CaseDiseaseShip.objects.filter(case=case).delete()

            if body_condition != None and body_condition != '':
                body_condition_ids = body_condition.split(',')
                body_condition_ships = CaseBodyConditionShip.objects.filter(case=case)
                for body_condition_id in body_condition_ids:
                    if CaseBodyConditionShip.objects.filter(case=case,body_condition=BodyCondition.objects.get(id=body_condition_id)).count() == 0:
                        casebodyconditionship = CaseBodyConditionShip()
                    else:
                        casebodyconditionship = CaseBodyConditionShip.objects.get(case=case,body_condition=BodyCondition.objects.get(id=body_condition_id))
                    casebodyconditionship.body_condition = BodyCondition.objects.get(id=body_condition_id)
                    casebodyconditionship.case = case
                    casebodyconditionship.save()
                for body_condition_ship in body_condition_ships:
                    if str(body_condition_ship.body_condition.id) not in disease_ids:
                        body_condition_ship.delete()
            else:
                CaseBodyConditionShip.objects.filter(case=case).delete()

            if service != None and service != '':
                service_ids = service.split(',')
                case_services = CaseServiceShip.objects.filter(case=case)
                for service_id in service_ids:
                    if CaseServiceShip.objects.filter(case=case,service=Service.objects.get(id=service_id)).count() == 0:
                        caseserviceship = CaseServiceShip()
                    else:
                        caseserviceship = CaseServiceShip.objects.get(case=case,service=Service.objects.get(id=service_id))
                    caseserviceship.service = Service.objects.get(id=service_id)
                    caseserviceship.case = case
                    caseserviceship.save()
                for case_service in case_services:
                    if str(case_service.service.id) not in service_ids:
                        case_service.delete()
            else:
                CaseServiceShip.objects.filter(case=case).delete()

            # 這邊要針對個別 servant 產生訂單~ 要有系統訊息, 推播訊息, 並檢查 transferFee, roadName, hospitalName 等新欄位
            if servant_id != None and servant_id != '':

                servant = User.objects.get(id=servant_id)
                
                if Order.objects.filter(case=case,servant=servant).count() != 0:
                    Order.objects.filter(case=case,servant=servant).update(state='canceled')
             
                order = Order()
                order.case = case
                order.user = case.user
                order.servant = servant
                order.state = 'unPaid'
                order.start_datetime = case.start_datetime
                order.end_datetime = case.end_datetime
                order.start_time = order.case.start_time
                order.end_time = order.case.end_time
                order.created_at = datetime.datetime.now()

                if order.case.care_type == 'home':
                    order.that_time_hour_wage = servant.home_hour_wage
                    order.that_time_half_day_wage = servant.home_half_day_wage
                    order.that_time_one_day_wage = servant.home_one_day_wage
                else:
                    order.that_time_hour_wage = servant.hospital_hour_wage
                    order.that_time_half_day_wage = servant.hospital_half_day_wage
                    order.that_time_one_day_wage = servant.hospital_one_day_wage

                order.save()

                if UserServiceLocation.objects.filter(user=order.servant,city=order.case.city).count() != 0:
                    transfer_fee = UserServiceLocation.objects.get(user=order.servant,city=order.case.city).transfer_fee
                    order.transfer_fee = transfer_fee
                else:
                    order.transfer_fee = 0
                
                
                if order.case.is_continuous_time == False:
                    weekdays = order.case.weekday.split(',')
                    for weekday in weekdays:
                        orderWeekday = OrderWeekDay()
                        orderWeekday.order = order
                        orderWeekday.weekday = weekday
                        orderWeekday.save()
                    
                    weekday_list = list(OrderWeekDay.objects.filter(order=order).values_list('weekday', flat=True))

                    days = days_count(weekday_list, order.start_datetime.date(), order.end_datetime.date())
                    number_of_transfer = days
                    total_hours = days * (order.end_time - order.start_time)
                    
                    order.work_hours = total_hours
                    order.number_of_transfer = number_of_transfer
                    order.amount_transfer_fee = transfer_fee * number_of_transfer
                    one_day_work_hours = order.end_time - order.start_time
                    if order.case.care_type == 'home':
                        if one_day_work_hours < 12:
                            wage = order.servant.home_hour_wage
                        elif one_day_work_hours >=12 and one_day_work_hours < 24:
                            wage = round(order.servant.home_half_day_wage/12)
                    elif order.case.care_type == 'hospital':
                        if one_day_work_hours < 12:
                            wage = order.servant.hospital_hour_wage
                        elif one_day_work_hours >=12 and one_day_work_hours < 24:
                            wage = round(order.servant.hospital_half_day_wage/12)
                else:
                    order.number_of_transfer = 1
                    order.amount_transfer_fee = order.transfer_fee * 1
                    # start_time = datetime.datetime.strptime(start_time,"%H:%M")
                    # end_time = datetime.datetime.strptime(end_time,"%H:%M")
                    # start_datetime = datetime.datetime.combine(order.start_datetime.date(),start_time)
                    # end_datetime = datetime.datetime.combine(order.end_datetime.date(),end_time)
                    # diff = end_datetime - start_datetime
                    # days, seconds = diff.days, diff.seconds
                    # hours = days * 24 + seconds // 3600
                    # minutes = (seconds % 3600) // 60
                    total_hours = continuous_time_cal(order)
                    order.work_hours = total_hours
                    if order.case.care_type == 'home':
                        if total_hours < 12:
                            wage = order.servant.home_hour_wage
                        elif total_hours >=12 and total_hours < 24:
                            wage = round(order.servant.home_half_day_wage/12)
                        else:
                            wage = round(order.servant.home_one_day_wage/24)
                    elif order.case.care_type == 'hospital':
                        if total_hours < 12:
                            wage = order.servant.hospital_hour_wage
                        elif total_hours >=12 and total_hours < 24:
                            wage = round(order.servant.hospital_half_day_wage/12)
                        else:
                            wage = round(order.servant.hospital_one_day_wage/24)
                order.wage_hour =wage
                order.base_money = round(order.work_hours * wage)

                # need to change in the future
                order.platform_percent = platform_percent_cal(servant,order)
                order.newebpay_percent = get_newebpay_percent()
                order.save()
                Review.objects.create(order=order,case=order.case,servant=order.servant)
                
                total_increase_money = 0
                if service != None and service != '':
                    for service_id in service_idList:
                        if int(service_id) <= 4:
                            orderIncreaseService = OrderIncreaseService()
                            orderIncreaseService.order = order
                            orderIncreaseService.service = Service.objects.get(id=service_id)
                            if UserServiceShip.objects.filter(user=servant,service=Service.objects.get(id=service_id)).count() > 0:
                                orderIncreaseService.increase_percent = UserServiceShip.objects.get(user=servant,service=Service.objects.get(id=service_id)).increase_percent
                            else:
                                orderIncreaseService.increase_percent = 0
                            orderIncreaseService.increase_money = round((order.base_money) * (orderIncreaseService.increase_percent)/100)
                            orderIncreaseService.save()

                            total_increase_money = total_increase_money + orderIncreaseService.increase_money

                total_service_money =  order.base_money + total_increase_money
                order.total_money = total_service_money + order.amount_transfer_fee

                order.newebpay_money = round(order.total_money * (order.newebpay_percent/100))
                order.platform_money = round(order.total_money * (order.platform_percent/100))

                order.servant_money = order.total_money - order.newebpay_money - order.platform_money
                order.save()

                receiveBooking(servant,order)
                chatroom_ids1 = list(ChatroomUserShip.objects.filter(user=case.user).values_list('chatroom', flat=True))
                chatroom_ids2 = list(ChatroomUserShip.objects.filter(user=servant).values_list('chatroom', flat=True))
                chatroom_set = set(chatroom_ids1).intersection(set(chatroom_ids2))
                print(chatroom_set,1)
                
                if list(chatroom_set) != []:
                    chatroom_id = list(chatroom_set)[0]
                    print(chatroom_id,2)
                    chatroom = ChatRoom.objects.get(id=chatroom_id)
                    message = ChatroomMessage(user=user,case=case,order=order,chatroom=chatroom,is_this_message_only_case=True)
                    message.save()
                elif list(chatroom_set) == []:
                    chatroom = ChatRoom()
                    chatroom.save()
                    ChatroomUserShip.objects.create(user=user,chatroom=chatroom)
                    ChatroomUserShip.objects.create(user=servant,chatroom=chatroom)
                    message = ChatroomMessage(user=user,case=case,chatroom=chatroom,is_this_message_only_case=True)
                    message.save()
                chatroom.update_at = datetime.datetime.now()
                chatroom.save()

            disease_idList = list(CaseDiseaseShip.objects.filter(case=case).values_list('disease', flat=True))
            case.disease = DiseaseCondition.objects.filter(id__in=disease_idList)
            body_condition_idList = list(CaseBodyConditionShip.objects.filter(case=case).values_list('body_condition', flat=True))
            case.body_condition = BodyCondition.objects.filter(id__in=body_condition_idList)
            service_idList = list(CaseServiceShip.objects.filter(case=case).values_list('service', flat=True))
            case.services = Service.objects.filter(id__in=service_idList)

            serializer = self.serializer_class(case)
            return Response(serializer.data)
        else:
            return Response('no auth')

class SmsVerifyViewSet(APIView):

    def get(self, request, format=None):
        from messageApp.tasks import randSmsVerifyCode
        phone= self.request.query_params.get('phone')
        if phone!= None and len(phone) == 10:
            if User.objects.filter(phone=phone).count() ==0:
                code = randSmsVerifyCode(phone)
                return Response({'message': "ok", 'code': code})
            else:
                return Response({'message': "this phone already registered"})
        else:
            return Response({'message': "wrong phone number type"})

class ResetPasswordSmsVerifyViewSet(APIView):

    def get(self, request, format=None):
        from messageApp.tasks import randSmsVerifyCode
        phone= self.request.query_params.get('phone')
        if phone!= None and len(phone) == 10:
            if User.objects.filter(phone=phone).count() !=0:
                code = randSmsVerifyCode(phone)
                return Response({'message': "ok", 'code': code})
            else:
                return Response({'message': "this phone haven't registered"})
        else:
            return Response({'message': "wrong phone number type"})

class ResetPasswordSmsSendPasswordViewSet(APIView):

    def get(self, request, format=None):
        from messageApp.tasks import smsSendPassword
        phone= self.request.query_params.get('phone')
        if phone!= None and len(phone) == 10:
            if User.objects.filter(phone=phone).count() !=0:
                user = User.objects.get(phone=phone)

                password = generatePassword()
                smsSendPassword(phone, password)

                user.set_password(password)
                user.save()
                return Response({'message': "ok"})
            else:
                return Response({'message': "this phone already registered"})
        else:
            return Response({'message': "wrong phone number type"})


# for test in shell
# from api.views import days_count
# import datetime
# weekday_list = [1,3,4,5]
# start = datetime.datetime.strptime('20221128', "%Y%m%d").date()
# end = datetime.datetime.strptime('20221130', "%Y%m%d").date()
# days_count(weekday_list, start, end)
def days_count(weekdays: list, start: date, end: date):
    dates_diff = end-start
    # print(f'days diff {dates_diff}')

    days = 0
    for i in range(dates_diff.days+1):
        day = start + timedelta(days=i)
        # print(day)
        # print(day.weekday())

        dayWeekDay = day.weekday() + 1
        if(dayWeekDay == 7):
            dayWeekDay = 0

        if str(dayWeekDay) in weekdays:
            days = days + 1
    return days

def time_format_change(time_int):
    hour = int(time_int) 
    minute = int((time_int - int(time_int)) * 60)
    if hour < 10:
        if minute < 10:
            return '0'+ str(hour) + ":0" + str(minute)
        else:
            return '0'+ str(hour) + ":" + str(minute)
    else:
        if minute < 10:
            return  str(hour) + ":0" + str(minute)
        else:
            return  str(hour) + ":" + str(minute)

def continuous_time_cal(order):
    # start_time = time_format_change(order.start_time) 
    # end_time = time_format_change(order.end_time) 
    # print('test01',start_time,end_time)
    # start_time = datetime.datetime.strptime(start_time,"%H:%M").time()
    # end_time = datetime.datetime.strptime(end_time,"%H:%M").time()
    # print('test02',start_time,end_time)
    # start_datetime = datetime.datetime.combine(order.start_datetime.date(),start_time)
    # end_datetime = datetime.datetime.combine(order.end_datetime.date(),end_time)
    # diff = end_datetime - start_datetime
    # days, seconds = diff.days, diff.seconds
    # hours = days * 24 + seconds // 3600
    # minutes = (seconds % 3600) // 60
    # total_hours = hours + round(minutes/60,1)

    theStartTime = datetime.datetime(order.start_datetime.year , order.start_datetime.month , order.start_datetime.day , int(order.start_time), int(round(order.start_time % 1,2)*60) )
    theEndTime = datetime.datetime(order.end_datetime.year , order.end_datetime.month , order.end_datetime.day , int(order.end_time), int(round(order.end_time % 1,2)*60) )

    diff = theEndTime - theStartTime
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    total_hours = hours + round(minutes/60,1)

    return total_hours

def platform_percent_cal(servant,order):
    orders = Order.objects.all()
    # today = datetime.datetime.today()
    # current_year = today.year
    # current_month = today.month
    # base_percent = 2.8
    # work_hours = order.work_hours
    # orders_total_hours = work_hours
    orders_total_hours = 0
    if orders.filter(servant=servant, start_datetime__year=order.start_datetime.year, start_datetime__month=order.start_datetime.month , state='paid').count() != 0:
        accumulate_work_hours = orders.filter(servant=servant, start_datetime__year=order.start_datetime.year, start_datetime__month=order.start_datetime.month,state='paid').aggregate(Sum('work_hours'))['work_hours__sum']
        print('accumulate_work_hours',accumulate_work_hours)
        orders_total_hours += accumulate_work_hours
    
    if orders_total_hours < 120:
        return 6.5
    elif orders_total_hours >= 120 and orders_total_hours < 240 :
        return 5.5
    elif orders_total_hours >= 240 and orders_total_hours < 360 :
        return 4.5
    elif orders_total_hours >= 360 :
        return 4

def get_newebpay_percent():
    return 2.8

def generatePassword() :
    # Declare a digits variable 
    # which stores all digits
    digits = "0123456789abcdefghij"
    OTP = ""
 
    # length of password can be changed
    # by changing value in range
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 20)]
    
    # ex.3211
    return OTP