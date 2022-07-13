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
router.register('search_cases', views.CaseSearchViewSet)
router.register('orders', views.OrderViewSet)
router.register('userServiceLocations', views.UserServiceLocationViewSet)
router.register('userWeekDayTimes', views.UserWeekDayTimeViewSet)
router.register('chatroom', views.ChatRoomViewSet)
router.register('messages', views.MessageViewSet)
router.register('system_messages', views.SystemMessageViewSet)
router.register('search_servants', views.SearchServantViewSet)
router.register('recommend_servants', views.RecommendServantViewSet)
router.register('servant_cases', views.ServantCaseViewSet)
router.register('need_cases', views.NeedCaseViewSet)
router.register('reviews', views.ReviewViewSet)



app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('servant_put_review/<int:pk>', views.ServantPutReviewView.as_view()),
]