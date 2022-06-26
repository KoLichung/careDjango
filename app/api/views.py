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
from datetime import timedelta , datetime
from modelCore.models import User, MarkupItem, Category, LanguageSkill, License, Servant, ServantMarkupItemPrice, ServantSkillShip,UserLicenseShipImage, ServantLicenseShipImage, ServantCategoryShip, Recipient, ServiceItem, City, CityArea,ServantCityAreaShip, Transportation, Case,OrderState, Order, OrderReview , CaseServiceItemShip 
from api import serializers

class MarkupItemViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = MarkupItem.objects.all()
    serializer_class = serializers.MarkupItemSerializer

class CsrfExemptSessionAuthentication(SessionAuthentication):
    
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class LanguageSkillViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    queryset = LanguageSkill.objects.all()
    serializer_class = serializers.LanguageSkillSerializer

class LicenseViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    queryset = License.objects.all()
    serializer_class = serializers.LicenseSerializer

class ServantRecommendationViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = Servant.objects.all()
    serializer_class = serializers.ServantSerializer
    for i in range(len(queryset)):
        Score_Dict = OrderReview.objects.filter(order__case__servant=queryset[i],servant_is_rated=True).aggregate(avg_rating=Avg('servant_score'))
        queryset[i].score = Score_Dict['avg_rating']
        queryset[i].save()
        print(queryset[i].score)

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

class ServantSkillShipViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = ServantSkillShip.objects.all()
    serializer_class = serializers.ServantSkillShipSerializer

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        languageSkill_id = self.request.GET.get('languageSkill_id')
        queryset = queryset.filter(servant__user=theUser)
        if languageSkill_id != None:
            queryset = queryset.filter(languageSkill=LanguageSkill.objects.get(id=languageSkill_id))
        for i in range(len(queryset)):
            queryset[i].servant_name = queryset[i].servant.user.name
            queryset[i].language_skill_name = queryset[i].languageSkill.name
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

class TransportationViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Transportation.objects.all()
    serializer_class = serializers.TransportationSerializer

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        cityarea_id = self.request.GET.get('cityarea_id')
        queryset = queryset.filter(servant__user=theUser)
        if cityarea_id != None:
            queryset = queryset.filter(cityarea=CityArea.objects.get(id=cityarea_id))
        for i in range(len(queryset)):
            queryset[i].servant_name = queryset[i].servant.user.name
            queryset[i].cityarea_name = queryset[i].cityarea.city + queryset[i].cityarea.area

        return queryset

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
        servant_id = self.request.GET.get('servant_id')
        cityarea_id = self.request.GET.get('cityarea_id')
        if servant_id != None:
            queryset = queryset.filter(servant=Servant.objects.get(id=servant_id))
        
        if cityarea_id != None:
            queryset = queryset.filter(cityarea=CityArea.objects.get(id=cityarea_id))
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
        servantContent = request.data.get('servantContent')
        servantScore = request.data.get('servantScore')
        order = Order.objects.get(case__recipient__user=user)
        orderReview = OrderReview.objects.get(order=order)

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
        userContent = request.data.get('userContent')
        userScore = request.data.get('userScore')
        queryset = self.get_queryset()
        filter = {}
        for field in self.multiple_lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        orderReview = obj

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

