from Crypto.Cipher import AES
import base64
import hashlib
import sys

class Cryptor:
    # Default Key for encryption
    rawkey = 'my-key-for-testing'
    rawiv = 'testing-iv'
    method = AES.MODE_CFB
    blocksize = 32  # 16, 32..etc
    padwith = '`'  # padding value for string
    # lambda function for padding
    pad = lambda self, s: s + (self.blocksize - len(s) % self.blocksize) * self.padwith
    
    def __init__(self, iv=None, key=None):

        self.key = key if key is not None else self.rawkey
        self.iv = key if iv is not None else self.rawiv

    def getKEY(self):

        if not self.key:
            sys.exit('key error')
        return hashlib.sha256(str(self.key).encode('utf-8')).hexdigest()[:32]

    def getIV(self):

        if not self.iv:
            sys.exit('iv error')
        return hashlib.sha256(str(self.iv).encode('utf-8')).hexdigest()[:16]

    def encrypt(self, text):

        cipher = AES.new(self.getKEY(), self.method, self.getIV(), segment_size=128)
        return base64.b64encode(cipher.encrypt(self.pad(text)))

    def decrypt(self, encrypted):
        
        encrypted = base64.b64decode(encrypted)
        cipher = AES.new(self.getKEY(), self.method, self.getIV(), segment_size=128)
        return str(cipher.decrypt(encrypted),  encoding = "utf-8").rstrip(self.padwith)
 
