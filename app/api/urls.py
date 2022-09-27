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

router.register('system_messages', views.SystemMessageViewSet)
router.register('search_servants', views.SearchServantViewSet)
router.register('recommend_servants', views.RecommendServantViewSet)
router.register('servant_cases', views.ServantCaseViewSet)
router.register('need_cases', views.NeedCaseViewSet)
router.register('reviews', views.ReviewViewSet)
router.register('blog_posts', views.BlogPostViewSet)
router.register('blog_categories', views.BlogCategoryViewSet)
# router.register('choose_servant', views.ChooseServantViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('servant_put_review/<int:pk>', views.ServantPutReviewView.as_view()),
    path('create_case', views.CreateCase.as_view()),
    path('create_servant_order', views.CreateServantOrder.as_view()),
    path('messages', views.MessageViewSet.as_view()),
    path('earlytermination', views.EarlyTermination.as_view()),
    path('edit_case', views.EditCase.as_view()),
]