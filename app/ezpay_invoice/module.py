import base64
from Crypto.Cipher import AES

def AES_Encrypt(key,iv, data):
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, iv.encode('utf8'))
    pad = lambda s: s + (16 - len(s)%16) * chr(16 - len(s)%16)
    data = pad(data)
    encryptedbytes = cipher.encrypt(data.encode('utf8'))
    encodestrs = base64.b64encode(encryptedbytes)
    enctext = encodestrs.decode('utf8')
    return enctext

def AES_Decrypt(key,iv, data):
    data = data.encode('utf8')
    encodebytes = base64.decodebytes(data)
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, iv.encode('utf8'))
    text_decrypted = cipher.decrypt(encodebytes)
    unpad = lambda s: s[0:-s[-1]]
    text_decrypted = unpad(text_decrypted)
    text_decrypted = text_decrypted.decode('utf8')
    return text_decrypted











