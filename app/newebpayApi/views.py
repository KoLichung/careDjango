from __future__ import absolute_import, division, unicode_literals
from django.shortcuts import render 
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

import requests
import time
import altapay
import hashlib
from Crypto.Cipher import AES
from newebpayApi.aesCipher import AESCipher
from modelCore.models import Order 

class CreateMerchant(APIView):
    
    def get(self, request, format=None):
        order_id = self.request.query_params.get('order_id')
        order = Order.objects.get(id=order_id)

        post_url = 'https://ccore.NewebPay.com/API/AddMerchant/modify'
        timeStamp = int( time.time() )
        MerchantID = "MS336989148"
        PartnerID_ = "CARE168"
        HashKey = "Oq1IRY4RwYXpLAfmnmKkwd26bcT6q88q"
        HashIV = "CeYa8zoA0mX4qBpP"
        data = {
                "Version" : "1.8",
                "TimeStamp": timeStamp,
                "MemberPhone": "0987654321",
                "MemberAddress": "台南市中西區民族路27號",
                "LoginAccount": "Scottman0815",
                "ManagerMobile": "0987654321",
                "ManagerEmail": "scottman778@gmail.com",
                "DisputeMail": "scottman778@gmail.com",
                "MerchantEmail": "happy777@gmail.com",
                "MerchantID": "AAA123456",
                "MCType": 1,
                "MerchantName": "杏心股份有限公司",
                "MerchantNameE": "Xinshing",
                "MerchantWebURL": "http://test.com",
                "MerchantAddrCity": "台南市",
                "MerchantAddrArea": "中西區",
                "MerchantAddrCode": "700",
                "MerchantAddr": "民族路27號",
                "MerchantEnAddr": "test",
                "NationalE": "Taiwan",
                "CityE": "Tainan City",
                "MerchantType": 2,
                "BusinessType": "8999",
                "MerchantDesc": "test",
                "BankCode": order.user.ATMInfoBankCode,
                "SubBankCode": order.user.ATMInfoBranchBankCode,
                "BankAccount": order.user.ATMInfoAccount,
                "AccountName": order.user.name,
        }

        extend_params_personal = {
            "MemberUnified": "D123456789",
            "IDCardDate": "1110330",
            "IDCardPlace": "台南市",
            "IDPic": 1,
            "IDFrom": 3,
            "Date": "1000101",
            "MemberName": "林小華",
        }

        extend_params_company = {
            "MemberUnified": "22803842",
            "RepresentName": "王小明",
            "ManagerID": "M123321123",
            "CapitalAmount": "10000000",
            "IncorporationDate": "202020202",
            "CompanyAddress": "台南市中西區民族路27號",
        }

        data.update(extend_params_personal)
        # data.update(extend_params_company)
        query_string = altapay.utils.http_build_query(data)

        aes = AESCipher()
        postData = aes.encrypt(str(query_string))

        # encrypted = cbc_encrypt(query_string, HashKey, HashIV)
        # print(int(encrypted, 16))
        # PostData_ = str(encrypted)
        resp = requests.post(post_url, data ={"PartnerID_":PartnerID_, "PostData_":postData})
        return Response(resp)

class MpgTrade(APIView):
    
    def get(self, request, format=None):
        order_id = self.request.query_params.get('order_id')
        order = Order.objects.get(id=order_id)

        post_url = 'https://ccore.newebpay.com/MPG/mpg_gateway'
        timeStamp = int( time.time() )
        MerchantID = "MS336989148"
        Version = "2.0"
        HashKey = "Oq1IRY4RwYXpLAfmnmKkwd26bcT6q88q"
        HashIV = "CeYa8zoA0mX4qBpP"
        data = {
                "Version": "2.0",
                "MerchantID" : "MS336989148",
                "RespondType": "JSON",
                "TimeStamp": timeStamp,
                "MerchantOrderNo":"202207300001",
                "Amt": order.total_money,
                "ItemDesc": "test",       
                "ReturnURL": ""
        }

        query_string = altapay.utils.http_build_query(data)
        # encrypted = cbc_encrypt(query_string, HashKey, HashIV)

        aes = AESCipher()
        data = aes.encrypt(str(query_string))

        hash_object = hashlib.sha256(str(HashKey + data + HashIV).encode('utf-8'))
        # print(hash_object)
        TradeSha = hash_object.hexdigest().upper()
        # print(TradeSha)
        TradeInfo = data

        resp = requests.post(post_url, data ={"MerchantID":MerchantID,"TradeInfo":TradeInfo,"TradeSha":TradeSha, "Version":Version})
        # decrypt_text = cbc_decrypt(resp.text,HashKey)
        # the_data = urllib.parse.unquote(decrypt_text)
        return HttpResponse(resp)
        