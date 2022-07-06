from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register('licenses', views.LicenseViewSet)
router.register('languages', views.LanguageViewSet)
router.register('services', views.ServiceViewSet)
router.register('disease_conditions', views.DiseaseConditionViewSet)
router.register('body_conditions', views.BodyConditionViewSet)
router.register('citys', views.CityViewSet)
router.register('countys', views.CountyViewSet)
router.register('cases', views.CaseViewSet)
router.register('orders', views.OrderViewSet)
router.register('userServiceLocations', views.UserServiceLocationViewSet)
router.register('caseWeekDayTimes', views.CaseWeekDayTimeViewSet)
router.register('userWeekDayTimes', views.UserWeekDayTimeViewSet)
router.register('messages', views.MessageViewSet)
router.register('systemMessages', views.SystemMessageViewSet)
router.register('search_servants', views.SearchServantViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]