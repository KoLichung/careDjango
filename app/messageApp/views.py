from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from modelCore.models import User
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice

class TestFCMViewSet(APIView):
    def get(self, request, format=None):
        from messageApp.tasks import sendTest
        sendTest()
        return Response({'message': "ok"})

class FCMDeviceViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        #name, active
        try:  
            registration_id = request.data.get('registration_id')
            device_id = request.data.get('device_id')
            type = request.data.get('type')

            if FCMDevice.objects.filter(device_id=device_id).count() == 0:
                fcmDevice = FCMDevice()
                fcmDevice.user = self.request.user
                fcmDevice.registration_id = registration_id
                fcmDevice.device_id = device_id
                fcmDevice.type = type
                fcmDevice.save()
                return Response({'message': "ok"})
            else:
                fcmDevice = FCMDevice.objects.filter(device_id=device_id).first()
                fcmDevice.registration_id = registration_id
                fcmDevice.device_id = device_id
                fcmDevice.save()
                return Response({'message': "already regist fcm device, update token"})
        except:
            return Response({'message': "error"})