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
from datetime import datetime, timedelta
import urllib.parse
import hashlib
import codecs
import logging
import json
from Crypto.Cipher import AES
from newebpayApi.aesCipher import AESCipher
from modelCore.models import Order ,UserStore ,PayInfo

logger = logging.getLogger(__file__)
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
                "MerchantID": "ACE00008",
                "MCType": 1,
                "MerchantName": "杏心測試八",
                "MerchantNameE": "XinshingTest8",
                "MerchantWebURL": "http://test.com",
                "MerchantAddrCity": "台南市",
                "MerchantAddrArea": "中西區",
                "MerchantAddrCode": "700",
                "MerchantAddr": "民族路27號",
                "MerchantEnAddr": "test",
                "NationalE": "Taiwan",
                "CityE": "Tainan City",
                "PaymentType": "CREDIT:1|WEBATM:0|VACC:0|CVS:0|BARCODE:0|EsunWallet:0|TaiwanPay:0",
                "MerchantType": 2,
                "BusinessType": "8999",
                "MerchantDesc": "test",
                "BankCode": "013",
                "SubBankCode": "1379",
                "BankAccount": "137030000175",
                "AccountName": "齊家科技股份有限公司",
                "NotifyURL": "http://202.182.105.11/newebpayApi/notifyurl_callback"
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
        # print(type(json.loads(resp.text)['status']))
        userstore = UserStore()
        userstore.user = self.request.user
        userstore.MerchantID = json.loads(resp.text)['result']['MerchantID']
        userstore.MerchantHashKey = json.loads(resp.text)['result']['MerchantHashKey']
        userstore.MerchantIvKey = json.loads(resp.text)['result']['MerchantIvKey']
        userstore.save()
        # save merchant_id, hash_key, hash_iv to UserStore

        return Response(json.loads(resp.text))

class MpgTrade(APIView):

    def get(self, request, format=None):
        # order_id = self.request.query_params.get('order_id')
        # order = Order.objects.get(id=order_id)

        api_url = 'https://ccore.newebpay.com/MPG/mpg_gateway'
        timeStamp = int( time.time() )

        Version = "2.0"

        merchant_id = "ACE00008"
        key = "Tog7hkxjtJcq9PeIX0qXx9GnIGAn6W9F"
        iv = "Cv96xp11VikUNhRP"

        data = {
            "Version": Version,
            "MerchantID" : merchant_id,
            "RespondType": "JSON",
            "TimeStamp": timeStamp,
            "MerchantOrderNo":"015",
            "Amt": 2000,
            "ItemDesc": "test",       
            "NotifyURL": "http://202.182.105.11/newebpayApi/notifyurl_callback"
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
        # <form id='form1' action={api_url} method='post'></form><script type='text/javascript'>form1.submit();</script>
        with open("MPG.html", 'w', encoding="utf-8") as f:
            html_string = f"<!DOCTYPE html><head><meta charset='utf-8'><title>MPG</title></head><body><form name='Newebpay' method='post' action={api_url}>測試URL: {api_url}<p>MerchantID:<input type='text' name='MerchantID' value={params['MerchantID']}><br><br>TradeInfo:<input type='text' name='TradeInfo' value={params['TradeInfo']}><br><br>TradeSha:<input type='text' name='TradeSha' value={params['TradeSha']}><br><br>Version:<input type='text' name='Version' value={params['Version']}><br><br><input type='submit' value='Submit'></form></body></html><script type='text/javascript'>Newebpay.submit();</script>"
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
        MerchantID = "ACE00004"
        key = "ZsaGSvba0vO3OP0pyu1hsUiqhhpdJL2m"
        iv = "CQtj19eestVGIjeP"
        Version = "1.3"
        RespondType = "JSON"
        check_data = {
            "Amt": 3500,
            "MerchantID" : MerchantID,
            "MerchantOrderNo":"202208020000",
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
        MerchantOrderNo = "202208020000"
        Amt = 3500

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

class NotifyUrlCallback(APIView):

    def post(self, request, format=None):
        # body_unicode = request.body.decode('utf-8')
        # logger.info(request)
        # logger.info(request.body)

        # logger.info(request.body.decode('utf-8'))

        data = urllib.parse.parse_qs(request.body.decode('utf-8'))
        logger.info(data)
        # print(body)
        key = "Tog7hkxjtJcq9PeIX0qXx9GnIGAn6W9F"
        iv = "Cv96xp11VikUNhRP"
        TradeInfo = data['TradeInfo'][0]
        decrypt_text = module.aes256_cbc_decrypt(TradeInfo, key, iv)
        # the_data = urllib.parse.unquote(decrypt_text)

        data_json = json.loads(decrypt_text)
        
        logger.info(data_json)

        if(PayInfo.objects.filter(OrderInfoMerchantOrderNo=data_json['Result']['MerchantOrderNo']).count()==0 ):
            payInfo = PayInfo()
            payInfo.MerchantID = data_json['Result']['MerchantID']

            if data_json['Status'] == 'SUCCESS' :
                payInfo.OrderInfoMerchantOrderNo = data_json['Result']['MerchantOrderNo']
                payInfo.OrderInfoTradeNo = data_json['Result']['TradeNo']
                payInfo.OrderInfoTradeAmt = data_json['Result']['Amt']
                payInfo.OrderInfoPaymentType = data_json['Result']['PaymentType']
                payInfo.OrderInfoPayTime = data_json['Result']['PayTime']
                try:
                    payInfo.OrderInfoTradeStatus = data_json['Result']['TradeStatus']
                except:
                    logger.info("no trade status")
            

            if data_json['Result']['PaymentType'] == 'CREDIT':
                payInfo.PaymentType = "信用卡"
                payInfo.EscrowBank = data_json['Result']['EscrowBank']
                payInfo.AuthBank = data_json['Result']['AuthBank']
                payInfo.Auth = data_json['Result']['Auth']
                payInfo.CardInfoCard6No = data_json['Result']['Card6No']
                payInfo.CardInfoCard4No = data_json['Result']['Card4No']

            payInfo.save()
            # if('ATMInfo' in data_json and data_json['ATMInfo']!= None):
            #     print("atm info")
            #     # 3碼
            #     payInfo.ATMInfoBankCode = data_json['ATMInfo']['ATMAccBank']
            #     # 後 5 碼
            #     payInfo.ATMInfovAccount = data_json['ATMInfo']['ATMAccNo']
            # else:
            #     print("no atm info")

            # if('CustomField' in data_json and data_json['CustomField']!= None):
            #     try:
            #         order = Order.objects.get(id= int(data_json['CustomField']))
            #         order.state = 'ownerWillContact'
            #         order.save()
            #         payInfo.order = order
            #         payInfo.save()
            #     except:
            #         print("can't find order custom field error")
            # else:
            #     order = Order.objects.get(id=1)
            #     order.state = 'ownerWillContact'
            #     order.save()
            #     payInfo.order = Order.objects.get(id=1)
                # payInfo.save()
            
            
        # print(the_data)

        # content = body['content']
        # print(content)

        return Response("1|OK")