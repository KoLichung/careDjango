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
from modelCore.models import Order,UserStore,PayInfo,UserLicenseShipImage,License,City,County,User

logger = logging.getLogger(__file__)

class CreateMerchant(APIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)

        ID_card_name = request.POST.get('ID_card_name')
        ManagerNameE = request.POST.get('ManagerNameE')
        ID_number = request.POST.get('ID_number')
        birthday = request.POST.get('birthday')
        ID_card_date = request.POST.get('ID_card_date')
        IDFrom = request.POST.get('IDFrom')
        city_id = request.POST.get('city_id')
        county_id = request.POST.get('county_id')
        ID_card_name = request.POST.get('ID_card_name')

        MerchantAddr = request.POST.get('MerchantAddr')
        MerchantEnAddr = request.POST.get('MerchantEnAddr')

        city = City.objects.get(id=city_id)
        county = County.objects.get(id=county_id)

        # if UserStore.objects.filter(user=user).count() == 0:
        #     print('code here')

        post_url = 'https://ccore.Newebpay.com/API/AddMerchant'
        timeStamp = int( time.time() )
        PartnerID_ = "CARE168"
        key = "Oq1IRY4RwYXpLAfmnmKkwd26bcT6q88q"
        iv = "CeYa8zoA0mX4qBpP"
        
        LoginAccount = "XinShing"+str(user.id)

        data = {
                "Version" : "1.8",
                "TimeStamp": timeStamp,
                "MemberPhone": parsePhone(user.phone),
                "MemberAddress": city.name+county.name+MerchantAddr,
                "ManagerName": ID_card_name,
                "ManagerNameE": ManagerNameE,
                "LoginAccount": LoginAccount,
                "ManagerMobile": user.phone.replace('-', '').replace(' ', ''),
                "ManagerEmail": "jason@kosbrother.com",
                "DisputeMail": "jason@kosbrother.com",
                "MerchantEmail": "jason@kosbrother.com",
                "MerchantID": "ACE0168"+str(user.id),
                "MCType": 1,
                "MerchantName": "杏心合作商店"+str(user.id),
                "MerchantNameE": "XinShing"+str(user.id),
                "MerchantWebURL": "https://care168.com.tw/web/search_carer_detail?servant="+str(user.id),
                "MerchantAddrCity": city.name,
                "MerchantAddrArea": county.name,
                "MerchantAddrCode": county.addressCode,
                "MerchantAddr": MerchantAddr,
                "MerchantEnAddr": MerchantEnAddr,
                "NationalE": "Taiwan",
                "CityE": city.nameE,
                "PaymentType": "CREDIT:1|WEBATM:0|VACC:0|CVS:0|BARCODE:0|EsunWallet:0|TaiwanPay:0",
                "MerchantType": 2,
                "BusinessType": "8999",
                "MerchantDesc": "test",
                "BankCode": user.ATMInfoBankCode,
                "SubBankCode": str(user.ATMInfoBranchBankCode),
                "BankAccount": user.ATMInfoAccount,
                # "AccountName": "齊家科技股份有限公司",
                "CreditAutoType": 1,
                "AgreedDay": "CREDIT:0",
                "Withdraw": "",
                "WithdrawMer": "",
                "WithdrawSetting" : "Withdraw=9",
                # "NotifyURL": "http://202.182.105.11/newebpayApi/notifyurl_callback/2/",
                
        }

        if UserLicenseShipImage.objects.get(user=user,license=License.objects.get(id=1)).image != None:
            IDPic = 0
        else:
            IDPic = 1

        extend_params_personal = {
            "MemberUnified": ID_number,
            "IDCardDate": ID_card_date,
            "IDCardPlace": city.newebpay_cityname,
            "IDPic": IDPic,
            "IDFrom": IDFrom,
            "Date": birthday,
            "MemberName": ID_card_name,
        }

        logger.info(data)
        logger.info(extend_params_personal)

        # extend_params_company = {
        #     "MemberUnified": "22803842",
        #     "RepresentName": "王小明",
        #     "ManagerID": "M123321123",
        #     "CapitalAmount": "10000000",
        #     "IncorporationDate": "202020202",
        #     "CompanyAddress": "台南市中西區民族路27號",
        # }

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

        print(resp.text)
        # print(type(json.loads(resp.text)['status']))
        # logger.info('check test')
        logger.info(resp.text)

        userstore = UserStore()
        userstore.user = user
        userstore.MerchantID = json.loads(resp.text)['result']['MerchantID']
        userstore.MerchantHashKey = json.loads(resp.text)['result']['MerchantHashKey']
        userstore.MerchantIvKey = json.loads(resp.text)['result']['MerchantIvKey']
        userstore.LoginAccount = LoginAccount
        userstore.MemberUnified = ID_number
        userstore.save()

        # save merchant_id, hash_key, hash_iv to UserStore

        return Response(json.loads(resp.text))

