from modelCore.models import UserWeekDayTime ,Language ,UserLanguage ,County, UserServiceLocation ,Service ,UserServiceShip ,License ,UserLicenseShipImage
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import viewsets, mixins

from user.serializers import UserSerializer, AuthTokenSerializer, UpdateUserSerializer ,GetUserSerializer

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
        user.Financial_Institutions_Code = request.data.get('Financial_Institutions_Code')
        user.Branch_Financial_Institutions_Code = request.data.get('Branch_Financial_Institutions_Code')
        user.accounts = request.data.get('accounts')
        user.save()
        serializer = GetUserSerializer(user)
        return Response(serializer.data)

class UpdateUserWeekDayTime(APIView):
    queryset = UserWeekDayTime.objects.all()
    
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, format=None):
        user = self.request.user
        weekday = request.data.get('weekday')
        weektime = request.data.get('weektime')
        if weekday != None:
            weekday_ids = weekday.split(',')
            weektime_list = weektime.split(',')
            UserWeekDayTime.objects.filter(user=user).delete()
            for i in range(len(weekday_ids)):
                start_time = int(weektime_list[i].split(':')[0][:2]) + float(int(weektime_list[i].split(':')[0][2:])/60)
                end_time = int(weektime_list[i].split(':')[1][:2]) + float(int(weektime_list[i].split(':')[1][2:])/60)
                userweekdaytime = UserWeekDayTime()
                userweekdaytime.user = user
                userweekdaytime.weekday = weekday_ids[i]
                userweekdaytime.start_time = start_time
                userweekdaytime.end_time = end_time
                userweekdaytime.save()
        serializer = GetUserSerializer(user)
        return Response(serializer.data)

class UpdateUserLanguage(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, format=None):
        user = self.request.user
        language = request.data.get('language')
        remark_original = request.data.get('remark_original')
        remark_others = request.data.get('remark_others')
        if language != None:
            language_ids = language.split(',')
            UserLanguage.objects.filter(user=user).delete()
            for language_id in language_ids:
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
        serializer = GetUserSerializer(user)
        return Response(serializer.data)

class UpdateUserCareType(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, format=None):
        user = self.request.user
        home = request.data.get('home')
        hospital = request.data.get('hospital')
        if home != None:
            home = home.split(',')
            user.is_home = True
            user.home_hour_wage = int(home[0])
            user.home_half_day_wage = int(home[1])
            user.home_one_day_wage = int(home[2])
        if hospital != None:
            hospital = hospital.split(',')
            user.is_hospital = True
            user.hospital_hour_wage = hospital[0]
            user.hospital_half_day_wage = hospital[1]
            user.hospital_one_day_wage = hospital[2]
        user.save()
        serializer = GetUserSerializer(user)
        return Response(serializer.data)

class UpdateUserLocations(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, format=None):
        user = self.request.user
        locations = request.data.get('locations')
        tranfer_fee = request.data.get('tranfer_fee')
        if locations != None:
            location_ids = locations.split(',')
            tranfer_fee_list = tranfer_fee.split(',')
            UserServiceLocation.objects.filter(user=user).delete()
            for i in range(len(location_ids)):
                userservicelocation = UserServiceLocation()
                userservicelocation.user = user
                userservicelocation.city = County.objects.get(id=location_ids[i]).city
                userservicelocation.county = County.objects.get(id=location_ids[i])
                userservicelocation.tranfer_fee = tranfer_fee_list[i]
                userservicelocation.save()
        serializer = GetUserSerializer(user)
        return Response(serializer.data)

class UpdateUserService(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, format=None):
        user = self.request.user
        services = request.data.get('services')
        increase_prices = request.data.get('increase_prices')
        if services != None:
            service_ids = services.split(',')
            increase_price_list = increase_prices.split(',')
            UserServiceShip.objects.filter(user=user).delete()
            for i in range(len(service_ids)):
                userserviceship = UserServiceShip()
                userserviceship.user = user
                userserviceship.service = Service.objects.get(id=service_ids[i])
                if int(service_ids[i]) < 5 :
                    userserviceship.increase_percent = increase_price_list[i]
                userserviceship.save()
        serializer = GetUserSerializer(user)
        return Response(serializer.data)

class UpdateUserLicenseImage(viewsets.GenericViewSet,
                    mixins.ListModelMixin,

                    mixins.CreateModelMixin):
    queryset = UserLicenseShipImage.objects.all()

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    # def put(self, request, format=None):
    #     user = self.request.user
    #     license_ids = License.objects.filter(id__gt=3).values_list('id', flat=True)
    #     UserLicenseShipImage.objects.filter(user=user).delete()
    #     for i in license_ids:
    #         if request.data.get('license_id_'+str(i)) != None:
    #             userlicenseshipimage = UserLicenseShipImage()
    #             userlicenseshipimage.user = user
    #             userlicenseshipimage.license = License.objects.get(id=int(i))
    #             userlicenseshipimage.image = request.data.get('license_id_'+str(i))
    #             userlicenseshipimage.save()
    #     serializer = GetUserSerializer(user)
    #     return Response(serializer.data)

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
