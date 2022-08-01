# -*- coding: utf-8 -*-
import hashlib
import binascii
from Crypto.Cipher import AES
from Crypto.Cipher.AES import MODE_GCM, MODE_CBC
from Crypto.Util.Padding import pad, unpad


# AES256-CBC加密 (parameter=dic型態的參數, key=商店HashKey, iv=商店HashIV)
def aes256_cbc_encrypt(parameter, key, iv):
    parameter, key, iv = parameter.encode(), key.encode(), iv.encode()
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    encrypt_data = str(binascii.b2a_hex(cipher.encrypt(
        pad(parameter, block_size=32))), "utf-8")
    return encrypt_data


# AES256-CBC解密 (encrypt_data=交易完成系統回傳之參數, key=商店HashKey, iv=商店HashIV)
def aes256_cbc_decrypt(encrypt_data, key, iv):
    encrypt_data, key, iv = encrypt_data.encode(), key.encode(), iv.encode()
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    parameter = unpad(cipher.decrypt(binascii.a2b_hex(
        encrypt_data)), block_size=32).decode("utf-8")
    return parameter


# SHA256壓碼 (TradeInfo=AES256加密後的值, key=商店HashKey, iv=商店HashIV)
def sha256_hash(TradeInfo, key, iv):
    TradeValue = "HashKey=" + key + "&" + TradeInfo + "&" + "HashIV=" + iv
    hashs = hashlib.sha256(TradeValue.encode("utf-8")).hexdigest()
    hashs = str.upper(hashs)
    return hashs