def parsePhone(phone):
    phone = phone.replace('-', '').replace(' ', '')
    return phone[0:4]+'-'+phone[4:len(phone)]

class MpgTrade(APIView):

    def get(self, request, format=None):
        print('test')
        order_id = self.request.query_params.get('order_id')
        print(order_id)
        order = Order.objects.get(id=order_id)
        user = order.user
        userStore = UserStore.objects.get(user=user)
        api_url = 'https://ccore.newebpay.com/MPG/mpg_gateway'
        timeStamp = int( time.time() )
        item_desc = "時薪 $"+ str(order.wage_hour) + " 共 " + str(order.work_hours) + " 小時"
        Version = "2.0"
        # order_id = '4'
        merchant_id = userStore.MerchantID
        key = userStore.MerchantHashKey
        iv = userStore.MerchantIvKey
        Amt = str(order.total_money)
        data = {
            "Version": Version,
            "MerchantID" : merchant_id,
            "RespondType": "JSON",
            "TimeStamp": timeStamp,
            "MerchantOrderNo": order_id,
            "Amt": Amt,
            "ItemDesc": item_desc,       
            "NotifyURL": "http://202.182.105.11/newebpayApi/notifyurl_callback/" + str(userStore.id) + "/",
            "ClientBackURL": "http://202.182.105.11/newebpayApi/success_pay",
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

def success_pay(request):
    return render(request, 'success_pay.html')

class SearchTradeInfo(APIView):
    def get(self, request, format=None):
        post_url = 'https://ccore.newebpay.com/API/QueryTradeInfo' 
        MerchantID = "ACE00009"
        key = "4hfcUUaByF7iCMttHAj06qVqgzKS1kiU"
        iv = "C3RqE64KeXb3RPqP"
        Version = "1.3"
        RespondType = "JSON"
        check_data = {
            "Amt": 2000,
            "MerchantID" : MerchantID,
            "MerchantOrderNo":"3",
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
        MerchantOrderNo = "3"
        Amt = 2000

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

# 請款
class Invoice(APIView):
    def get(self, request, format=None):
        post_url = 'https://ccore.newebpay.com/API/CreditCard/Close'
        MerchantID = "ACE00009"
        timeStamp = int( time.time() )
        key = "4hfcUUaByF7iCMttHAj06qVqgzKS1kiU"
        iv = "C3RqE64KeXb3RPqP"

        data = {
                "RespondType": "JSON",
                "Version": "1.1",
                "Amt": 2000,   
                "MerchantOrderNo":"3",
                "TimeStamp": timeStamp,
                "IndexType" : 1,
                "TradeNo": "22080613222748822",
                "CloseType": 1,
            }

        query_str = urllib.parse.urlencode(data)
        encrypt_data = module.aes256_cbc_encrypt(query_str, key, iv)

        resp = requests.post(post_url, data ={"MerchantID_":MerchantID, "PostData_":encrypt_data})

        return Response(json.loads(resp.text))

# 撥款
class Appropriation(APIView):

    def get(self, request, format=None):
        post_url = 'https://ccore.newebpay.com/API/ExportInstruct'
        PartnerID_ = "CARE168"
        timeStamp = int( time.time() )
        key = "Oq1IRY4RwYXpLAfmnmKkwd26bcT6q88q"
        iv = "CeYa8zoA0mX4qBpP"

        data = {
                "Version": "1.0",
                "MerchantID" : "ACE00009",
                "MerTrade": "DebitTest001",
                "TimeStamp": timeStamp,
                "FeeType": 1,
                "BalanceType": 0,
                "MerchantOrderNo":"3",
                "Amount": 2000,     
            }

        query_str = urllib.parse.urlencode(data)
        encrypt_data = module.aes256_cbc_encrypt(query_str, key, iv)

        resp = requests.post(post_url, data ={"PartnerID_":PartnerID_, "PostData_":encrypt_data})

        return Response(json.loads(resp.text))

# 扣款
class Debit(APIView):

    def get(self, request, format=None):
        post_url = 'https://ccore.newebpay.com/API/ChargeInstruct'
        PartnerID_ = "CARE168"
        timeStamp = int( time.time() )
        key = "Oq1IRY4RwYXpLAfmnmKkwd26bcT6q88q"
        iv = "CeYa8zoA0mX4qBpP"

        data = {
                "Version": "1.1",
                "MerchantID" : "ACE00009",
                "MerTrade": "DebitTest001",
                "TimeStamp": timeStamp,
                "FeeType": 1,
                "BalanceType": 0,
                "Amount": 2000,     
            }

        query_str = urllib.parse.urlencode(data)
        encrypt_data = module.aes256_cbc_encrypt(query_str, key, iv)

        resp = requests.post(post_url, data ={"PartnerID_":PartnerID_, "PostData_":encrypt_data})

        return Response(json.loads(resp.text))

class NotifyUrlCallback(APIView):

    def post(self, request, id):
        # body_unicode = request.body.decode('utf-8')
        # logger.info(request)
        # logger.info(request.body)

        # logger.info(request.body.decode('utf-8'))
        userstore_id = id
        logger.info('id:',id)
        userStore = UserStore.objects.get(id=userstore_id)
        data = urllib.parse.parse_qs(request.body.decode('utf-8'))
        logger.info(data)
        # print(body)
        key = userStore.MerchantHashKey
        iv = userStore.MerchantIvKey
        TradeInfo = data['TradeInfo'][0]
        decrypt_text = module.aes256_cbc_decrypt(TradeInfo, key, iv)
        # the_data = urllib.parse.unquote(decrypt_text)

        data_json = json.loads(decrypt_text)
        
        logger.info(data_json)

        if(PayInfo.objects.filter(OrderInfoMerchantOrderNo=data_json['Result']['MerchantOrderNo']).count()==0 ):
            payInfo = PayInfo()
            payInfo.order = Order.objects.get(id=data_json['Result']['MerchantOrderNo'])
            payInfo.MerchantID = data_json['Result']['MerchantID']
            
            if data_json['Status'] == 'SUCCESS' :
                payInfo.OrderInfoMerchantOrderNo = data_json['Result']['MerchantOrderNo']
                payInfo.OrderInfoTradeNo = data_json['Result']['TradeNo']
                payInfo.OrderInfoTradeAmt = data_json['Result']['Amt']
                payInfo.OrderInfoPaymentType = data_json['Result']['PaymentType']
                payInfo.OrderInfoPayTime = data_json['Result']['PayTime']
                payInfo.save()
                #change order state
                order = Order.objects.get(id=payInfo.OrderInfoMerchantOrderNo)
                order.state='paid'

                case = order.case
                case.servant = order.servant

                order.save()
                case.save()

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