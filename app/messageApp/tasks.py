from modelCore.models import ChatRoom ,Message ,ChatroomUserShip ,SystemMessage
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice


#====================================
### 推播訊息
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

#====================================
### 系統訊息
#====================================
def receiveBooking(user,order):
    message = SystemMessage(case=order.case,user=user,content="您收到來自"+ order.servant.name +"的預訂申請，請利用聊聊與對方聯絡。")
    message.save()
    print(message)

def servantOrderEstablished(user,order):
    message = SystemMessage(case=order.case,user=user,content="您已成功接案！"+ order.servant.name +"的預定已成立～您可前往會員中心-我接的案查詢詳情。")
    message.save()
    print(message)

def neederOrderEstablished(user,order):
    message = SystemMessage(case=order.case,user=user,content="您已成功預定！"+ order.servant.name +"服務者已接案～您可前往會員中心-訂單管理查詢詳情。")
    message.save()
    print(message)

def orderCancel(user,order):
    message = SystemMessage(case=order.case,user=user,content="很抱歉，"+ order.servant.name +"的定單已取消，請您不用前往服務!")
    message.save()
    print(message)

def orderEarlyTermination(user,order):
    message = SystemMessage(case=order.case,user=user,content="請注意！"+ order.servant.name +"的定單已申請「提前結束」，確認交接完成，即可收班。")
    message.save()
    print(message)