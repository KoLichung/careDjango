from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('markup_items', views.MarkupItemViewSet)
router.register('licenses',views.LicenseViewSet)
router.register('servant_search',views.ServantSearchViewSet)
router.register('servant_markupItem_prices',views.ServantMarkupItemPriceViewSet)
router.register('user_licenses', views.UserLicenseShipImageViewSet)
router.register('servant_licenses', views.ServantLicenseShipImageViewSet)
router.register('recipients', views.RecipientViewSet)
router.register('serviceItems',views.ServiceItemViewSet)
router.register('cases',views.CaseViewSet)
router.register('orderstates', views.OrderStateViewSet)
router.register('orders', views.OrderViewSet)
router.register('orderReviews', views.OrderReviewViewSet)
router.register('my_post_case', views.MYPostCaseViewSet)
router.register('my_take_case', views.MYTakeCaseViewSet)
router.register('not_rated_yet', views.NotRatedYetViewSet)
router.register('servant_rate', views.ServantRateViewSet)
router.register('user_rate', views.UserRateViewSet)
router.register('case_detail', views.CaseDetailViewSet)




app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('case_search', views.CaseSearchViewSet.as_view()),
    path('add_servant_rate', views.AddServantRateViewSet.as_view()),
    path('add_user_rate', views.AddUserRateViewSet.as_view()),
    path('change_basic_info', views.ChangeBasicInfoViewSet.as_view()),
    path('my_document', views.MyDocumentViewSet.as_view()),
    path('service_settings', views.ServiceSettingsViewSet.as_view()),
    path('fill_order', views.FillOrderViewSet.as_view()),
]