from django.urls import path
from newebpayApi import views

app_name = 'newebpayApi'

urlpatterns = [
    path('create_merchant', views.CreateMerchant.as_view()),
    path('mpg_trade', views.MpgTrade.as_view()),
]