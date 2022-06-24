from unicodedata import category
from httplib2 import Authentication
from rest_framework import viewsets, mixins
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
# Create your views here.
import datetime 
import math
from datetime import timedelta , datetime
from modelCore.models import User, MarkupItem, Category, LanguageSkill, License, Servant, ServantMarkupItemPrice, ServantSkillShip,UserLicenseShipImage, ServantLicenseShipImage, ServantCategoryShip, Recipient, ServiceItem, City, CityArea, Transportation, Case,OrderState, Order, OrderReview , CaseServiceItemShip 
from api import serializers

class MarkupItemViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = MarkupItem.objects.all()
    serializer_class = serializers.MarkupItemSerializer

class CategoryViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

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

class ServantViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):
    queryset = Servant.objects.all()
    serializer_class = serializers.ServantSerializer

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

class PostCaseDetailViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):

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
            if queryset[i].category.care_type == '居家照顧':
                hour_wage = queryset[i].servant.home_hourly_wage
            else:
                hour_wage = queryset[i].servant.hospital_hourly_wage

            working_hours = ((queryset[i].end_time).hour - (queryset[i].start_time).hour) * (((queryset[i].end_date) - (queryset[i].start_date)).days)
            queryset[i].servant_name = queryset[i].servant.user.name
            queryset[i].recipient_name = queryset[i].recipient.name
            queryset[i].recipient_gender = queryset[i].recipient.gender
            queryset[i].recipient_age = queryset[i].recipient.age
            queryset[i].recipient_weight = queryset[i].recipient.weight
            queryset[i].recipient_disease = queryset[i].recipient.disease
            queryset[i].recipient_conditions = queryset[i].recipient.conditions
            queryset[i].recipient_disease_info = queryset[i].recipient.disease_info
            queryset[i].recipient_conditions_info = queryset[i].recipient.conditions_info
            queryset[i].cityarea_name = queryset[i].cityarea.city + queryset[i].cityarea.area
            queryset[i].category_CareType = queryset[i].category.care_type
            queryset[i].category_TimeType = queryset[i].category.time_type
            queryset[i].case_date = str(queryset[i].start_date) + ' ~ ' + str(queryset[i].end_date)
            queryset[i].basic_price =  hour_wage * working_hours
            queryset[i].hour_wage =  hour_wage 
            queryset[i].working_hours =  working_hours 
            queryset[i].markup_Item = queryset[i].markup_item.markup_item
            queryset[i].markup_Item_percent =  str(((queryset[i].markup_item.pricePercent)*100) - 100) + '%'
            queryset[i].markup_price = round(((queryset[i].markup_item.pricePercent)-1) * hour_wage * working_hours)
            queryset[i].total_price = round((queryset[i].markup_item.pricePercent) * hour_wage * working_hours)
            service_Items = CaseServiceItemShip.objects.filter(case=queryset[i])
            All_service_item = []
            for x in range(len(service_Items)):                
                All_service_item.append({'serviceItem':str(service_Items[x].service_item)})
            print(All_service_item)
            
            queryset[i].service_Item =  All_service_item

        return queryset


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

class AddRateViewSet(APIView):
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
            queryset[i].user_name = theUser
            queryset[i].servant_name = queryset[i].order.case.servant.user.name
            queryset[i].recipient_name = queryset[i].order.case.recipient.name
            queryset[i].cityarea_name = queryset[i].order.case.cityarea.city + queryset[i].order.case.cityarea.area
            queryset[i].category_CareType = queryset[i].order.case.category.care_type
            queryset[i].category_TimeType = queryset[i].order.case.category.time_type
            queryset[i].case_date = str(queryset[i].order.case.start_date) + ' ~ ' + str(queryset[i].order.case.end_date)
        
        return queryset

class ServantRateViewSet(viewsets.GenericViewSet,
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

class UserRateViewSet(viewsets.GenericViewSet,
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
        queryset = queryset.filter(servant_is_rated=True)
        

        for i in range(len(queryset)):
            queryset[i].user_name = theUser
            queryset[i].servant_name = queryset[i].order.case.servant.user.name
            queryset[i].cityarea_name = queryset[i].order.case.cityarea.city + queryset[i].order.case.cityarea.area
            queryset[i].category_CareType = queryset[i].order.case.category.care_type
            queryset[i].category_TimeType = queryset[i].order.case.category.time_type
            queryset[i].case_date = str(queryset[i].order.case.start_date) + ' ~ ' + str(queryset[i].order.case.end_date)
        
        return queryset

class BasicInfoViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = serializers.OrderReviewSerializer

    def post(self, request, format=None):
        queryset = self.queryset
        theuser = self.request.user
        phone = request.data.get('phone')
        gender = request.data.get('gender')
        address = request.data.get('address')
        email = request.data.get('email')
        line_id = request.data.get('line_id')
        user = theuser
        if user == theuser:
            user.phone = phone
            user.gender = gender
            user.address = address
            user.email = email
            user.line_id = line_id
            user.save()
            return Response({'message': "ok"})
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
    serializer_class = serializers.OrderReviewSerializer

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

