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
                    mixins.CreateModelMixin):
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





#http://localhost:8000/api/products/?suppervision_office_id=1&category_id=2
