from calendar import weekday
from unicodedata import category
from unittest import case
from httplib2 import Authentication
from rest_framework import viewsets, mixins
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.db.models import Avg ,Count
# Create your views here.
import datetime 
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
import datetime 
from modelCore.models import User, MarkupItem, Category, License,Weekday, Servant,ServantWeekdayTimeShip, ServantMarkupItemPrice, ServantSkill,UserLicenseShipImage, ServantLicenseShipImage, ServantCategoryShip, Recipient, ServiceItem, City, CityArea,ServantCityAreaShip, Transportation, Case,OrderState, Order, OrderReview , CaseServiceItemShip ,ServantServiceItemShip
from api import serializers

class CreateListModelMixin:

    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CreateListModelMixin, self).get_serializer(*args, **kwargs)
        
class MarkupItemViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = MarkupItem.objects.all()
    serializer_class = serializers.MarkupItemSerializer

class CsrfExemptSessionAuthentication(SessionAuthentication):
    
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class LicenseViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    queryset = License.objects.all()
    serializer_class = serializers.LicenseSerializer

class ServantRecommendationViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = Servant.objects.all()
    serializer_class = serializers.ServantSerializer

        

    def filter_queryset(self, queryset):
        queryset = self.queryset 
        category_id = self.request.GET.get('category_id')
        cityarea_id = self.request.GET.get('cityarea_id')
        sort = self.request.GET.get('sort')
        print(type(sort))
        if category_id != None:
            queryset = queryset.filter(category=Category.objects.get(id=category_id))
        if cityarea_id != None:
            queryset = queryset.filter(cityarea=CityArea.objects.get(id=cityarea_id))
        
        for i in range(len(queryset)):
            Score_Dict = OrderReview.objects.filter(order__case__servant=queryset[i],servant_is_rated=True).aggregate(avg_rating=Avg('servant_score'))
            queryset[i].score = Score_Dict['avg_rating']
            queryset[i].save()
            print(queryset[i].score)
            Num_Dict = OrderReview.objects.filter(order__case__servant=queryset[i],servant_is_rated=True).aggregate(num=Count('servant_score'))
            queryset[i].servant_ratedNum = Num_Dict['num']
            ServantCareTypeList = {}
            servantCategory = ServantCategoryShip.objects.filter(servant=queryset[i])
            for n in range(len(servantCategory)):
                ServantCareTypeList['servantCareType'+str(n+1)] = str(servantCategory[n].category.care_type)
            queryset[i].caregory_type = ServantCareTypeList
            serviceCityList = {}
            serviceCity = ServantCityAreaShip.objects.filter(servant=queryset[i])
            for x in range(len(serviceCity)):  
                serviceCityList['serviceCity'+str(x+1)] = str(serviceCity[x].cityarea.city)
            queryset[i].service_area = serviceCityList
        print(queryset[1].score)
        if sort == 'HighScore':
            return queryset.order_by('-score')
        elif sort == 'LowScore':
            return queryset.order_by('score')
        elif sort == 'HighPrice':
            return queryset.order_by('-home_hourly_wage')
        elif sort == 'LowPrice':
            return queryset.order_by('home_hourly_wage')
        else:
            return queryset

class ServantMarkupItemPriceViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = ServantMarkupItemPrice.objects.all()
    serializer_class = serializers.ServantMarkupItemPriceSerializer

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        markupItem_id = self.request.GET.get('markupItem_id')
        queryset = queryset.filter(servant__user=theUser)
        if markupItem_id != None:
            queryset = queryset.filter(markup_item=MarkupItem.objects.get(id=markupItem_id))
        for i in range(len(queryset)):
            queryset[i].servant_name = queryset[i].servant.user.name
            queryset[i].markup_item_name = queryset[i].markup_item.name
        return queryset



class UserLicenseShipImageViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = UserLicenseShipImage.objects.all()
    serializer_class = serializers.UserLicenseShipImageSerializer

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        license_id = self.request.GET.get('license_id')
        queryset = queryset.filter(user=user)
        if license_id != None:
            queryset = queryset.filter(license=License.objects.get(id=license_id))
        for i in range(len(queryset)):
            queryset[i].user_name = queryset[i].user.name
            queryset[i].license_name = queryset[i].license.name
        return queryset

class ServantLicenseShipImageViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = ServantLicenseShipImage.objects.all()
    serializer_class = serializers.ServantLicenseShipImageSerializer

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        
        license_id = self.request.GET.get('license_id')
        queryset = queryset.filter(servant__user=theUser)
        if license_id != None:
            queryset = queryset.filter(license=License.objects.get(id=license_id))
        for i in range(len(queryset)):
            queryset[i].servant_name = queryset[i].servant.user.name
            queryset[i].license_name = queryset[i].license.name
        return queryset

class ServantCategoryShipViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = ServantCategoryShip.objects.all()
    serializer_class = serializers.ServantCategoryShipSerializer

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        category_id = self.request.GET.get('category_id')
        queryset = queryset.filter(servant__user=theUser)
        if category_id != None:
            queryset = queryset.filter(category=Category.objects.get(id=category_id))
        for i in range(len(queryset)):
            queryset[i].servant_name = queryset[i].servant.user.name
            queryset[i].category_CareType = queryset[i].category.care_type
            queryset[i].category_TimeType = queryset[i].category.time_type

        return queryset

class RecipientViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Recipient.objects.all()
    serializer_class = serializers.RecipientSerializer

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        recipient_name = self.request.GET.get('recipient_name')
        queryset = queryset.filter(user=theUser)
        if recipient_name != None:
            queryset = queryset.filter(name=recipient_name)
        # for i in range(len(queryset)):
        #     queryset[i].user_name = queryset[i].user.name
        return queryset

class ServiceItemViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    queryset = ServiceItem.objects.all()
    serializer_class = serializers.ServiceItemSerializer

class CityViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    queryset = City.objects.all()
    serializer_class = serializers.CitySerializer

class CityAreaViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    queryset = CityArea.objects.all()
    serializer_class = serializers.CityAreaSerializer


class CaseViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Case.objects.all()
    serializer_class = serializers.CaseSerializer

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        queryset = queryset.filter(recipient__user=theUser)
        servant_id = self.request.GET.get('servant_id')
        cityarea_id = self.request.GET.get('cityarea_id')
        if servant_id != None:
            queryset = queryset.filter(servant=Servant.objects.get(id=servant_id))
        
        if cityarea_id != None:
            queryset = queryset.filter(cityarea=CityArea.objects.get(id=cityarea_id))
        for i in range(len(queryset)):
            queryset[i].servant_name = queryset[i].servant.user.name
            queryset[i].recipient_name = queryset[i].recipient.name
            queryset[i].cityarea_name = queryset[i].cityarea.city + queryset[i].cityarea.area

        return queryset

class CaseServiceItemShipViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = CaseServiceItemShip.objects.all()
    serializer_class = serializers.CaseServiceItemShipSerializer

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        queryset = queryset.filter(case__recipient__user=theUser)
        servant_id = self.request.GET.get('servant_id')
        cityarea_id = self.request.GET.get('cityarea_id')
        serviceItem_id = self.request.GET.get('serviceItem_id')
        if servant_id != None:
            queryset = queryset.filter(case__servant=Servant.objects.get(id=servant_id))
        
        if cityarea_id != None:
            queryset = queryset.filter(case__cityarea=CityArea.objects.get(id=cityarea_id))

        if serviceItem_id != None:
            queryset = queryset.filter(service_item=ServiceItem.objects.get(id=serviceItem_id))

        for i in range(len(queryset)):
            queryset[i].servant_name = queryset[i].case.servant.user.name
            queryset[i].recipient_name = queryset[i].case.recipient.name
            queryset[i].serviceItem_name = queryset[i].service_item.name
            queryset[i].cityarea_name = queryset[i].case.cityarea.city + queryset[i].case.cityarea.area
        
        return queryset

class OrderStateViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = OrderState.objects.all()
    serializer_class = serializers.OrderStateSerializer

class OrderViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        queryset = queryset.filter(case__recipient__user=theUser)
        servant_id = self.request.GET.get('servant_id')
        cityarea_id = self.request.GET.get('cityarea_id')
        if servant_id != None:
            queryset = queryset.filter(case__servant=Servant.objects.get(id=servant_id))
        
        if cityarea_id != None:
            queryset = queryset.filter(case__cityarea=CityArea.objects.get(id=cityarea_id))

        for i in range(len(queryset)):
            queryset[i].servant_name = queryset[i].case.servant.user.name
            queryset[i].recipient_name = queryset[i].case.recipient.name
            queryset[i].cityarea_name = queryset[i].case.cityarea.city + queryset[i].case.cityarea.area
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, cashflowState='unPaid')

class OrderReviewViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = OrderReview.objects.all()
    serializer_class = serializers.OrderReviewSerializer

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        queryset = queryset.filter(order__case__recipient__user=theUser)
        servant_id = self.request.GET.get('servant_id')
        cityarea_id = self.request.GET.get('cityarea_id')
        if servant_id != None:
            queryset = queryset.filter(order__case__servant=Servant.objects.get(id=servant_id))
        
        if cityarea_id != None:
            queryset = queryset.filter(order__case__cityarea=CityArea.objects.get(id=cityarea_id))

        for i in range(len(queryset)):
            queryset[i].servant_name = queryset[i].order.case.servant.user.name
            queryset[i].recipient_name = queryset[i].order.case.recipient.name
            queryset[i].cityarea_name = queryset[i].order.case.cityarea.city + queryset[i].order.case.cityarea.area
        
        return queryset


class PostCaseViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Case.objects.all()
    serializer_class = serializers.CaseSerializer
    lookup_url_kwarg = "uid"

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
 
        queryset = queryset.filter(recipient__user=theUser)

        for i in range(len(queryset)):
            queryset[i].servant_name = queryset[i].servant.user.name
            queryset[i].recipient_name = queryset[i].recipient.name
            queryset[i].category_CareType = queryset[i].category.care_type
            queryset[i].category_TimeType = queryset[i].category.time_type
            queryset[i].case_date = str(queryset[i].start_date) + ' ~ ' + str(queryset[i].end_date)

        return queryset
       

    def retrieve(self, request,uid):
        uid = self.kwargs.get(self.lookup_url_kwarg)
        theUser = self.request.user
        case = Case.objects.get(id=uid)
    
        if case.recipient.user == theUser:
            if case.category.care_type == '居家照顧':
                hour_wage = case.servant.home_hourly_wage
            else:
                hour_wage = case.servant.hospital_hourly_wage

            working_hours = ((case.end_time).hour - (case.start_time).hour) * (((case.end_date) - (case.start_date)).days)

            case.quservant_name = case.servant.user.name
            case.recipient_name = case.recipient.name
            case.recipient_gender = case.recipient.gender
            case.recipient_age = case.recipient.age
            case.recipient_weight = case.recipient.weight
            case.recipient_disease = case.recipient.disease
            case.recipient_conditions = case.recipient.conditions
            case.recipient_disease_info = case.recipient.disease_info
            case.recipient_conditions_info = case.recipient.conditions_info
            case.cityarea_name = case.cityarea.city + case.cityarea.area
            case.category_CareType = case.category.care_type
            case.category_TimeType = case.category.time_type
            case.case_date = str(case.start_date) + ' ~ ' + str(case.end_date)
            case.basic_price =  hour_wage * working_hours
            case.hour_wage =  hour_wage 
            case.working_hours =  working_hours 
            case.markup_Item = case.markup_item.markup_item
            case.markup_Item_percent =  str(((case.markup_item.pricePercent)*100) - 100) + '%'
            case.markup_price = round(((case.markup_item.pricePercent)-1) * hour_wage * working_hours)
            case.total_price = round((case.markup_item.pricePercent) * hour_wage * working_hours)
            service_Items = CaseServiceItemShip.objects.filter(case=case)
            All_service_item = {}
            for x in range(len(service_Items)):                
                All_service_item['serviveItem'+str(x+1)] = str(service_Items[x].service_item)
            case.service_Item =  All_service_item

            serializer = self.get_serializer(case)
            return Response(serializer.data)
        else:
            return Response({'message': "have no authority"})
        
class TakeCaseViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Case.objects.all()
    serializer_class = serializers.CaseSerializer
    lookup_url_kwarg = "uid"

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        queryset = queryset.filter(servant__user=theUser)
        
        for i in range(len(queryset)):
            queryset[i].user_name = queryset[i].recipient.user.name
            queryset[i].servant_name = queryset[i].servant.user.name
            queryset[i].recipient_name = queryset[i].recipient.name
            queryset[i].category_CareType = queryset[i].category.care_type
            queryset[i].category_TimeType = queryset[i].category.time_type
            queryset[i].case_date = str(queryset[i].start_date) + ' ~ ' + str(queryset[i].end_date)

        return queryset
    def retrieve(self, request,uid):
        uid = self.kwargs.get(self.lookup_url_kwarg)
        theUser = self.request.user
        case = Case.objects.get(id=uid)
        if case.servant.user == theUser:
            if case.category.care_type == '居家照顧':
                hour_wage = case.servant.home_hourly_wage
            else:
                hour_wage = case.servant.hospital_hourly_wage

            working_hours = ((case.end_time).hour - (case.start_time).hour) * (((case.end_date) - (case.start_date)).days)
            case.user_name = case.recipient.user.name
            case.quservant_name = case.servant.user.name
            case.recipient_name = case.recipient.name
            case.recipient_gender = case.recipient.gender
            case.recipient_age = case.recipient.age
            case.recipient_weight = case.recipient.weight
            case.recipient_disease = case.recipient.disease
            case.recipient_conditions = case.recipient.conditions
            case.recipient_disease_info = case.recipient.disease_info
            case.recipient_conditions_info = case.recipient.conditions_info
            case.cityarea_name = case.cityarea.city + case.cityarea.area
            case.category_CareType = case.category.care_type
            case.category_TimeType = case.category.time_type
            case.case_date = str(case.start_date) + ' ~ ' + str(case.end_date)
            case.basic_price =  hour_wage * working_hours
            case.hour_wage =  hour_wage 
            case.working_hours =  working_hours 
            case.markup_Item = case.markup_item.markup_item
            case.markup_Item_percent =  str(((case.markup_item.pricePercent)*100) - 100) + '%'
            case.markup_price = round(((case.markup_item.pricePercent)-1) * hour_wage * working_hours)
            case.platform_fee = round((case.markup_item.pricePercent) * 0.15 * hour_wage * working_hours)
            case.total_price = round((case.markup_item.pricePercent) *(1-0.15)  * hour_wage * working_hours)
            service_Items = CaseServiceItemShip.objects.filter(case=case)
            All_service_item = {}
            for x in range(len(service_Items)):                
                All_service_item['serviveItem'+str(x+1)] = str(service_Items[x].service_item)
            case.service_Item =  All_service_item

            serializer = self.get_serializer(case)
            return Response(serializer.data)
        else:
            return Response({'message': "have no authority"})

class NotRatedYetViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = OrderReview.objects.all()
    serializer_class = serializers.OrderReviewSerializer

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        queryset = queryset.filter(order__case__recipient__user=theUser)
        queryset = queryset.filter(servant_is_rated=False)
        servant_id = self.request.GET.get('servant_id')
        cityarea_id = self.request.GET.get('cityarea_id')
        if servant_id != None:
            queryset = queryset.filter(order__case__servant=Servant.objects.get(id=servant_id))
        
        if cityarea_id != None:
            queryset = queryset.filter(order__case__cityarea=CityArea.objects.get(id=cityarea_id))

        for i in range(len(queryset)):
            queryset[i].servant_name = queryset[i].order.case.servant.user.name
            queryset[i].recipient_name = queryset[i].order.case.recipient.name
            queryset[i].cityarea_name = queryset[i].order.case.cityarea.city + queryset[i].order.case.cityarea.area
            queryset[i].category_CareType = queryset[i].order.case.category.care_type
            queryset[i].category_TimeType = queryset[i].order.case.category.time_type
            queryset[i].case_date = str(queryset[i].order.case.start_date) + ' ~ ' + str(queryset[i].order.case.end_date)
        
        return queryset

class AddServantRateViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = OrderReview.objects.all()
    serializer_class = serializers.OrderReviewSerializer

    def post(self, request, format=None):
        user = self.request.user
        order_id = request.data.get('order_id')
        servantContent = request.data.get('servantContent')
        servantScore = request.data.get('servantScore')
        orderReview = OrderReview.objects.get(order=order_id)

        if orderReview.order.case.recipient.user == user:
            orderReview.servant_content = servantContent
            orderReview.servant_score = servantScore
            orderReview.servant_is_rated = True
            orderReview.servant_review_createdate = datetime.now()
            orderReview.save()
            return Response({'message': "ok"})
        else:
            return Response({'message': "have no authority"})

class AddUserRateViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = OrderReview.objects.all()
    serializer_class = serializers.OrderReviewSerializer

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.multiple_lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def post(self, request, format=None):
        user = self.request.user
        order_id = request.data.get('order_id')
        userContent = request.data.get('userContent')
        userScore = request.data.get('userScore')
        orderReview = OrderReview.objects.get(order=order_id)

        if orderReview.order.case.servant.user == user:
            orderReview.user_content = userContent
            orderReview.user_score = userScore
            orderReview.user_is_rated = True
            orderReview.user_review_createdate = datetime.now()
            orderReview.save()
            return Response({'message': "ok"})
        else:
            return Response({'message': "have no authority"})

    

class ServantRateViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = OrderReview.objects.all()
    serializer_class = serializers.OrderReviewSerializer
    lookup_url_kwarg = "uid"

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        queryset = queryset.filter(order__case__recipient__user=theUser)
        queryset = queryset.filter(servant_is_rated=True)
        print(theUser)

        for i in range(len(queryset)):
            queryset[i].user_name = theUser
            queryset[i].servant_name = queryset[i].order.case.servant.user.name
            queryset[i].cityarea_name = queryset[i].order.case.cityarea.city + queryset[i].order.case.cityarea.area
            queryset[i].category_CareType = queryset[i].order.case.category.care_type
            queryset[i].category_TimeType = queryset[i].order.case.category.time_type
            queryset[i].case_date = str(queryset[i].order.case.start_date) + ' ~ ' + str(queryset[i].order.case.end_date)
        
        return queryset

    def retrieve(self, request,uid):
        uid = self.kwargs.get(self.lookup_url_kwarg)
        theUser = self.request.user
        orderReview = self.queryset.get(id=uid)
        if orderReview.order.case.recipient.user == theUser:
            orderReview.servant_name = orderReview.order.case.servant.user
            serializer = self.get_serializer(orderReview)
            return Response(serializer.data)
        else:
            return Response({'message': "have no authority"})
    

class UserRateViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = OrderReview.objects.all()
    serializer_class = serializers.OrderReviewSerializer
    lookup_url_kwarg = "uid"
    

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        queryset = queryset.filter(order__case__recipient__user=theUser)
        queryset = queryset.filter(user_is_rated=True)
        

        for i in range(len(queryset)):
            queryset[i].user_name = theUser
            queryset[i].servant_name = queryset[i].order.case.servant.user.name
            queryset[i].cityarea_name = queryset[i].order.case.cityarea.city + queryset[i].order.case.cityarea.area
            queryset[i].category_CareType = queryset[i].order.case.category.care_type
            queryset[i].category_TimeType = queryset[i].order.case.category.time_type
            queryset[i].case_date = str(queryset[i].order.case.start_date) + ' ~ ' + str(queryset[i].order.case.end_date)
        
        return queryset

    def retrieve(self, request,uid):
        uid = self.kwargs.get(self.lookup_url_kwarg)
        theUser = self.request.user
        orderReview = self.queryset.get(id=uid)
        if orderReview.order.case.recipient.user == theUser:
            orderReview.servant_name = orderReview.order.case.servant.user
            serializer = self.get_serializer(orderReview)
            return Response(serializer.data)
        else:
            return Response({'message': "have no authority"})

    


class ChangeBasicInfoViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = serializers.OrderReviewSerializer

    def post(self, request, format=None):
        theuser = self.request.user
        phone = request.data.get('phone')
        gender = request.data.get('gender')
        address = request.data.get('address')
        email = request.data.get('email')
        line_id = request.data.get('line_id')
        image = request.data.get('image')
        user = theuser
        if user == theuser:
            user.phone = phone
            user.gender = gender
            user.address = address
            user.email = email
            user.line_id = line_id
            user.image = image
            user.save()
            return Response({'message': "ok"})
        else:
            return Response({'message': "have no authority"})

class MyDocumentViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = UserLicenseShipImage.objects.all()
    serializer_class = serializers.UserLicenseShipImageSerializer

    def post(self, request, format=None):
        queryset = self.queryset
        theuser = self.request.user
        queryset = queryset.filter(user=theuser)
        ID_card_front = request.data.get('ID_card_front')
        ID_card_back = request.data.get('ID_card_back')
        health_ID_card = request.data.get('health_ID_card')

        queryset_front = queryset.get(license=License.objects.get(id=1))
        queryset_back = queryset.get(license=License.objects.get(id=2))
        queryset_health = queryset.get(license=License.objects.get(id=3))

        if queryset_front.user == theuser:
            queryset_front.image = ID_card_front
            queryset_front.save()
            queryset_back.image = ID_card_back
            queryset_back.save()
            queryset_health.image = health_ID_card
            queryset_health.save()
            return Response({'message': "ok"})

            
        else:
            return Response({'message': "have no authority"})

