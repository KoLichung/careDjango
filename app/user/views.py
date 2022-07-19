from modelCore.models import UserWeekDayTime ,Language ,UserLanguage ,County, UserServiceLocation ,Service ,UserServiceShip ,License ,UserLicenseShipImage
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import viewsets, mixins

from user.serializers import UserSerializer, AuthTokenSerializer, UpdateUserSerializer ,GetUserSerializer
from api import serializers

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(user=self.request.user)
        return user

#http://localhost:8000/api/user/token/  要用 post, 並帶參數
class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

#http://localhost:8000/api/user/me/  要有 token
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UpdateUserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user"""
        if self.request.user.line_id != None and self.request.user.line_id != '':
            self.request.user.is_gotten_line_id = True

        return self.request.user

class UpdateUserLineIdView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)

    def put(self, request, format=None):
        try:
            # print(self.request.user)
            # print(self.request.data.get('line_id'))
            user = self.request.user
            user.line_id = self.request.data.get('line_id')
            user.save()
            return Response({'message': 'success update!'})
        except Exception as e:
            raise APIException("wrong token or null line_id")

class UpdateUserPassword(APIView):
    authentication_classes = (authentication.TokenAuthentication,)

    def put(self, request, format=None):
        user = self.request.user
        old_password = self.request.data.get('old_password')

        if user.check_password(old_password):
            new_password = self.request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response({'message': 'success update!'})
        else:
            raise APIException("wrong old password")

class UpdateATMInfo(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, format=None):
        user = self.request.user
        user.ATMInfoBankCode = request.data.get('ATMInfoBankCode')
        user.ATMInfoBranchBankCode = request.data.get('ATMInfoBranchBankCode')
        user.ATMInfoAccount = request.data.get('ATMInfoAccount')
        user.save()
        serializer = GetUserSerializer(user)
        return Response(serializer.data)

class UpdateUserWeekDayTime(generics.UpdateAPIView):
    queryset = UserWeekDayTime.objects.all()
    serializer_class = serializers.UserWeekDayTimeSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.queryset
        weekday = request.data.get('weekday')
        weektime = request.data.get('weektime')
        if weekday != None:
            weekday_ids = weekday.split(',')
            weektime_list = weektime.split(',')
            for i in range(len(weekday_ids)):
                if queryset.filter(user=user,weekday=weekday_ids[i]).exists() != True:
                    userweekdaytime = UserWeekDayTime()
                else:
                    userweekdaytime = queryset.get(user=user,weekday=weekday_ids[i])
                start_time = int(weektime_list[i].split(':')[0][:2]) + float(int(weektime_list[i].split(':')[0][2:])/60)
                end_time = int(weektime_list[i].split(':')[1][:2]) + float(int(weektime_list[i].split(':')[1][2:])/60)
                userweekdaytime.user = user
                userweekdaytime.weekday = weekday_ids[i]
                userweekdaytime.start_time = start_time
                userweekdaytime.end_time = end_time
                userweekdaytime.save()
            for userweekdaytime in queryset.filter(user=user):
                if userweekdaytime.weekday not in weekday_ids:
                    userweekdaytime.delete()
        queryset = queryset.filter(user=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class UpdateUserLanguage(generics.UpdateAPIView):
    queryset = UserLanguage.objects.all()
    serializer_class = serializers.LangaugeSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.queryset
        language = request.data.get('language')
        remark_original = request.data.get('remark_original')
        remark_others = request.data.get('remark_others')
        if language != None:
            language_ids = language.split(',')
            for language_id in language_ids:
                if queryset.filter(user=user,language=language_id).exists() != True:
                    UserLanguage.objects.create(user=user,language=Language.objects.get(id=language_id))
            if '5' in language_ids :
                if remark_original != None:
                    userlanguage = UserLanguage.objects.get(user=user,language=Language.objects.get(id=5))
                    userlanguage.remark = remark_original
                    userlanguage.save()
            if '8' in language_ids :
                if remark_others != None:
                    userlanguage = UserLanguage.objects.get(user=user,language=Language.objects.get(id=8))
                    userlanguage.remark = remark_others
                    userlanguage.save()
            for userlanguage in queryset.filter(user=user):
                if str(userlanguage.language.id) not in language_ids:
                    userlanguage.delete()
                    
        language_list = list(UserLanguage.objects.filter(user=user).values_list('language', flat=True))
        langueges = Language.objects.filter(id__in=language_list)
        serializer = self.get_serializer(langueges,many=True)
        return Response(serializer.data)

class UpdateUserCareType(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, format=None):
        user = self.request.user
        is_home = eval(request.data.get('is_home'))
        is_hospital = eval(request.data.get('is_hospital'))
        home_wage = request.data.get('home_wage')
        hospital_wage = request.data.get('hospital_wage')
        if is_home == True:
            user.is_home = True 
        elif is_home == False: 
            user.is_home = False
        if home_wage != None:
            home_wage = home_wage.split(',')
            user.home_hour_wage = int(home_wage[0])
            user.home_half_day_wage = int(home_wage[1])
            user.home_one_day_wage = int(home_wage[2])
        if is_hospital == True:
            user.is_hospital = True 
        elif is_hospital == False: 
            user.is_hospital = False
        if hospital_wage != None:
            hospital_wage = hospital_wage.split(',')
            user.hospital_hour_wage = hospital_wage[0]
            user.hospital_half_day_wage = hospital_wage[1]
            user.hospital_one_day_wage = hospital_wage[2]
        user.save()
        serializer = GetUserSerializer(user)
        return Response(serializer.data)

class UpdateUserLocations(generics.UpdateAPIView):
    queryset = UserServiceLocation.objects.all()
    serializer_class = serializers.UserServiceLocationSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.queryset
        locations = request.data.get('locations')
        tranfer_fee = request.data.get('tranfer_fee')
        if locations != None:
            location_ids = locations.split(',')
            tranfer_fee_list = tranfer_fee.split(',')
            for i in range(len(location_ids)):
                if queryset.filter(user=user,county=location_ids[i]).exists() != True:
                    userservicelocation = UserServiceLocation()
                else:
                    userservicelocation = queryset.get(user=user,county=location_ids[i])
                userservicelocation.user = user
                userservicelocation.city = County.objects.get(id=location_ids[i]).city
                userservicelocation.county = County.objects.get(id=location_ids[i])
                userservicelocation.tranfer_fee = tranfer_fee_list[i]
                userservicelocation.save()
            for userservicelocation in queryset.filter(user=user):
                if str(userservicelocation.county.id) not in location_ids:
                    userservicelocation.delete()
        queryset = queryset.filter(user=user)
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)

class UpdateUserService(generics.UpdateAPIView):
    queryset = UserServiceShip.objects.all()
    serializer_class = serializers.ServiceSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.queryset
        services = request.data.get('services')
        increase_prices = request.data.get('increase_prices')
        if services != None:
            service_ids = services.split(',')
            increase_price_list = increase_prices.split(',')
            for i in range(len(service_ids)):
                if queryset.filter(user=user,service=service_ids[i]).exists() != True:
                    userserviceship = UserServiceShip()
                else:
                    userserviceship = queryset.get(user=user,service=service_ids[i])
                userserviceship.user = user
                userserviceship.service = Service.objects.get(id=service_ids[i])
                if int(service_ids[i]) < 5 :
                    userserviceship.increase_percent = increase_price_list[i]
                userserviceship.save()
            for userserviceship in queryset.filter(user=user):
                if str(userserviceship.service.id) not in service_ids:
                    userserviceship.delete()
        service_list = list(UserServiceShip.objects.filter(user=user).values_list('service', flat=True))
        services = Service.objects.filter(id__in=service_list)
        for i in range(len(services)):
            if queryset.get(user=user,service=services[i]).increase_percent > 0:
                services[i].increase_percent = queryset.get(user=user,service=services[i]).increase_percent
        serializer = self.get_serializer(services,many=True)
        return Response(serializer.data)

class UpdateUserLicenseImage(viewsets.GenericViewSet,
                            generics.UpdateAPIView,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    queryset = UserLicenseShipImage.objects.all()
    serializer_class = serializers.LicenseSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.queryset
        license = request.data.get('licence_id')
        image = request.data.get('image')
        if license != None:
            if queryset.filter(user=user,license=license).exists() != True:
                userlicenseimage = UserLicenseShipImage()
            else:
                userlicenseimage = queryset.get(user=user,license=license)
            userlicenseimage.user = user
            userlicenseimage.license = License.objects.get(id=license)
            userlicenseimage.image = image
            userlicenseimage.save()
        license_list = list(UserLicenseShipImage.objects.filter(user=user).values_list('license', flat=True))
        licences = License.objects.filter(id__in=license_list)
        serializer = self.get_serializer(licences,many=True)
        return Response(serializer.data)

class UpdateUserInfoImage(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, format=None):
        user = self.request.user
        about_me = request.data.get('about_me')
        background_image = request.data.get('background_image')
        if about_me != None:
            user.about_me = about_me
        if background_image != None:
            user.background_image = background_image
        user.save()
        serializer = GetUserSerializer(user)
        return Response(serializer.data)
