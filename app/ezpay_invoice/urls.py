from django.urls import path
from ezpay_invoice import views

app_name = 'ezpay_invoice'

urlpatterns = [
    path('invoice', views.Invoice.as_view()),

]