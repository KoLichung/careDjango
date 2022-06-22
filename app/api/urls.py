from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('markup_items', views.MarkupItemViewSet)
router.register('categories', views.CategoryViewSet)
router.register('languages',views.LanguageSkillViewSet)
router.register('licenses',views.LicenseViewSet)
router.register('servants',views.ServantViewSet)
router.register('servant_markupItem_prices',views.ServantMarkupItemPriceViewSet)
router.register('servant_skills',views.ServantSkillShipViewSet)
router.register('user_licenses', views.UserLicenseShipImageViewSet)
router.register('servant_licenses', views.ServantLicenseShipImageViewSet)
router.register('servant_categories', views.ServantCategoryShipViewSet)
router.register('recipients', views.RecipientViewSet)
router.register('serviceItems',views.ServiceItemViewSet)
router.register('citys',views.CityViewSet)
router.register('cityareas',views.CityAreaViewSet)
router.register('transportations',views.TransportationViewSet)
router.register('cases',views.CaseViewSet)
router.register('case_serviceItems', views.CaseServiceItemShipViewSet)
router.register('orderstates', views.OrderStateViewSet)
router.register('orders', views.OrderViewSet)
router.register('orderReviews', views.OrderReviewViewSet)


app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]