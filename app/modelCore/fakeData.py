import csv
import os
import datetime
from datetime import date ,timedelta
from pytz import timezone
import pytz
from django.db.models import Sum
from .models import  ChatroomUserShip, User, City, County,Service,UserWeekDayTime,UserServiceShip ,Language ,UserLanguage , License, UserLicenseShipImage
from .models import  UserServiceLocation, Case, DiseaseCondition,BodyCondition,CaseDiseaseShip,CaseBodyConditionShip ,ChatRoom , ChatroomUserShip
from .models import  CaseServiceShip ,Order ,Review ,PayInfo ,Message ,SystemMessage ,OrderWeekDay ,OrderIncreaseService

def importCityCounty():
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'county.csv')

    file = open(file_path)
    reader = csv.reader(file, delimiter=',')
    for index, row in enumerate(reader):
        if index != 0:
            if City.objects.filter(name=row[0]).count()==0:
                city = City()
                city.name = row[0]
                city.newebpay_cityname = row[6]
                city.save()
            else:
                city = City.objects.get(name=row[0])

            county_name = row[2].replace(row[0],'')
            county = County()
            county.city = city
            county.name = county_name
            county.save()
            print(city.name + " " + county.name)

def seedData():
    License.objects.create(name="身分證正面")
    License.objects.create(name="身分證反面")
    License.objects.create(name="健保卡正面")
    License.objects.create(name="COVID-19 疫苗接種記錄卡",remark="若未提供，服務者頁面會顯示「未提供」供預訂者參考")
    License.objects.create(name="一年內良民證-警察刑事紀錄證明書",remark="若未提供，服務者頁面會顯示「未提供」供預訂者參考")
    License.objects.create(name="一年內體檢表（需有B肝表面抗原 & 胸部 X 光）",remark="若未提供，服務者頁面會顯示「未提供」供預訂者參考")
    License.objects.create(name="照服員結業證書")
    License.objects.create(name="照服員單一級證照")
    License.objects.create(name="護理師證書")
    License.objects.create(name="護理相關畢業證書")
    License.objects.create(name="長照證明卡")
    License.objects.create(name="失智症 20 小時課程")
    License.objects.create(name="身心障礙 20 小時課程")
    License.objects.create(name="物理治療師證照")
    License.objects.create(name="職能治療師證照")

    Service.objects.create(name="急診室患者",is_increase_price=True)
    Service.objects.create(name="傳染性疾病",is_increase_price=True)
    Service.objects.create(name="體重超過 70 公斤",is_increase_price=True)
    Service.objects.create(name="體重超過 90 公斤",is_increase_price=True)
    Service.objects.create(name="安全維護",remark="預防跌倒、陪同散步、推輪椅、心靈陪伴")
    Service.objects.create(name="協助進食",remark="用餐，按醫囑給藥")
    Service.objects.create(name="協助如廁",remark="大小便處理、更換尿布、會陰沖洗")
    Service.objects.create(name="身體清潔",remark="沐浴、擦澡")
    Service.objects.create(name="陪同就醫",remark="陪伴看診、洗腎，代領藥品")
    Service.objects.create(name="陪同復健")
    Service.objects.create(name="代購物品",remark="代買生活必需品以有發票或收據為主；代購物品期間服務者無法負責安全維護，家屬需自行評估被照顧者狀況")
    Service.objects.create(name="簡易備餐",remark="依現有食材簡易煮粥、麵食或加熱即食品；僅提供被照顧者與一位家屬餐食")
    Service.objects.create(name="家務協助",remark="簡易掃地拖地，清洗衣物、床單")
    Service.objects.create(name="鼻胃管灌食")
    Service.objects.create(name="管路清潔")
    Service.objects.create(name="翻身拍背",remark="僅提供長期臥床或手術無法自行翻身的病人")
    Service.objects.create(name="被動關節運動",remark="僅提供長期臥床、癱瘓、昏迷或關節炎的病人； 病人有骨質疏鬆症、骨折病史請告知")
    Service.objects.create(name="協助移位")

    Language.objects.create(name="國語")
    Language.objects.create(name="台語")
    Language.objects.create(name="客家話")
    Language.objects.create(name="粵語")
    Language.objects.create(name="原住民語")
    Language.objects.create(name="日文")
    Language.objects.create(name="英文")
    Language.objects.create(name="其他")

    DiseaseCondition.objects.create(name='無')
    DiseaseCondition.objects.create(name='關節炎')
    DiseaseCondition.objects.create(name='癌症')
    DiseaseCondition.objects.create(name='骨質酥鬆症')
    DiseaseCondition.objects.create(name='手術照顧')
    DiseaseCondition.objects.create(name='心臟病')
    DiseaseCondition.objects.create(name='骨折')
    DiseaseCondition.objects.create(name='敗血症')
    DiseaseCondition.objects.create(name='高血壓')
    DiseaseCondition.objects.create(name='肺炎')
    DiseaseCondition.objects.create(name='糖尿病')
    DiseaseCondition.objects.create(name='褥瘡')
    DiseaseCondition.objects.create(name='失智症')
    DiseaseCondition.objects.create(name='帕金森氏症')
    DiseaseCondition.objects.create(name='中風')
    DiseaseCondition.objects.create(name='精神疾病')
    DiseaseCondition.objects.create(name='腎臟病')
    DiseaseCondition.objects.create(name='癲癇')

    BodyCondition.objects.create(name='無')
    BodyCondition.objects.create(name='鼻胃管')
    BodyCondition.objects.create(name='使用輔具')
    BodyCondition.objects.create(name='尿管')
    BodyCondition.objects.create(name='長期臥床')
    BodyCondition.objects.create(name='氣切管')
    BodyCondition.objects.create(name='傷口')
    BodyCondition.objects.create(name='腸造口 - 人工肛門')
    BodyCondition.objects.create(name='昏迷')
    BodyCondition.objects.create(name='胃造口')

