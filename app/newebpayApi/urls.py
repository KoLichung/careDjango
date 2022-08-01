from django.urls import path
from newebpayApi import views

app_name = 'newebpayApi'

urlpatterns = [
    path('create_merchant', views.CreateMerchant.as_view()),
    path('mpg_trade', views.MpgTrade.as_view()),
    path('search_tradeinfo', views.SearchTradeInfo.as_view()),
    path('cancel_authorization', views.CancelAuthorization.as_view()),
    path('invoice', views.Invoice.as_view()),
    path('appropriation', views.Appropriation.as_view()),
    path('debit', views.Debit.as_view()),
]