
from modelCore.models import Order
import requests
import time
import urllib.parse
import hashlib
import codecs
import logging
import json
from modelCore.models import Order,UserStore,PayInfo,UserLicenseShipImage,License,City,County,User
from newebpayApi import module

logger = logging.getLogger(__file__)

#1.尚未請款, 無法退款
#2.已請款, 尚未撥款 => 可退款

#步驟:
#1.先查看訂單狀態
def backboard_refound(order_id, money):
    order = Order.objects.get(id=order_id)

    #search trade info

    #if trade info is 已請款
    #進行退款
    #return "success"

    #if trade info is not 請款
    #return "haven't send invoice to bank"

    #測試
    # post_url = 'https://ccore.newebpay.com/API/CreditCard/Close'
    #正式
    post_url = 'https://core.newebpay.com/API/CreditCard/Close'
    
    timeStamp = int( time.time() )

    close_type = 2

    order = Order.objects.get(id=order_id)
    user = order.servant
    userStore = UserStore.objects.filter(user=user).first()

    MerchantID = userStore.MerchantID
    key = userStore.MerchantHashKey
    iv = userStore.MerchantIvKey

    payInfo = PayInfo.objects.get(order=order)

    data = {
            "RespondType": "JSON",
            "Version": "1.1",
            "Amt": money,   
            "MerchantOrderNo": order.id,
            "TimeStamp": timeStamp,
            "IndexType" : 1,
            "TradeNo": payInfo.OrderInfoTradeNo,
            "CloseType": close_type,
        }

    logger.info(data)

    query_str = urllib.parse.urlencode(data)
    encrypt_data = module.aes256_cbc_encrypt(query_str, key, iv)

    resp = requests.post(post_url, data ={"MerchantID_":MerchantID, "PostData_":encrypt_data})
    # resp.encoding = 'utf-8'

    jsonText = json.loads(resp.text)
    logger.info(jsonText)

    if jsonText['Status'] == 'SUCCESS':
        return 'SUCCESS'
    else:
        return "FAIL"

#撥款
def approprivate_money_to_store(order_id):
    #測試
    # post_url = 'https://ccore.newebpay.com/API/ExportInstruct'
    # key = "Oq1IRY4RwYXpLAfmnmKkwd26bcT6q88q"
    # iv = "CeYa8zoA0mX4qBpP"
    #正式
    post_url = 'https://core.newebpay.com/API/ExportInstruct'
    key = "WXPufoC84rf6VgWVUmzrFaV0AeFEqVFZ"
    iv = "PtMc75C71vZUAhqC"

    PartnerID_ = "CARE168"

    timeStamp = int( time.time() )

    order = Order.objects.get(id=order_id)
    user = order.servant
    userStore = UserStore.objects.filter(user=user).first()

    MerchantID = userStore.MerchantID
    # key = userStore.MerchantHashKey
    # iv = userStore.MerchantIvKey

    data = {
            "Version": "1.0",
            "TimeStamp": timeStamp,
            "MerchantID" : MerchantID,
            "MerchantOrderNo": order.id,
            "Amount": order.total_money,     
        }

    logger.info(data)

    query_str = urllib.parse.urlencode(data)
    encrypt_data = module.aes256_cbc_encrypt(query_str, key, iv)

    resp = requests.post(post_url, data ={"PartnerID_":PartnerID_, "PostData_":encrypt_data})
    # resp.encoding = 'utf-8'
    # logger.info(resp.text)

    jsonText = json.loads(resp.text)
    logger.info(jsonText)

    if jsonText['Status'] == 'SUCCESS':
        return 'SUCCESS'
    else:
        return "FAIL"

#扣款
def debit_money_to_platform(order_id, platform_money):
    #測試
    # post_url = 'https://ccore.newebpay.com/API/ChargeInstruct'
    # key = "Oq1IRY4RwYXpLAfmnmKkwd26bcT6q88q"
    # iv = "CeYa8zoA0mX4qBpP"
    #正式 
    post_url = 'https://core.newebpay.com/API/ChargeInstruct'
    key = "WXPufoC84rf6VgWVUmzrFaV0AeFEqVFZ"
    iv = "PtMc75C71vZUAhqC"

    PartnerID_ = "CARE168"
    

    timeStamp = int( time.time() )

    order = Order.objects.get(id=order_id)
    user = order.servant
    userStore = UserStore.objects.filter(user=user).first()

    MerchantID = userStore.MerchantID
    # key = userStore.MerchantHashKey
    # iv = userStore.MerchantIvKey

    data = {
        "Version": "1.1",
        "TimeStamp": timeStamp,
        "MerchantID" : MerchantID,
        "Amount": platform_money,
        "FeeType": 0,
        "BalanceType": 0,
    }

    logger.info(data)

    query_str = urllib.parse.urlencode(data)
    encrypt_data = module.aes256_cbc_encrypt(query_str, key, iv)

    resp = requests.post(post_url, data ={"PartnerID_":PartnerID_, "PostData_":encrypt_data})
    # resp.encoding = 'utf-8'
    # logger.info(resp.text)

    jsonText = json.loads(resp.text)
    logger.info(jsonText)

    if jsonText['Status'] == 'SUCCESS':
        return 'SUCCESS'
    else:
        return "FAIL"

        
