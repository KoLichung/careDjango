from modelCore.models import Order
import requests
import time
import urllib.parse
import logging
import json
from newebpayApi import module

logger = logging.getLogger(__file__)

def send_invoice(order_id):

    order = Order.objects.get(id=order_id)
    post_url = 'https://cinv.ezpay.com.tw/Api/invoice_issue'
    timeStamp = int( time.time() )

    MerchantID_ = "35104311"
    key = "EESNrB33LHu6z705F5PXtBP3G06B4WhZ"
    iv = "Ca1cfkx7oJiAJWwP"

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

    query_str = urllib.parse.urlencode(data)
    encrypt_data = module.aes256_cbc_encrypt(query_str, key, iv)
    resp = requests.post(post_url, data ={"MerchantID_":MerchantID_, "PostData_":encrypt_data})

    jsonText = json.loads(resp.text)
    logger.info(jsonText)

    if jsonText['Status'] == 'SUCCESS':
        return 'SUCCESS'
    else:
        return "FAIL"
