from modelCore.models import UserWeekDayTime ,Language ,UserLanguage ,City, UserServiceLocation ,Service ,UserServiceShip ,License 
from modelCore.models import ChatroomUserShip, UserLicenseShipImage, ChatroomMessage ,User 
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import viewsets, mixins

from user.serializers import UserSerializer, AuthTokenSerializer, UpdateUserSerializer ,GetUserSerializer, UserLicenceImageSerializer
from api import serializers
from django.db.models import Q

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

    def perform_create(self, serializer,):
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
        # if self.request.user.line_id != None and self.request.user.line_id != '':
        #     self.request.user.is_gotten_line_id = True
        
        user = self.request.user
        
        #total_unread_num
        #找出有我的 chatrooms, 找出 unread messages id__in chatroom_ids, count()
        chatroom_ids = list(ChatroomUserShip.objects.filter(user=user).values_list('chatroom', flat=True))
        total_not_read_messages = ChatroomMessage.objects.filter(chatroom__in=chatroom_ids,is_read_by_other_side=False).filter(~Q(user=user))
        user.total_unread_num = total_not_read_messages.count()

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

class UserWeekDayTimesViewSet(generics.UpdateAPIView,generics.ListAPIView,):
    queryset = UserWeekDayTime.objects.all()
    serializer_class = serializers.UserWeekDayTimeSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(user=user)
        return queryset

    def update(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.queryset
        weekday = request.data.get('weekday')
        weektime = request.data.get('weektime')
        if weekday != None and weekday != '':
            weekday_ids = weekday.split(',')
            weektime_list = weektime.split(',')
            for i in range(len(weekday_ids)):
                if queryset.filter(user=user,weekday=weekday_ids[i]).exists() != True:
                    userweekdaytime = UserWeekDayTime()
                else:
                    userweekdaytime = queryset.get(user=user,weekday=weekday_ids[i])
                # start_time = int(weektime_list[i].split(':')[0][:2]) + float(int(weektime_list[i].split(':')[0][2:])/60)
                # end_time = int(weektime_list[i].split(':')[1][:2]) + float(int(weektime_list[i].split(':')[1][2:])/60)
                start_time = weektime_list[i].split(':')[0]
                end_time = weektime_list[i].split(':')[1]
                userweekdaytime.user = user
                userweekdaytime.weekday = weekday_ids[i]
                userweekdaytime.start_time = start_time
                userweekdaytime.end_time = end_time
                userweekdaytime.save()
            for userweekdaytime in queryset.filter(user=user):
                if userweekdaytime.weekday not in weekday_ids:
                    userweekdaytime.delete()

        if weekday=='':
            queryset.filter(user=user).delete()

        queryset = queryset.filter(user=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class UserLanguagesViewSet(generics.UpdateAPIView,generics.ListAPIView,):
    queryset = UserLanguage.objects.all()
    serializer_class = serializers.UserLangaugeSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(user=user)
        return queryset

    def update(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.queryset
        language = request.data.get('language')
        remark_original = request.data.get('remark_original')
        remark_others = request.data.get('remark_others')
        if language != None and language!='':
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
        userlanguages = UserLanguage.objects.filter(user=user)    
        serializer = self.get_serializer(userlanguages,many=True)
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

class UserLocationsViewSet(generics.UpdateAPIView,generics.ListAPIView,):
    queryset = UserServiceLocation.objects.all()
    serializer_class = serializers.UserServiceLocationSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        user_id = self.request.query_params.get('user_id')
        if user_id == None:
            queryset = self.queryset.filter(user=user)
        else:
            queryset = self.queryset.filter(user=User.objects.get(id=user_id))
        return queryset

    def update(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.queryset
        locations = request.data.get('locations')
        transfer_fee = request.data.get('transfer_fee')
        if locations != None:
            location_ids = locations.split(',')
            transfer_fee_list = transfer_fee.split(',')
            for i in range(len(location_ids)):
                if queryset.filter(user=user,city=location_ids[i]).exists() != True:
                    userservicelocation = UserServiceLocation()
                else:
                    userservicelocation = queryset.get(user=user,city=location_ids[i])
                userservicelocation.user = user
                userservicelocation.city = City.objects.get(id=location_ids[i])
                userservicelocation.transfer_fee = transfer_fee_list[i]
                userservicelocation.save()
            for userservicelocation in queryset.filter(user=user):
                if str(userservicelocation.city.id) not in location_ids:
                    userservicelocation.delete()
        queryset = queryset.filter(user=user)
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)

class UserServicesViewSet(generics.UpdateAPIView,generics.ListAPIView,):
    queryset = UserServiceShip.objects.all()
    serializer_class = serializers.UserServiceSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(user=user)
        return queryset

    def update(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.queryset
        services = request.data.get('services')
        print(services)

        if services != None:
            service_ids = services.split(',')
            print(service_ids)
            service_id_list = []
            for i in range(len(service_ids)):
                if ':' in service_ids[i]:
                    service_id = service_ids[i].split(':')[0]
                    service_id_list.append(service_id)

                    increase_percent = service_ids[i].split(':')[1]
                    if queryset.filter(user=user,service=service_id).exists() != True:
                        userserviceship = UserServiceShip()
                    else:
                        userserviceship = queryset.get(user=user,service=service_id)

                    userserviceship.user = user
                    userserviceship.service = Service.objects.get(id=service_id)
                    userserviceship.increase_percent = increase_percent
                    userserviceship.save()
                else:
                    service_id = service_ids[i]
                    service_id_list.append(service_id)

                    if queryset.filter(user=user,service=service_id).exists() != True:
                        userserviceship = UserServiceShip()
                    else:
                        userserviceship = queryset.get(user=user,service=service_id)

                    userserviceship.user = user
                    userserviceship.service = Service.objects.get(id=service_id)
                    userserviceship.save()

            for userserviceship in queryset.filter(user=user):
                if str(userserviceship.service.id) not in service_id_list:
                    userserviceship.delete()

        userservices = UserServiceShip.objects.filter(user=user)
        serializer = self.get_serializer(userservices,many=True)

        return Response(serializer.data)

class UserLicenseImagesViewSet(generics.UpdateAPIView,generics.ListAPIView,):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = UserLicenseShipImage.objects.all()
    serializer_class = UserLicenceImageSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(user=user).order_by('license')
        return queryset

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
        userlicences = UserLicenseShipImage.objects.filter(user=user)
        serializer = self.get_serializer(userlicences,many=True)
        return Response(serializer.data)

class UpdateUserBackgroundImage(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, format=None):
        user = self.request.user

        background_image = request.data.get('background_image')
        if background_image != None:
            user.background_image = background_image
            
        user.save()
        serializer = GetUserSerializer(user)
        return Response(serializer.data)

class UpdateUserImage(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, format=None):
        user = self.request.user
        image = request.data.get('image')
        if image != None:
            user.image = image
        user.save()
        serializer = GetUserSerializer(user)
        return Response(serializer.data)

class GetUpdateUserFCMNotify(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = self.request.user
        return Response({'is_fcm_notify':user.is_fcm_notify})

    def put(self, request, format=None):
        user = self.request.user
        is_fcm_notify = request.data.get('is_fcm_notify')
        if is_fcm_notify =='true' or is_fcm_notify =='True':
            user.is_fcm_notify = True
        else:
             user.is_fcm_notify = False
        user.save()
        return Response({'message':'ok'})

class DeleteUser(generics.DestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # lookup_field = 'pk'
    def delete(self, request, pk, format=None):
        
        auth_user = self.request.user
        user = User.objects.get(id=pk)
        if user == auth_user:
            if qualifications_to_delete_user(user) == False:
                return Response("continuous order exists")
            else:
                user.delete()
                return Response('delete user')
        else:
            return Response('not auth')

def qualifications_to_delete_user(user):
    for order in user.user_orders.all():
        if order.case.state == 'unComplete':
            return False
    for order in user.servant_orders.all():
        if order.case.state == 'unComplete':
            return False