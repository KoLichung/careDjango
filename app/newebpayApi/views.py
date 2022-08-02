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
import json
from Crypto.Cipher import AES
from newebpayApi.aesCipher import AESCipher
from modelCore.models import Order ,UserStore

class CreateMerchant(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        # order_id = self.request.query_params.get('order_id')
        # order = Order.objects.get(id=order_id)

        post_url = 'https://ccore.Newebpay.com/API/AddMerchant'
        timeStamp = int( time.time() )
        PartnerID_ = "CARE168"
        key = "Oq1IRY4RwYXpLAfmnmKkwd26bcT6q88q"
        iv = "CeYa8zoA0mX4qBpP"
        data = {
                "Version" : "1.8",
                "TimeStamp": timeStamp,
                "MemberPhone": "0987-654321",
                "MemberAddress": "台南市中西區民族路27號",
                "ManagerName": "方聖傑",
                "ManagerNameE": "Sheng Jie,Fang",
                "LoginAccount": "scottfang2022",
                "ManagerMobile": "0981352308",
                "ManagerEmail": "scottman608@gmail.com",
                "DisputeMail": "scottman608@gmail.com",
                "MerchantEmail": "scottman608@gmail.com",
                "MerchantID": "ACE0000",
                "MCType": 1,
                "MerchantName": "杏心測試三",
                "MerchantNameE": "XinshingTest3",
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
                "BankCode": "013",
                "SubBankCode": "1379",
                "BankAccount": "137030000175",
                "AccountName": "齊家科技股份有限公司",
        }

        extend_params_personal = {
            "MemberUnified": "D122776936",
            "IDCardDate": "1070124",
            "IDCardPlace": "南市",
            "IDPic": 0,
            "IDFrom": 2,
            "Date": "19850911",
            "MemberName": "方聖傑",
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
        print(json.loads(resp.text)['MerchantID'])
        UserStore.objects.create(user=self.request.user,MerchantID=json.loads(resp.text)['MerchantID'],MerchantHashKey=json.loads(resp.text)['MerchantHashKey'],MerchantIvKey=json.loads(resp.text)['MerchantIvKey'])
        # save merchant_id, hash_key, hash_iv to UserStore

        return Response(json.loads(resp.text))

class MpgTrade(APIView):

    def get(self, request, format=None):
        # order_id = self.request.query_params.get('order_id')
        # order = Order.objects.get(id=order_id)

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
            "MerchantOrderNo":"202208020003",
            "Amt": 3500,
            "ItemDesc": "test",       
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
        html = codecs.open("MPG.html", 'r', 'utf-8')
        f.close()
        return HttpResponse(html)
        # html_string = f"<!DOCTYPE html><head><meta charset='utf-8'><title>MPG</title></head><body><form name='Newebpay' method='post' action={api_url}>測試URL: {api_url}<p>MerchantID:<input type='text' name='MerchantID' value={params['MerchantID']}><br><br>TradeInfo:<input type='text' name='TradeInfo' value={params['TradeInfo']}><br><br>TradeSha:<input type='text' name='TradeSha' value={params['TradeSha']}><br><br>Version:<input type='text' name='Version' value={params['Version']}><br><br><input type='submit' value='Submit'></form></body></html>"
       
        # resp = requests.post(api_url, data =params)
        # return HttpResponse(resp.text)

class SearchTradeInfo(APIView):
    def get(self, request, format=None):
        post_url = 'https://ccore.newebpay.com/API/QueryTradeInfo' 
        MerchantID = "MS336989148"
        key = "SKYfwec2P46Kzzgc8CrcblPzeX8r8jTH"
        iv = "C6RhZZ45pflwEoSP"
        Version = "1.3"
        RespondType = "JSON"
        check_data = {
            "Amt": 2500,
            "MerchantID" : MerchantID,
            "MerchantOrderNo":"202208020002",
            }
        # sorted_check_data = {}
        # for key in sorted(check_data):
        #     sorted_check_data[str(key)] = check_data[key]
        check_string = urllib.parse.urlencode(check_data)
        hashs = 'IV=' + iv + '&' + check_string + '&Key=' + key
        hashs = hashlib.sha256(hashs.encode("utf-8")).hexdigest()
        hash = str.upper(hashs)
        CheckValue = hash
        TimeStamp = int( time.time() )
        MerchantOrderNo = "202208020002"
        Amt = 3000

        # with open("SearchTradeInfo.html", 'w', encoding="utf-8") as f:
        #     html_string = f"<!DOCTYPE html><head><meta charset='utf-8'><title>MPG</title></head><body><form name='Newebpay' method='post' action={post_url}>測試URL: {post_url}<p>MerchantID:<input type='text' name='MerchantID' readonly='readonly' value={MerchantID} ><br><br>Version:<input type='text' name='Version' readonly='readonly' value={Version} ><br><br>RespondType:<input type='text' name='RespondType' readonly='readonly' value={RespondType}><br><br>CheckValue:<input type='text' name='CheckValue' readonly='readonly' value={CheckValue}><br><br><br>TimeStamp:<input type='text' name='TimeStamp' readonly='readonly' value={TimeStamp}><br><br>MerchantOrderNo:<input type='text' name='MerchantOrderNo' readonly='readonly' value={MerchantOrderNo}><br><br>Amt:<input type='text' name='Amt' readonly='readonly' value={Amt}><br><input type='submit' value='Submit'></form></body></html>"
        #     f.write(html_string)
        # html = codecs.open("SearchTradeInfo.html", 'r', 'utf-8')
        # f.close()
        # return HttpResponse(html)

        resp = requests.post(post_url, data ={"MerchantID":MerchantID, "Version":Version,"RespondType":RespondType, "CheckValue":CheckValue, "TimeStamp":TimeStamp,"MerchantOrderNo":MerchantOrderNo, "Amt":Amt})

        return Response(json.loads(resp.text))

class CancelAuthorization(APIView):
    def get(self, request, format=None):
        post_url = 'https://ccore.newebpay.com/API/CreditCard/Cancel'
        MerchantID_ = "MS336989148"
        timeStamp = int( time.time() )
        key = "SKYfwec2P46Kzzgc8CrcblPzeX8r8jTH"
        iv = "C6RhZZ45pflwEoSP"
        data = {
            "RespondType": "JSON",
            "Version": "1.0",
            "Amt": 2500,
            "MerchantOrderNo": "202208020002",
            "IndexType": 1,
            "TimeStamp": timeStamp,
        } 

        query_str = urllib.parse.urlencode(data)
        encrypt_data = module.aes256_cbc_encrypt(query_str, key, iv)

        resp = requests.post(post_url, data ={"MerchantID_":MerchantID_, "PostData_":encrypt_data})

        return Response(json.loads(resp.text))

class Invoice(APIView):
    def get(self, request, format=None):
        post_url = 'https://ccore.newebpay.com/API/CreditCard/Close'
        PartnerID_ = "CARE168"
        MerchantID = "MS336989148"
        timeStamp = int( time.time() )
        key = "SKYfwec2P46Kzzgc8CrcblPzeX8r8jTH"
        iv = "C6RhZZ45pflwEoSP"

        data = {
                "RespondType": "JSON",
                "Version": "1.1",
                "Amt": 3500,   
                "MerchantOrderNo":"202208020003",
                "TimeStamp": timeStamp,
                "IndexType" : 1,
                "TradeNo": "22080207362527794",
                "CloseType": 1,
            }

        query_str = urllib.parse.urlencode(data)
        encrypt_data = module.aes256_cbc_encrypt(query_str, key, iv)

        resp = requests.post(post_url, data ={"MerchantID_":MerchantID, "PostData_":encrypt_data})

        return Response(json.loads(resp.text))

class Appropriation(APIView):

    def get(self, request, format=None):
        post_url = 'https://ccore.newebpay.com/API/ExportInstruct'
        PartnerID_ = "CARE168"
        timeStamp = int( time.time() )
        key = "Oq1IRY4RwYXpLAfmnmKkwd26bcT6q88q"
        iv = "CeYa8zoA0mX4qBpP"

        data = {
                "Version": "1.0",
                "MerchantID" : "ACE123456",
                "MerTrade": "DebitTest001",
                "TimeStamp": timeStamp,
                "FeeType": 1,
                "BalanceType": 0,
                "MerchantOrderNo":"202207300003",
                "Amount": 3000,     
            }

        query_str = urllib.parse.urlencode(data)
        encrypt_data = module.aes256_cbc_encrypt(query_str, key, iv)

        resp = requests.post(post_url, data ={"PartnerID_":PartnerID_, "PostData_":encrypt_data})

        return Response(json.loads(resp.text))

class Debit(APIView):

    def get(self, request, format=None):
        post_url = 'https://ccore.newebpay.com/API/ChargeInstruct'
        PartnerID_ = "CARE168"
        timeStamp = int( time.time() )
        key = "Oq1IRY4RwYXpLAfmnmKkwd26bcT6q88q"
        iv = "CeYa8zoA0mX4qBpP"

        data = {
                "Version": "1.1",
                "MerchantID" : "ACE123456",
                "MerTrade": "DebitTest001",
                "TimeStamp": timeStamp,
                "FeeType": 1,
                "BalanceType": 0,
                "AppointMerID":"202207300003",
                "Amount": 3000,     
            }

        query_str = urllib.parse.urlencode(data)
        encrypt_data = module.aes256_cbc_encrypt(query_str, key, iv)

        resp = requests.post(post_url, data ={"PartnerID_":PartnerID_, "PostData_":encrypt_data})

        return Response(json.loads(resp.text))