def fakeData():
    user = User()
    user.name = 'user01'
    user.phone = '0915323131'
    user.gender = 'M'
    user.save()

    user = User()
    user.name = 'user02'
    user.phone = '0985463816'
    user.gender = 'M'
    user.is_servant = True
    user.is_home = True
    user.home_hour_wage = 300
    user.home_half_day_wage = 1600
    user.home_one_day_wage = 2900
    user.is_continuous_time = True
    user.save()

    user = User()
    user.name = 'user03'
    user.phone = '0985463888'
    user.gender = 'F'
    user.is_servant = True
    user.is_hospital = True
    user.hospital_hour_wage = 320
    user.hospital_half_day_wage = 1750
    user.hospital_one_day_wage = 3200
    user.save()

    userWeekdayTIme = UserWeekDayTime()
    userWeekdayTIme.user = User.objects.get(id=4)
    userWeekdayTIme.weekday = '2'
    userWeekdayTIme.start_time = 9
    userWeekdayTIme.end_time = 21
    userWeekdayTIme.save()

    userWeekdayTIme = UserWeekDayTime()
    userWeekdayTIme.user = User.objects.get(id=4)
    userWeekdayTIme.weekday = '4'
    userWeekdayTIme.start_time = 9
    userWeekdayTIme.end_time = 21
    userWeekdayTIme.save()

    userWeekdayTIme = UserWeekDayTime()
    userWeekdayTIme.user = User.objects.get(id=4)
    userWeekdayTIme.weekday = '5'
    userWeekdayTIme.start_time = 9
    userWeekdayTIme.end_time = 21
    userWeekdayTIme.save()

    userWeekdayTIme = UserWeekDayTime()
    userWeekdayTIme.user = User.objects.get(id=4)
    userWeekdayTIme.weekday = '6'
    userWeekdayTIme.start_time = 9
    userWeekdayTIme.end_time = 21
    userWeekdayTIme.save()

    userServiceShip = UserServiceShip()
    userServiceShip.user = User.objects.get(id=2)
    userServiceShip.service = Service.objects.get(id=1)
    userServiceShip.save()

    userServiceShip = UserServiceShip()
    userServiceShip.user = User.objects.get(id=3)
    userServiceShip.service = Service.objects.get(id=1)
    userServiceShip.increase_percent = 15
    userServiceShip.save()

    userServiceShip = UserServiceShip()
    userServiceShip.user = User.objects.get(id=3)
    userServiceShip.service = Service.objects.get(id=4)
    userServiceShip.increase_percent = 20
    userServiceShip.save()

    userServiceShip = UserServiceShip()
    userServiceShip.user = User.objects.get(id=3)
    userServiceShip.service = Service.objects.get(id=5)
    userServiceShip.save()

    userServiceShip = UserServiceShip()
    userServiceShip.user = User.objects.get(id=4)
    userServiceShip.service = Service.objects.get(id=9)
    userServiceShip.save()

    userLanguage = UserLanguage()
    userLanguage.user = User.objects.get(id=2)
    userLanguage.language = Language.objects.get(id=3)
    userLanguage.save()

    userLanguage = UserLanguage()
    userLanguage.user = User.objects.get(id=3)
    userLanguage.language = Language.objects.get(id=6)
    userLanguage.save()

    userLanguage = UserLanguage()
    userLanguage.user = User.objects.get(id=4)
    userLanguage.language = Language.objects.get(id=7)
    userLanguage.save()

    userLicenseshipImage = UserLicenseShipImage()
    userLicenseshipImage.user = User.objects.get(id=2)
    userLicenseshipImage.license = License.objects.get(id=4)
    userLicenseshipImage.save()

    userLicenseshipImage = UserLicenseShipImage()
    userLicenseshipImage.user = User.objects.get(id=3)
    userLicenseshipImage.license = License.objects.get(id=6)
    userLicenseshipImage.save()

    userLicenseshipImage = UserLicenseShipImage()
    userLicenseshipImage.user = User.objects.get(id=4)
    userLicenseshipImage.license = License.objects.get(id=10)
    userLicenseshipImage.save()

    userserviceLocation = UserServiceLocation()
    userserviceLocation.user = User.objects.get(id=2)
    userserviceLocation.county = County.objects.get(id=20)
    userserviceLocation.city = userserviceLocation.county.city
    userserviceLocation.tranfer_fee = 200
    userserviceLocation.save()

    userserviceLocation = UserServiceLocation()
    userserviceLocation.user = User.objects.get(id=3)
    userserviceLocation.county = County.objects.get(id=35)
    userserviceLocation.city = userserviceLocation.county.city
    userserviceLocation.tranfer_fee = 300
    userserviceLocation.save()

    userserviceLocation = UserServiceLocation()
    userserviceLocation.user = User.objects.get(id=4)
    userserviceLocation.county = County.objects.get(id=77)
    userserviceLocation.city = userserviceLocation.county.city
    userserviceLocation.tranfer_fee = 450
    userserviceLocation.save()

    case = Case()
    case.user = User.objects.get(id=2)
    case.servant = User.objects.get(id=3)
    case.county = County.objects.get(id=35)
    case.city = case.county.city
    case.care_type = 'home'
    case.name = '王大明'
    case.gender = 'M'
    case.age = 70
    case.weight = 67
    case.disease_remark = 'Test'
    case.conditions_remark = 'Test'
    case.is_continuous_time = True
    case.weekday =  '1,3,5'
    case.start_time = 10
    case.end_time = 19
    case.start_datetime = datetime.datetime(2022,7,20).replace(tzinfo=pytz.UTC)
    case.end_datetime = datetime.datetime(2022,8,20).replace(tzinfo=pytz.UTC)
    case.save()

    case = Case()
    case.user = User.objects.get(id=3)
    case.servant = User.objects.get(id=4)
    case.county = County.objects.get(id=77)
    case.city = case.county.city
    case.care_type = 'hospital'
    case.name = '陳小芬'
    case.gender = 'F'
    case.age = 72
    case.weight = 56
    case.is_open_for_search = True
    case.disease_remark = 'Test'
    case.conditions_remark = 'Test'
    case.weekday =  '2,4,6'
    case.start_time = 11
    case.end_time = 20
    case.start_datetime = datetime.datetime(2022,7,10).replace(tzinfo=pytz.UTC)
    case.end_datetime = datetime.datetime(2022,8,5).replace(tzinfo=pytz.UTC)
    case.save()

    caseDiseaseShip = CaseDiseaseShip()
    caseDiseaseShip.case = Case.objects.get(id=1)
    caseDiseaseShip.disease = DiseaseCondition.objects.get(id=4)
    caseDiseaseShip.save()

    caseDiseaseShip = CaseDiseaseShip()
    caseDiseaseShip.case = Case.objects.get(id=2)
    caseDiseaseShip.disease = DiseaseCondition.objects.get(id=15)
    caseDiseaseShip.save()

    caseBodyconditionShip = CaseBodyConditionShip()
    caseBodyconditionShip.case = Case.objects.get(id=1)
    caseBodyconditionShip.body_condition = BodyCondition.objects.get(id=3)
    caseBodyconditionShip.save()
    
    caseBodyconditionShip = CaseBodyConditionShip()
    caseBodyconditionShip.case = Case.objects.get(id=2)
    caseBodyconditionShip.body_condition = BodyCondition.objects.get(id=7)
    caseBodyconditionShip.save()

    caseServiceShip = CaseServiceShip()
    caseServiceShip.case = Case.objects.get(id=1)
    caseServiceShip.service = Service.objects.get(id=2)
    caseServiceShip.increase_percent = 30
    caseServiceShip.save()

    caseServiceShip = CaseServiceShip()
    caseServiceShip.case = Case.objects.get(id=1)
    caseServiceShip.service = Service.objects.get(id=3)
    caseServiceShip.increase_percent = 25
    caseServiceShip.save()
    
    caseServiceShip = CaseServiceShip()
    caseServiceShip.case = Case.objects.get(id=1)
    caseServiceShip.service = Service.objects.get(id=5)
    caseServiceShip.save()

    caseServiceShip = CaseServiceShip()
    caseServiceShip.case = Case.objects.get(id=2)
    caseServiceShip.service = Service.objects.get(id=1)
    caseServiceShip.increase_percent = 20
    caseServiceShip.save()

    caseServiceShip = CaseServiceShip()
    caseServiceShip.case = Case.objects.get(id=2)
    caseServiceShip.service = Service.objects.get(id=4)
    caseServiceShip.increase_percent = 25
    caseServiceShip.save()

    caseServiceShip = CaseServiceShip()
    caseServiceShip.case = Case.objects.get(id=2)
    caseServiceShip.service = Service.objects.get(id=9)
    caseServiceShip.save()

    order = Order()
    order.case = Case.objects.get(id=1)
    order.user = order.case.user
    order.servant = order.case.servant
    order.state = 'unPaid'
    order.start_time = order.case.start_time
    order.end_time = order.case.end_time
    order.start_datetime = order.case.start_datetime
    order.end_datetime = order.case.end_datetime
    order.base_money =(((Case.objects.get(id=1).end_datetime) - (Case.objects.get(id=1).start_datetime)).days) * (Case.objects.get(id=1).servant.home_one_day_wage)
    total_hours = 0
    for i in range(7):
        total_hours += (days_count([int(i)], order.start_datetime.date(), order.end_datetime.date())) * (order.end_time - order.start_time)
    order.work_hours = total_hours
    order.platform_percent = 15
    order.save()
    Review.objects.create(order=order,case=order.case,servant=order.case.servant,
                        case_offender_rating=4.8,case_offender_comment='good',
                        servant_rating=5,servant_comment='nice')

    order = Order()
    order.case = Case.objects.get(id=2)
    order.user = order.case.user
    order.servant = order.case.servant
    order.state = 'paid'
    order.start_datetime = Case.objects.get(id=2).start_datetime
    order.end_datetime = Case.objects.get(id=2).end_datetime
    order.start_time = order.case.start_time
    order.end_time = order.case.end_time
    order.save()
    weekdays = order.case.weekday.split(',')
    for weekday in weekdays:
        orderWeekday = OrderWeekDay()
        orderWeekday.order = order
        orderWeekday.weekday = weekday
        orderWeekday.save()
    weekday_list = list(OrderWeekDay.objects.filter(order=order).values_list('weekday', flat=True))
    total_hours = 0
    for i in weekday_list:
        total_hours += (days_count([int(i)], order.start_datetime.date(), order.end_datetime.date())) * (order.end_time - order.start_time)
    order.work_hours = total_hours
    order.base_money = order.work_hours * order.case.servant.hospital_hour_wage
    order.platform_percent = 15
    order.save()
    Review.objects.create(order=order,case=order.case,servant=order.case.servant)

    orderIncreaseService = OrderIncreaseService()
    orderIncreaseService.order = Order.objects.get(id=1)
    orderIncreaseService.service = Service.objects.get(id=2)
    orderIncreaseService.increase_percent = 15
    orderIncreaseService.increase_money = (Order.objects.get(id=1).base_money) * (orderIncreaseService.increase_percent)/100
    orderIncreaseService.save()

    orderIncreaseService = OrderIncreaseService()
    orderIncreaseService.order = Order.objects.get(id=1)
    orderIncreaseService.service = Service.objects.get(id=3)
    orderIncreaseService.increase_percent = 25
    orderIncreaseService.increase_money = (Order.objects.get(id=1).base_money) * (orderIncreaseService.increase_percent)/100
    orderIncreaseService.save()

    orderIncreaseService = OrderIncreaseService()
    orderIncreaseService.order = Order.objects.get(id=2)
    orderIncreaseService.service = Service.objects.get(id=1)
    orderIncreaseService.increase_percent = 20
    orderIncreaseService.increase_money = (Order.objects.get(id=1).base_money) * (orderIncreaseService.increase_percent)/100
    orderIncreaseService.save()

    orderIncreaseService = OrderIncreaseService()
    orderIncreaseService.order = Order.objects.get(id=2)
    orderIncreaseService.service = Service.objects.get(id=4)
    orderIncreaseService.increase_percent = 30
    orderIncreaseService.increase_money = (Order.objects.get(id=1).base_money) * (orderIncreaseService.increase_percent)/100
    orderIncreaseService.save()

    for order in Order.objects.all():
        order.total_money = ((order.base_money) + (OrderIncreaseService.objects.filter(order=order,service__is_increase_price=True).aggregate(Sum('increase_money'))['increase_money__sum'])) * ((100 - order.platform_percent)/100)
        order.platform_money = order.total_money * (order.platform_percent/100)
        order.save()

    ChatRoom.objects.create(update_at=datetime.datetime.now())
    ChatRoom.objects.create(update_at=datetime.datetime.now())

    ChatroomUserShip.objects.create(user=User.objects.get(id=2),chatroom=ChatRoom.objects.get(id=1))
    ChatroomUserShip.objects.create(user=User.objects.get(id=3),chatroom=ChatRoom.objects.get(id=1))
    ChatroomUserShip.objects.create(user=User.objects.get(id=3),chatroom=ChatRoom.objects.get(id=2))
    ChatroomUserShip.objects.create(user=User.objects.get(id=4),chatroom=ChatRoom.objects.get(id=2))
    
    message = Message()
    chatroom = ChatRoom.objects.get(id=1)
    message.chatroom = chatroom
    message.user = User.objects.get(id=3)
    message.content = 'Hello'
    chatroom.update_at = datetime.datetime.now()
    chatroom.save()
    message.save()

    message = Message()
    chatroom = ChatRoom.objects.get(id=1)
    message.chatroom = chatroom
    message.user = User.objects.get(id=2)
    message.is_this_message_only_case = True
    message.case = Case.objects.get(id=1)
    chatroom.update_at = datetime.datetime.now()
    chatroom.save()
    message.save()

    message = Message()
    chatroom = ChatRoom.objects.get(id=2)
    message.chatroom = chatroom
    message.user = User.objects.get(id=3)
    message.content = 'Hello'
    chatroom.update_at = datetime.datetime.now()
    chatroom.save()
    message.save()
    
    systemMessage = SystemMessage()
    systemMessage.user = User.objects.get(id=2)
    systemMessage.case = Case.objects.get(id=1)
    systemMessage.content = 'SystemTest01'
    systemMessage.save()

    systemMessage = SystemMessage()
    systemMessage.user = User.objects.get(id=3)
    systemMessage.case = Case.objects.get(id=2)
    systemMessage.content = 'SystemTest02'
    systemMessage.save()

def days_count(weekdays: list, start: date, end: date):
    dates_diff = end-start
    days = [start + timedelta(days=i) for i in range(dates_diff.days)]
    return len([day for day in days if day.weekday() in weekdays])