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
    TaxAmt = order.platform_money
    print(TaxAmt)
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
        'BuyerName':order.user.name,
        'PrintFlag':'Y',
        'TaxType':'1',
        'TaxRate':5,
        'Amt':(order.total_money - int(TaxAmt)),
        'TaxAmt':int(TaxAmt),
        'TotalAmt':order.total_money,
        'ItemName':'Care168平台服務費',
        'ItemCount':1,
        'ItemUnit':'項',
        'ItemPrice':order.total_money,
        'ItemAmt':order.total_money,
        'ItemTaxType':1,
    }
    
    logger.info(data)

    query_str = urllib.parse.urlencode(data)
    encrypt_data = module.aes256_cbc_encrypt(query_str, key, iv)
    resp = requests.post(post_url, data ={"MerchantID_":MerchantID_, "PostData_":encrypt_data})

    logger.info(json.loads(resp.text))
