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
from user.serializers import UserSerializer

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
    # lookup_url_kwarg = "pk"

    # def retrieve(self, request,pk):
    #     pk = self.kwargs.get(self.lookup_url_kwarg)
    #     case = Case.objects.get(id=pk)
    #     serializer = self.get_serializer(case)
    #     return Response(serializer.data)

    # def perform_update(self, serializer):
    #     serializer.save()

    # def perform_create(self, serializer):
    #     serializer.save()
 
class CasePostViewSet(APIView):
        queryset = Case.objects.all()
        serializer_class = serializers.CaseSerializer

        def post(self,request):
            case = Case()
            case.user = User.objects.get(id=(request.data.get('user_id')))
            case.servant = User.objects.get(id=(request.data.get('servant_id')))
            case.county = County.objects.get(id=(request.data.get('county_id')))
            case.care_type = (request.data.get('care_type'))
            case.name = request.data.get('name')
            case.gender = request.data.get('gender')
            case.age = int(request.data.get('age'))
            case.weight = int(request.data.get('weight'))
            case.disease_remark = request.data.get('disease_remark')
            case.conditions_remark = request.data.get('conditions_remark')
            case.is_alltime_service = eval(request.data.get('is_alltime_service'))
            case.is_taken = eval(request.data.get('is_taken'))
            case.is_open_for_search = eval(request.data.get('is_open_for_search'))
            case.start_datetime = datetime.datetime(int(request.data.get('start_datetime').split(',')[0]),int(request.data.get('start_datetime').split(',')[1]),int(request.data.get('start_datetime').split(',')[2])).replace(tzinfo=pytz.UTC)
            case.end_datetime = datetime.datetime(int(request.data.get('end_datetime').split(',')[0]),int(request.data.get('end_datetime').split(',')[1]),int(request.data.get('end_datetime').split(',')[2])).replace(tzinfo=pytz.UTC)
            case.save()
            serializer = self.serializer_class(case)
            return Response(serializer.data)

class OrderViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    lookup_url_kwarg = "pk"

    def retrieve(self, request,pk):
        pk = self.kwargs.get(self.lookup_url_kwarg)
        order = Order.objects.get(id=pk)
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def perform_create(self, serializer):
        serializer.save()

class UserServiceLocationViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin):
    queryset = UserServiceLocation.objects.all()
    serializer_class = serializers.UserServiceLocationSerializer
    lookup_url_kwarg = "pk"

    def retrieve(self, request,pk):
        pk = self.kwargs.get(self.lookup_url_kwarg)
        userServiceLocation = UserServiceLocation.objects.get(id=pk)
        serializer = self.get_serializer(userServiceLocation)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def perform_create(self, serializer):
        serializer.save()

class CaseWeekDayTimeViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin):
    queryset = CaseWeekDayTime.objects.all()
    serializer_class = serializers.CaseWeekDayTimeSerializer
    lookup_url_kwarg = "pk"

    def retrieve(self, request,pk):
        pk = self.kwargs.get(self.lookup_url_kwarg)
        caseWeekDayTime = CaseWeekDayTime.objects.get(id=pk)
        serializer = self.get_serializer(caseWeekDayTime)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def perform_create(self, serializer):
        serializer.save()

class UserWeekDayTimeViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin):
    queryset = UserWeekDayTime.objects.all()
    serializer_class = serializers.UserWeekDayTimeSerializer
    lookup_url_kwarg = "pk"

    def retrieve(self, request,pk):
        pk = self.kwargs.get(self.lookup_url_kwarg)
        userWeekDayTime = UserWeekDayTime.objects.get(id=pk)
        serializer = self.get_serializer(userWeekDayTime)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def perform_create(self, serializer):
        serializer.save()

class MessageViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer

    def perform_create(self, serializer):
        serializer.save()

class SystemMessageViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = SystemMessage.objects.all()
    serializer_class = serializers.SystemMessageSerializer

    def perform_create(self, serializer):
        serializer.save()

class SearchServantView(APIView):

    def get(self, request, format=None):
        #home, hospital
        care_type= self.request.query_params.get('care_type')
        city = self.request.query_params.get('city')
        county = self.request.query_params.get('county')
        is_alltime_service = self.request.query_params.get('is_alltime_service')
        #2022-07-10T00:00:00Z
        start_datetime = self.request.query_params.get('start_datetime')
        end_datetime = self.request.query_params.get('end_datetime')
        #1,3,5
        weekdays = self.request.query_params.get('weekdays')
        #0800:2200
        start_end_time = self.request.query_params.get('start_end_time')

        servants = User.objects.filter(is_servant=True)
        serializer = UserSerializer(servants, many=True)
        return Response(serializer.data)