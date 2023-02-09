from __future__ import absolute_import, division, unicode_literals
from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse

from newebpayApi import module

import requests
import time
import urllib.parse
import hashlib
import codecs
import logging
import json
from modelCore.models import Order ,UserStore ,PayInfo ,UserLicenseShipImage ,License, City

logger = logging.getLogger(__file__)

class Invoice(APIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = self.request.user
        order_id = self.request.query_params.get('order_id')
        print(order_id)
        order = Order.objects.get(id=order_id)
        # TaxAmt = order.platform_money
        # print(TaxAmt)
        timeStamp = int( time.time() )

        # 測試
        # post_url = 'https://cinv.ezpay.com.tw/Api/invoice_issue'
        # MerchantID_ = "35104311"
        # key = "EESNrB33LHu6z705F5PXtBP3G06B4WhZ"
        # iv = "Ca1cfkx7oJiAJWwP"

        # 正式
        post_url = 'https://inv.ezpay.com.tw/Api/invoice_issue'
        MerchantID_ = "330658039"
        key = "3AdkuHMWuCFl5GdvwjhpoB1fxfRSILpS"
        iv = "PUiPYzm30OKfZ4gC"

        data = {
            'RespondType':'JSON',
            'Version':'1.5',
            'TimeStamp':str(timeStamp),
            'MerchantOrderNo':order_id,
            'Status':'1',
            'Category':'B2C',
            'BuyerName':order.servant.name,
            'PrintFlag':'Y',
            'TaxType':'1',
            'TaxRate':5,
            'Amt':order.platform_money-int(order.platform_money*0.05),
            'TaxAmt':int(order.platform_money*0.05),
            'TotalAmt':order.platform_money,
            'ItemName':'Care168平台服務費',
            'ItemCount':1,
            'ItemUnit':'項',
            'ItemPrice':order.platform_money,
            'ItemAmt':order.platform_money,
            'ItemTaxType':1,
            'BuyerEmail':order.servant.email
        }

        logger.info(data)

        extend_params_personal = {
            "CarrierType": '0',
            "BuyerEmail": 'scottman608@gmail.com',
            "CarrierNum": 'TEST',
            "LoveCode": 'test',
        }

        extend_params_company = {
            "BuyerUBN": "22803842",
        }

        # data.update(extend_params_personal)
        query_str = urllib.parse.urlencode(data)
        encrypt_data = module.aes256_cbc_encrypt(query_str, key, iv)
        resp = requests.post(post_url, data ={"MerchantID_":MerchantID_, "PostData_":encrypt_data})
        # 在order欄位加入
        print(json.loads(resp.text))
        # print(json.loads(json.loads(resp.text)['Result'])['InvoiceTransNo'])
        return Response(json.loads(resp.text))

# not used
# class Invoice_touch(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = self.request.user
        post_url = 'https://cinv.ezpay.com.tw/Api/invoice_touch_issue'
        timeStamp = int( time.time() )
        MerchantID_ = "CARE168"
        key = "Hxz8q13qoEMkW42UGrAOOeJwVz8E43PK"
        iv = "C7HjdwVLqYw4updP"

        data = {
            'RespondType':'JSON',
            'Version':'1.0。',
            'TimeStamp':str(timeStamp),
            'InvoiceTransNo':'test',
            'MerchantOrderNo':'201406010001',
            'TotalAmt':3150,
        }

        query_str = urllib.parse.urlencode(data)
        print(query_str)
        encrypt_data = module.aes256_cbc_encrypt(query_str, key, iv)
        print(encrypt_data)
        resp = requests.post(post_url, data ={"MerchantID_":MerchantID_, "PostData_":encrypt_data})
        print(resp)
        # 在order欄位加入
        return Response(json.loads(resp.text))