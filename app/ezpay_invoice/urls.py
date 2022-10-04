from django.urls import path
from ezpay_invoice import tasks

app_name = 'ezpay_invoice'

urlpatterns = [
    path('invoice', tasks.Invoice.as_view()),

]