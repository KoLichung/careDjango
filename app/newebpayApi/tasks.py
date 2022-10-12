
from modelCore.models import Order

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