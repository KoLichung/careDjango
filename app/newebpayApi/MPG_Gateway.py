# -*- coding: utf-8 -*-
# MPG 多元付款交易

import time
import module
import urllib.parse
import webbrowser
import codecs

# 設定api網址、建立商店代號.key.iv
api_url = 'https://ccore.newebpay.com/MPG/mpg_gateway'
timeStamp = int( time.time() )
merchant_id = "MS336989148"
Version = "2.0"
key = "SKYfwec2P46Kzzgc8CrcblPzeX8r8jTH"
iv = "C6RhZZ45pflwEoSP"


# 建立MPG交易時要填入的資料、設定版本號(以信用卡一次付清為例)
test_data = {
            "Version": "2.0",
            "MerchantID" : "MS336989148",
            "RespondType": "JSON",
            "TimeStamp": timeStamp,
            "MerchantOrderNo":"202207300001",
            "Amt": 3000,
            "ItemDesc": "test",       
            
        }


# 將資料編成搜尋字串，並依照不同加密模式進行加密及SHA256壓碼
query_str = urllib.parse.urlencode(test_data)
encrypt_data = module.aes256_cbc_encrypt(query_str, key, iv)
hashs = module.sha256_hash(encrypt_data, key, iv)


# 建立POST參數並帶入MPG
params = {
    "MerchantID": merchant_id,
    "TradeInfo": encrypt_data,
    "TradeSha": hashs,
    "Version": test_data["Version"],
}


# 建立測試用的web頁面，將POST參數代入
with open("MPG.html", 'w', encoding="utf-8") as f:
    html_string = f"<!DOCTYPE html><head><meta charset='utf-8'><title>MPG</title></head><body><form name='Newebpay' method='post' action={api_url}>測試URL: {api_url}<p>MerchantID:<input type='text' name='MerchantID' value={params['MerchantID']}><br><br>TradeInfo:<input type='text' name='TradeInfo' value={params['TradeInfo']}><br><br>TradeSha:<input type='text' name='TradeSha' value={params['TradeSha']}><br><br>Version:<input type='text' name='Version' value={params['Version']}><br><br><input type='submit' value='Submit'></form></body></html>"
    f.write(html_string)

webbrowser.open("../../MPG.html", "r")
