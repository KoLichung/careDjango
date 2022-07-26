from __future__ import absolute_import, division, unicode_literals
from urllib import response
from django.shortcuts import render 
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

from newebpayApi import module
import requests
import time
import urllib.parse
import webbrowser
import hashlib
from Crypto.Cipher import AES
from newebpayApi.aesCipher import AESCipher
from modelCore.models import Order 

class CreateMerchant(APIView):
    
    def get(self, request, format=None):
        order_id = self.request.query_params.get('order_id')
        order = Order.objects.get(id=order_id)

        post_url = 'https://ccore.Newebpay.com/API/AddMerchant'
        timeStamp = int( time.time() )
        MerchantID = "MS336989148"
        PartnerID_ = "CARE168"
        key = "Oq1IRY4RwYXpLAfmnmKkwd26bcT6q88q"
        iv = "CeYa8zoA0mX4qBpP"
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
                "MerchantName": "杏心一股份有限公司",
                "MerchantNameE": "XinshingOne",
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
            "MemberUnified": "N124596345",
            "IDCardDate": "1070124",
            "IDCardPlace": "桃市",
            "IDPic": 0,
            "IDFrom": 2,
            "Date": "19850911",
            "MemberName": "柯力中",
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

        query_str = urllib.parse.urlencode(data)
        encrypt_data = module.aes256_cbc_encrypt(query_str, key, iv)
        
        # query_string = altapay.utils.http_build_query(data)
        # aes = AESCipher()
        # postData = aes.encrypt(str(query_string))

        # encrypted = cbc_encrypt(query_string, HashKey, HashIV)
        # print(int(encrypted, 16))
        # PostData_ = str(encrypted)
        resp = requests.post(post_url, data ={"PartnerID_":PartnerID_, "PostData_":encrypt_data})
        return Response(resp)

class MpgTrade(APIView):
    
    def get(self, request, format=None):
        order_id = self.request.query_params.get('order_id')
        order = Order.objects.get(id=order_id)

        api_url = 'https://ccore.newebpay.com/MPG/mpg_gateway'
        timeStamp = int( time.time() )
        merchant_id = "MS336989148"
        Version = "2.0"
        key = "SKYfwec2P46Kzzgc8CrcblPzeX8r8jTH"
        iv = "C6RhZZ45pflwEoSP"
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

        query_str = urllib.parse.urlencode(data)
        encrypt_data = module.aes256_cbc_encrypt(query_str, key, iv)
        hashs = module.sha256_hash(encrypt_data, key, iv)
        
        params = {
            "MerchantID": merchant_id,
            "TradeInfo": encrypt_data,
            "TradeSha": hashs,
            "Version": data["Version"],
        }               
        with open("MPG.html", 'w', encoding="utf-8") as f:
            html_string = f"<!DOCTYPE html><head><meta charset='utf-8'><title>MPG</title></head><body><form name='Newebpay' method='post' action={api_url}>測試URL: {api_url}<p>MerchantID:<input type='text' name='MerchantID' value={params['MerchantID']}><br><br>TradeInfo:<input type='text' name='TradeInfo' value={params['TradeInfo']}><br><br>TradeSha:<input type='text' name='TradeSha' value={params['TradeSha']}><br><br>Version:<input type='text' name='Version' value={params['Version']}><br><br><input type='submit' value='Submit'></form></body></html>"
            f.write(html_string)
        webbrowser.open("MPG.html", "r")
        return response('ok')
        # query_string = altapay.utils.http_build_query(data)
        # # encrypted = cbc_encrypt(query_string, HashKey, HashIV)
        # aes = AESCipher()
        # data = aes.encrypt(str(query_string))
        # hash_object = hashlib.sha256(str(HashKey + data + HashIV).encode('utf-8'))
        # print(hash_object)
        # TradeSha = hash_object.hexdigest().upper()
        # print(TradeSha)
        # TradeInfo = data

        resp = requests.post(api_url, data =params)
        # decrypt_text = cbc_decrypt(resp.text,HashKey)
        # the_data = urllib.parse.unquote(decrypt_text)
        return HttpResponse(resp)
        