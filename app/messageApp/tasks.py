from modelCore.models import ChatRoom ,ChatroomMessage ,ChatroomUserShip ,SystemMessage ,Order, SmsVerifyCode
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice
import requests
import math, random
from celery import shared_task
import environ

#====================================
### 推播訊息 1.收到訂單訊息(chatroom 文字圖片) 2.收到系統訊息
#====================================
#推播測試
def sendTest():
    message = Message(
        notification= Notification(title="title", body="text"),
        # data={
        #     "Nick" : "Mario",
        #     "body" : "great match!",
        #     "Room" : "PortugalVSDenmark"
        # }
    )
    devices = FCMDevice.objects.all()
    # for device in devices:
    #     print(device.name)
    devices.send_message(message)

def sendTaskMessage(user):
    message = Message(
        notification= Notification(title="新任務來囉！", body="回 app 接單~"),
    )
    devices = FCMDevice.objects.filter(user=user)
    devices.send_message(message)
    print("send fcm")

def sendFCMMessage(user,title,text):
    message = Message(
        notification= Notification(title=title, body=text),
    )
    devices = FCMDevice.objects.filter(user=user)
    devices.send_message(message)

#====================================
### 系統訊息
#====================================

# [服務者]收到訂單
def receiveBooking(user,order):
    content_text = "您收到來自"+ order.case.user.name +"的預訂申請，請利用聊聊與對方聯絡。"
    message = SystemMessage(case=order.case,user=user,order=order,content=content_text)
    message.save()
    if user.is_fcm_notify == True:
        sendFCMMessage(order.case.servant, '收到訂單', content_text)
    

# 需求者付款, [服務者]收到訂單成立
def servantOrderEstablished(user,order):
    content_text = "您已成功接案！"+ order.user.name +"的預定已成立～您可前往會員中心-我接的案查詢詳情。"
    message = SystemMessage(case=order.case,user=user,order=order,content=content_text)
    message.save()
    if user.is_fcm_notify == True:
        sendFCMMessage(order.servant, '訂單成立', content_text)
    

# [需求者] 收到服務者已接案
def neederOrderEstablished(user,order):
    content_text = "您的定單已成立！您可前往會員中心-訂單管理查詢詳情。"
    message = SystemMessage(case=order.case,order=order,user=order.user,content=content_text)
    message.save()
    if user.is_fcm_notify == True:
        sendFCMMessage(order.user, '訂單成立', content_text)
    

# [服務者] 收到訂單取消
def orderCancel(user,order):
    content_text = "很抱歉，"+ order.user.name +"的定單已取消，請您不用前往服務!"
    message = SystemMessage(case=order.case,user=user,order=order,content=content_text)
    message.save()
    if user.is_fcm_notify == True:
        sendFCMMessage(order.servant, '訂單取消', content_text)
    

# [服務者] 收到訂單提前結束
def orderEarlyTermination(user,order):
    content_text = "請注意！"+ order.user.name +"的定單已申請「提前結束」，確認交接完成，即可收班。"
    message = SystemMessage(case=order.case,order=order,user=user,content=content_text)
    message.save()
    if user.is_fcm_notify == True:
        sendFCMMessage(order.servant, '訂單提前結束', content_text)
    

#====================================
### 聊聊訊息 1.order狀態改變(訂單成立, 修改(x), 付款, 取消, 提前結束) 2.發文字訊息 or 圖片訊息(不用, 因為這個只出現在 chatroom 的場景)
#====================================

# 這邊先不要給推播
def changeOrderStateMessage(user,order,orderState):
    print('code')


#====================================
### 簡訊訊息
#====================================

def testSMS():
    print('test mitake sms')
    url = 'https://smsb2c.mitake.com.tw/b2c/mtk/SmSend?CharsetURL=UTF8'

    testString = "這個是一個測試 0012"
    
    env = environ.Env()
    environ.Env.read_env()

    params ={
        "username": env('SMS_USER_NAME'),
        "password": env('SMS_PASSWORD'),
        "dstaddr": "0912585506",
        "smbody": testString
    }

    resp = requests.post(url, params= params)

    print(resp.text)

def sendSMSCode(phone, code):
    url = 'https://smsb2c.mitake.com.tw/b2c/mtk/SmSend?CharsetURL=UTF8'

    theString = f"您的驗證碼為 {code}, 請盡快驗證~"

    env = environ.Env()
    environ.Env.read_env()

    params ={
        "username": env('SMS_USER_NAME'),
        "password": env('SMS_PASSWORD'),
        "dstaddr": phone,
        "smbody": theString
    }
    resp = requests.post(url, params= params)
    print(resp.text)

def randSmsVerifyCode(phone):
    smsVerifyCode = SmsVerifyCode()
    smsVerifyCode.phone = phone
    smsVerifyCode.code = generateOTP()
    smsVerifyCode.save()
    sendSMSCode(smsVerifyCode.phone, smsVerifyCode.code)
    expireSmsCode.apply_async(kwargs={'id': smsVerifyCode.id}, countdown=60)
    return smsVerifyCode.code

def smsSendPassword(phone, password):
    url = 'https://smsb2c.mitake.com.tw/b2c/mtk/SmSend?CharsetURL=UTF8'

    theString = f"您的臨時密碼為 {password}, 請盡快登入並修改~"

    env = environ.Env()
    environ.Env.read_env()

    params ={
        "username": env('SMS_USER_NAME'),
        "password": env('SMS_PASSWORD'),
        "dstaddr": phone,
        "smbody": theString
    }
    resp = requests.post(url, params= params)
    print(resp.text)

def generateOTP() :
    # Declare a digits variable 
    # which stores all digits
    digits = "0123456789"
    OTP = ""
 
    # length of password can be changed
    # by changing value in range
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    
    # ex.3211
    return OTP

@shared_task
def expireSmsCode(id):
    smsVerifyCode = SmsVerifyCode.objects.get(id=id)
    smsVerifyCode.is_expired = True
    smsVerifyCode.save()
