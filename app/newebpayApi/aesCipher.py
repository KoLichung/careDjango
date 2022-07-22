from Crypto.Cipher import AES
import base64
import hashlib
import sys
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms
import binascii

class AESCipher:
    # Default Key for encryption
    # HashKey：Oq1IRY4RwYXpLAfmnmKkwd26bcT6q88q
    # HashIV：CeYa8zoA0mX4qBpP

    # $key="TTF0Fg1QxAOejgV1FZxXgWKQlO52njrO"; $iv="Cwah1NwceYk3PmKP";

    rawkey = 'TTF0Fg1QxAOejgV1FZxXgWKQlO52njrO'
    rawiv = 'Cwah1NwceYk3PmKP'
    method = AES.MODE_CBC
    blocksize = 32  # 16, 32..etc
    padwith = '`'  # padding value for string
    # lambda function for padding
    pad = lambda self, s: s + (self.blocksize - len(s) % self.blocksize) * self.padwith
    
    def __init__(self, iv=None, key=None):
        self.key = self.rawkey.encode()
        self.iv = self.rawiv.encode()
        self.mode = self.method

    # def getKEY(self):
    #     if not self.key:
    #         sys.exit('key error')
    #     return hashlib.sha256(str(self.key).encode('utf-8')).hexdigest()[:32]

    # def getIV(self):
    #     if not self.iv:
    #         sys.exit('iv error')
    #     return hashlib.sha256(str(self.iv).encode('utf-8')).hexdigest()[:16]

    def encrypt(self, text):
        # cipher = AES.new(self.getKEY(), self.method, self.getIV(), segment_size=128)
        cipher = AES.new(self.key, self.mode, self.iv)
        text= self.pkcs7_padding(text)
        # ciphertext = base64.b64encode(cipher.encrypt(text)).decode('utf8')
        ciphertext = binascii.b2a_hex(cipher.encrypt(text)).decode()
        return ciphertext

    # def decrypt(self, encrypted):
    #     encrypted = base64.b64decode(encrypted)
    #     cipher = AES.new(self.getKEY(), self.method, self.getIV(), segment_size=128)
    #     return str(cipher.decrypt(encrypted),  encoding = "utf-8").rstrip(self.padwith)

    @staticmethod
    def pkcs7_padding(data):
        if not isinstance(data, bytes):
            data = data.encode()

        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        return padded_data
 
