from __future__ import absolute_import, division, unicode_literals
from django.shortcuts import render 
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

import requests
import time
import altapay
import base64
import binascii
import hashlib
from Crypto.Cipher import AES
from modelCore.models import Order 

def cbc_encrypt(plaintext: str, key: str,iv: str):

    block_size = len(key)
    padding = (block_size - len(plaintext) % block_size) or block_size  # 填充位元組
    iv = iv
    mode = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
    ciphertext = mode.encrypt((plaintext + padding * chr(padding)).encode())
    return binascii.b2a_hex(ciphertext)
    # return base64.b64encode(iv.encode() + ciphertext).decode()

def cbc_decrypt(ciphertext: str, key: str):
    ciphertext = base64.b64decode(ciphertext)
    mode = AES.new(key.encode(), AES.MODE_CBC, ciphertext[:AES.block_size])
    plaintext = mode.decrypt(ciphertext[AES.block_size:]).decode()
    return plaintext[:-ord(plaintext[-1])]


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

        # aes = Cryptor(key=HashKey.encode("utf8"),iv=HashIV.encode("utf8"))
        # data = aes.encrypt(str(query_string))

        encrypted = cbc_encrypt(query_string, HashKey, HashIV)
        print(int(encrypted, 16))
        PostData_ = str(encrypted)
        resp = requests.post(post_url, data ={"PartnerID_":PartnerID_, "PostData_":PostData_})
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
        encrypted = cbc_encrypt(query_string, HashKey, HashIV)
        # aes = Cryptor(HashKey,HashIV)
        # data = aes.encrypt(str(query_string))
        hash_object = hashlib.sha256(str(HashKey + encrypted + HashIV).encode('utf-8'))
        print(hash_object)
        TradeSha = hash_object.hexdigest().upper()
        print(TradeSha)
        TradeInfo = encrypted
        resp = requests.post(post_url, data ={"MerchantID":MerchantID,"TradeInfo":TradeInfo,"TradeSha":TradeSha, "Version":Version})
        # decrypt_text = cbc_decrypt(resp.text,HashKey)
        # the_data = urllib.parse.unquote(decrypt_text)
        return HttpResponse(resp)
        