class ServiceSettings(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ServantSerializer
    # 性別 gender : M
    # 服務時段  monday : True , monday_startTime : 11:30 , monday_endTime : 21:30
    # 語言 Chinese : True
    # 服務類型 hospital_care : True , hospital_hourly_wage : 300
    # 服務地區 add_region_num：1 , city_1 : 基隆市 , area_1 : 全區 , transportation_1 : 200
    # 服務項目 service_item_id_1 : 協助進食
    def post(self,request):
        theUser = self.request.user
        theServant = Servant.objects.get(user=theUser)
        gender = request.data.get('gender')
        
        all_time = request.data.get('all_time')
        monday = request.data.get('monday')
        monday_startTime = request.data.get('monday_startTime')
        monday_endTime = request.data.get('monday_endTime')
        tuesday = request.data.get('tuesday')
        tuesday_startTime = request.data.get('tuesday_startTime')
        tuesday_endTime = request.data.get('tuesday_endTime')
        wednesday = request.data.get('wednesday')
        wednesday_startTime = request.data.get('wednesday_startTime')
        wednesday_endTime = request.data.get('wednesday_endTime')
        thursday = request.data.get('thursday')
        thursday_startTime = request.data.get('thursday_startTime')
        thursday_endTime = request.data.get('thursday_endTime')
        friday = request.data.get('friday')
        friday_startTime = request.data.get('friday_startTime')
        friday_endTime = request.data.get('friday_endTime')
        saturday = request.data.get('saturday')
        saturday_startTime = request.data.get('saturday_startTime')
        saturday_endTime = request.data.get('saturday_endTime')
        sunday = request.data.get('sunday')
        sunday_startTime = request.data.get('sunday_startTime')
        sunday_endTime = request.data.get('sunday_endTime')

        Chinese = request.data.get('Chinese')
        Taiwanese = request.data.get('Taiwanese')
        Hakka = request.data.get('Hakka')
        Cantonese = request.data.get('Cantonese')
        Aboriginal = request.data.get('Aboriginal')
        Aboriginal_Type = request.data.get('Aboriginal_Type')
        Japanese = request.data.get('Japanese')
        English = request.data.get('English')
        other= request.data.get('other')
        other_Language = request.data.get('other_Language')
        home_care = request.data.get('home_care')
        hospital_care = request.data.get('hospital_care')
        home_hourly_wage = request.data.get('home_hourly_wage')
        home_halfday_wage = request.data.get('home_halfday_wage')
        home_oneday_wage = request.data.get('home_oneday_wage')
        hospital_hourly_wage = request.data.get('hospital_hourly_wage')
        hospital_halfday_wage = request.data.get('hospital_halfday_wage')
        hospital_oneday_wage = request.data.get('hospital_oneday_wage')
        add_region_num = request.data.get('add_region_num')
        service_item_num = ServiceItem.objects.all().count()
        
        theServant.gender = gender

        if all_time  == 'True' :
            timeship = ServantWeekdayTimeShip()
            timeship.servant = theServant
            timeship.weekday = Weekday.objects.get(name='7')
            timeship.start_time = datetime.time(0,0,0)
            timeship.end_time = datetime.time(23,59,59)
            timeship.save()
        else:
            if monday == 'True' :
                if ServantWeekdayTimeShip.objects.filter(servant=theServant,weekday=Weekday.objects.get(name='1')).exists() != True:
                    timeship = ServantWeekdayTimeShip()
                    
                else:
                    timeship = ServantWeekdayTimeShip.objects.get(servant=theServant,weekday=Weekday.objects.get(name='1'))
                timeship.servant = theServant
                timeship.weekday = Weekday.objects.get(name='1')
                timeship.start_time = datetime.time(int(monday_startTime.split(':')[0]),int(monday_startTime.split(':')[1]))
                timeship.end_time = datetime.time(int(monday_endTime.split(':')[0]),int(monday_endTime.split(':')[1]))
                timeship.save()

            if tuesday == 'True' :
                if ServantWeekdayTimeShip.objects.filter(servant=theServant,weekday=Weekday.objects.get(name='2')).exists() != True:
                    timeship = ServantWeekdayTimeShip()
                    
                else:
                    timeship = ServantWeekdayTimeShip.objects.get(servant=theServant,weekday=Weekday.objects.get(name='2'))
                timeship.servant = theServant
                timeship.weekday = Weekday.objects.get(name='2')
                timeship.start_time = datetime.time(int(tuesday_startTime.split(':')[0]),int(tuesday_startTime.split(':')[1]))
                timeship.end_time = datetime.time(int(tuesday_endTime.split(':')[0]),int(tuesday_endTime.split(':')[1]))
                timeship.save()
                
            if wednesday == 'True' :
                if ServantWeekdayTimeShip.objects.filter(servant=theServant,weekday=Weekday.objects.get(name='3')).exists() != True:
                    timeship = ServantWeekdayTimeShip()
                    
                else:
                    timeship = ServantWeekdayTimeShip.objects.get(servant=theServant,weekday=Weekday.objects.get(name='3'))
                timeship.servant = theServant
                timeship.weekday = Weekday.objects.get(name='3')
                timeship.start_time = datetime.time(int(wednesday_startTime.split(':')[0]),int(wednesday_startTime.split(':')[1]))
                timeship.end_time = datetime.time(int(wednesday_endTime.split(':')[0]),int(wednesday_endTime.split(':')[1]))
                timeship.save()
            if thursday == 'True' :
                if ServantWeekdayTimeShip.objects.filter(servant=theServant,weekday=Weekday.objects.get(name='4')).exists() != True:
                    timeship = ServantWeekdayTimeShip()
                    
                else:
                    timeship = ServantWeekdayTimeShip.objects.get(servant=theServant,weekday=Weekday.objects.get(name='4'))
                timeship.servant = theServant
                timeship.weekday = Weekday.objects.get(name='4')
                timeship.start_time = datetime.time(int(thursday_startTime.split(':')[0]),int(thursday_startTime.split(':')[1]))
                timeship.end_time = datetime.time(int(thursday_endTime.split(':')[0]),int(thursday_endTime.split(':')[1]))
                timeship.save()
            if friday == 'True' :
                if ServantWeekdayTimeShip.objects.filter(servant=theServant,weekday=Weekday.objects.get(name='5')).exists() != True:
                    timeship = ServantWeekdayTimeShip()
                    
                else:
                    timeship = ServantWeekdayTimeShip.objects.get(servant=theServant,weekday=Weekday.objects.get(name='5'))
                timeship.servant = theServant
                timeship.weekday = Weekday.objects.get(name='5')
                timeship.start_time = datetime.time(int(friday_startTime.split(':')[0]),int(friday_startTime.split(':')[1]))
                timeship.end_time = datetime.time(int(friday_endTime.split(':')[0]),int(friday_endTime.split(':')[1]))
                timeship.save()
            if saturday == 'True' :
                if ServantWeekdayTimeShip.objects.filter(servant=theServant,weekday=Weekday.objects.get(name='6')).exists() != True:
                    timeship = ServantWeekdayTimeShip()
                    
                else:
                    timeship = ServantWeekdayTimeShip.objects.get(servant=theServant,weekday=Weekday.objects.get(name='6'))
                timeship.servant = theServant
                timeship.weekday = Weekday.objects.get(name='6')
                timeship.start_time = datetime.time(int(saturday_startTime.split(':')[0]),int(saturday_startTime.split(':')[1]))
                timeship.end_time = datetime.time(int(saturday_endTime.split(':')[0]),int(saturday_endTime.split(':')[1]))
                timeship.save()
            if sunday == True :
                if ServantWeekdayTimeShip.objects.filter(servant=theServant,weekday=Weekday.objects.get(name='0')).exists() != True:
                    timeship = ServantWeekdayTimeShip()
                    
                else:
                    timeship = ServantWeekdayTimeShip.objects.get(servant=theServant,weekday=Weekday.objects.get(name='0'))
                timeship.servant = theServant
                timeship.weekday = Weekday.objects.get(name='0')
                timeship.start_time = datetime.time(int(sunday_startTime.split(':')[0]),int(sunday_startTime.split(':')[1]))
                timeship.end_time = datetime.time(int(sunday_endTime.split(':')[0]),int(sunday_endTime.split(':')[1]))
                timeship.save()

        if (Chinese == 'True') and (ServantSkill.objects.filter(servant=theServant,languageSkill='國語').exists() == False):
            servantskill = ServantSkill()
            servantskill.servant = theServant
            servantskill.languageSkill = '國語'
            servantskill.save()

        if (Taiwanese == 'True')and (ServantSkill.objects.filter(servant=theServant,languageSkill='台語').exists() == False):
            servantskill = ServantSkill()
            servantskill.servant = theServant
            servantskill.languageSkill = '台語'
            servantskill.save()

        if (Hakka == 'True')and (ServantSkill.objects.filter(servant=theServant,languageSkill='客家話').exists() == False):
            servantskill = ServantSkill()
            servantskill.servant = theServant
            servantskill.languageSkill = '客家話'
            servantskill.save()

        if (Cantonese == 'True')and (ServantSkill.objects.filter(servant=theServant,languageSkill='粵語').exists() == False):
            servantskill = ServantSkill()
            servantskill.servant = theServant
            servantskill.languageSkill = '粵語'
            servantskill.save()

        if (Aboriginal == 'True')and (ServantSkill.objects.filter(servant=theServant,languageSkill=Aboriginal_Type).exists() == False):
            servantskill = ServantSkill()
            servantskill.servant = theServant
            servantskill.languageSkill = Aboriginal_Type
            servantskill.save()

        if (Japanese == 'True') and (ServantSkill.objects.filter(servant=theServant,languageSkill='日文').exists() == False):
            servantskill = ServantSkill()
            servantskill.servant = theServant
            servantskill.languageSkill = '日文'
            servantskill.save()

        if (English == 'True') and (ServantSkill.objects.filter(servant=theServant,languageSkill='英文').exists() == False):
            servantskill = ServantSkill()
            servantskill.servant = theServant
            servantskill.languageSkill = '英文'
            servantskill.save()

        if (other == 'True') and (ServantSkill.objects.filter(servant=theServant,languageSkill=other_Language).exists() == False):
            servantskill = ServantSkill()
            servantskill.servant = theServant
            servantskill.languageSkill = other_Language
            servantskill.save()

        if home_care == 'True':
            if all_time == 'True':
                if ServantCategoryShip.objects.get(servant=theServant,category=Category.objects.get(id=1)) != None:
                    pass
                else:
                    servantCategoryship = ServantCategoryShip()
                    servantCategoryship.servant = theServant
                    servantCategoryship.category = Category.objects.get(id=1)
                    servantCategoryship.save()

                theServant.home_hourly_wage = home_hourly_wage
                theServant.home_halfday_wage = home_halfday_wage
                theServant.home_oneday_wage = home_oneday_wage
            else:
                if ServantCategoryShip.objects.get(servant=theServant,category=Category.objects.get(id=2)) != None:
                     pass
                else:
                    servantCategoryship = ServantCategoryShip()
                    servantCategoryship.servant = theServant
                    servantCategoryship.category = Category.objects.get(id=2)
                    servantCategoryship.save()

                theServant.home_hourly_wage = home_hourly_wage
                theServant.home_halfday_wage = home_halfday_wage
                theServant.home_oneday_wage = home_oneday_wage

        if hospital_care == 'True':
            if all_time == 'True':
                if ServantCategoryShip.objects.get(servant=theServant,category=Category.objects.get(id=3)) != None:
                    pass
                else:
                    servantCategoryship = ServantCategoryShip()
                    servantCategoryship.servant = theServant
                    servantCategoryship.category = Category.objects.get(id=3)
                    servantCategoryship.save()

                theServant.hospital_hourly_wage = hospital_hourly_wage
                theServant.hospital_halfday_wage = hospital_halfday_wage
                theServant.hospital_oneday_wage = hospital_oneday_wage
            else:
                if ServantCategoryShip.objects.get(servant=theServant,category=Category.objects.get(id=4)) != None:
                     pass
                else:
                    servantCategoryship = ServantCategoryShip()
                    servantCategoryship.servant = theServant
                    servantCategoryship.category = Category.objects.get(id=4)
                    servantCategoryship.save()

                theServant.hospital_hourly_wage = hospital_hourly_wage
                theServant.hospital_halfday_wage = hospital_halfday_wage
                theServant.hospital_oneday_wage = hospital_oneday_wage

        cityArealist = []
        transportation_dict = {}
        for i in range(int(add_region_num)):
            cityArealist.append({'city':request.data.get('city_'+str(i+1)),'area':request.data.get('area_'+str(i+1)),'transportation':request.data.get('transportation_'+str(i+1))})
            if  ServantCityAreaShip.objects.filter(servant=theServant,cityarea=CityArea.objects.get(city=cityArealist[i]['city'],area=cityArealist[i]['area'])).exists() == False:
               servantCityAreaShip = ServantCityAreaShip()
            else:
                servantCityAreaShip = ServantCityAreaShip.objects.get(servant=theServant,cityarea=CityArea.objects.get(city=cityArealist[i]['city'],area=cityArealist[i]['area']))
            servantCityAreaShip.servant = theServant
            servantCityAreaShip.cityarea = CityArea.objects.get(city=cityArealist[i]['city'],area=cityArealist[i]['area'])
            servantCityAreaShip.save()
            transportation = Transportation()
            transportation.servantCityArea = servantCityAreaShip
            transportation.price = int(cityArealist[i]['transportation'])
            transportation.save()

        service_item_list = []
        service_item_count = 0
        for i in range(service_item_num):
            if request.data.get('service_item_'+str(i+1))  != None:
                service_item_count += 1
        print(service_item_count)
        for n in range(service_item_count):
            service_item_list.append({'service_item':request.data.get('service_item_'+str(n+1))}) 
            if  ServantServiceItemShip.objects.filter(servant=theServant,service_item=ServiceItem.objects.get(name=service_item_list[n]['service_item'])).exists() == False:
                servantItemShip = ServantServiceItemShip()
            else:
                servantItemShip = ServantServiceItemShip.objects.get(servant=theServant,service_item=ServiceItem.objects.get(name=service_item_list[n]['service_item']))

            servantItemShip.servant = theServant
            servantItemShip.service_item = ServiceItem.objects.get(name=service_item_list[n]['service_item'])
            servantItemShip.save()


        service_time_dict={}
        service_time = ServantWeekdayTimeShip.objects.filter(servant=theServant)
        
        if service_time.filter(weekday=Weekday.objects.get(id=8)).exists() == True :
            print('all')
            service_time_dict['服務時段'] = '任何時段皆可'
        else:
            if service_time.filter(weekday=Weekday.objects.get(id=2)).exists() == True :
                service_time_dict['monday'] = '時段：' + str(service_time.get(weekday=Weekday.objects.get(id=2)).start_time) + '~' + str(service_time.get(weekday=Weekday.objects.get(id=2)).end_time)
            if service_time.filter(weekday=Weekday.objects.get(id=3)).exists() == True :
                service_time_dict['tuesday'] = '時段：' + str(service_time.get(weekday=Weekday.objects.get(id=3)).start_time) + '~' + str(service_time.get(weekday=Weekday.objects.get(id=3)).end_time)
            if service_time.filter(weekday=Weekday.objects.get(id=4)).exists() == True :
                service_time_dict['wednesday'] = '時段：' + str(service_time.get(weekday=Weekday.objects.get(id=4)).start_time) + '~' + str(service_time.get(weekday=Weekday.objects.get(id=4)).end_time)
            if service_time.filter(weekday=Weekday.objects.get(id=5)).exists() == True :
                service_time_dict['thursday'] = '時段：' + str(service_time.get(weekday=Weekday.objects.get(id=5)).start_time) + '~' + str(service_time.get(weekday=Weekday.objects.get(id=5)).end_time)
            if service_time.filter(weekday=Weekday.objects.get(id=6)).exists() == True :
                service_time_dict['friday'] = '時段：' + str(service_time.get(weekday=Weekday.objects.get(id=6)).start_time) + '~' + str(service_time.get(weekday=Weekday.objects.get(id=6)).end_time)
            if service_time.filter(weekday=Weekday.objects.get(id=7)).exists() == True :
                service_time_dict['saturday'] = '時段：' + str(service_time.get(weekday=Weekday.objects.get(id=7)).start_time) + '~' + str(service_time.get(weekday=Weekday.objects.get(id=7)).end_time)
            if service_time.filter(weekday=Weekday.objects.get(id=1)).exists() == True :
                service_time_dict['sunday'] = '時段：' + str(service_time.get(weekday=Weekday.objects.get(id=1)).start_time) + '~' + str(service_time.get(weekday=Weekday.objects.get(id=1)).end_time)
        theServant.serviceTime = service_time_dict

        servant_skill_dict={}
        theServantSkill = ServantSkill.objects.filter(servant=theServant)
        for x in range(len(theServantSkill)):
            servant_skill_dict['servant_skill'+str(x+1)] = theServantSkill[x].languageSkill
        theServant.servant_skill = servant_skill_dict

        transportation_list = []
        transportation = Transportation.objects.filter(servantCityArea__servant=theServant)
        for x in range(len(transportation)):
            transportation_list.append({'city':transportation[x].servantCityArea.cityarea.city,'area':transportation[x].servantCityArea.cityarea.area,'transportation':transportation[x].price})
            transportation_dict[str(x+1)] = transportation_list[x]
        theServant.transportation = transportation_dict

        service_Item_dict = {}
        service_item = ServantServiceItemShip.objects.filter(servant=theServant)
        for x in range(len(service_item)):
            service_Item_dict['service_item'+str(x+1)] = service_item[x].service_item.name
        theServant.service_item = service_Item_dict


        serializer = self.serializer_class(theServant)
        return Response(serializer.data)
