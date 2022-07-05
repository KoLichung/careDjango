import csv
import os
import datetime
from datetime import date ,timedelta
from pytz import timezone
import pytz
from .models import  User, City, County,Service,UserWeekDayTime,UserServiceShip ,Language ,UserLanguage , License, UserLicenseShipImage
from .models import  UserServiceLocation, Case, DiseaseCondition,BodyCondition,CaseDiseaseShip,CaseBodyConditionShip ,CaseWeekDayTime 
from .models import  CaseServiceShip ,Order ,Review ,PayInfo ,Message ,SystemMessage

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
    License.objects.create(name="COVID-19 疫苗接種記錄卡\n若未提供，服務者頁面會顯示「未提供」供預訂者參考")
    License.objects.create(name="一年內良民證-警察刑事紀錄證明書\n若未提供，服務者頁面會顯示「未提供」供預訂者參考")
    License.objects.create(name="一年內體檢表（需有B肝表面抗原 & 胸部 X 光）\n若未提供，服務者頁面會顯示「未提供」供預訂者參考")
    License.objects.create(name="照服員結業證書")
    License.objects.create(name="照服員單一級證照")
    License.objects.create(name="護理師證書")
    License.objects.create(name="護理相關畢業證書")
    License.objects.create(name="長照證明卡")
    License.objects.create(name="失智症 20 小時課程")
    License.objects.create(name="身心障礙 20 小時課程")
    License.objects.create(name="物理治療師證照")
    License.objects.create(name="職能治療師證照")

    Service.objects.create(name='急診室患者',is_increase_price=True)
    Service.objects.create(name='傳染性疾病',is_increase_price=True)
    Service.objects.create(name='體重超過 70 公斤',is_increase_price=True)
    Service.objects.create(name='體重超過 90 公斤',is_increase_price=True)
    Service.objects.create(name='安全維護 \n預防跌倒、陪同散步、推輪椅、心靈陪伴',is_increase_price=True)
    Service.objects.create(name='協助進食 \n用餐，按醫囑給藥',is_increase_price=True)
    Service.objects.create(name='協助如廁 \n大小便處理、更換尿布、會陰沖洗',is_increase_price=True)
    Service.objects.create(name='身體清潔 \n沐浴、擦澡',is_increase_price=True)
    Service.objects.create(name='陪同就醫 \n陪伴看診、洗腎，代領藥品',is_increase_price=True)
    Service.objects.create(name='陪同復健',is_increase_price=True)
    Service.objects.create(name='代購物品 \n代買生活必需品以有發票或收據為主；\n代購物品期間服務者無法負責安全維護，家屬需自行評估被照顧者狀況',is_increase_price=True)
    Service.objects.create(name='簡易備餐 \n依現有食材簡易煮粥、麵食或加熱即食品； \n僅提供被照顧者與一位家屬餐食',is_increase_price=True)
    Service.objects.create(name='家務協助 \n簡易掃地拖地，清洗衣物、床單',is_increase_price=True)
    Service.objects.create(name='鼻胃管灌食',is_increase_price=True)
    Service.objects.create(name='管路清潔',is_increase_price=True)
    Service.objects.create(name='翻身拍背 \n僅提供長期臥床或手術無法自行翻身的病人',is_increase_price=True)
    Service.objects.create(name='被動關節運動 \n僅提供長期臥床、癱瘓、昏迷或關節炎的病人； \n病人有骨質疏鬆症、骨折病史請告知',is_increase_price=True)
    Service.objects.create(name='協助移位',is_increase_price=True)

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
    user.is_alltime_service = True
    user.save()

    userWeekdayTIme = UserWeekDayTime()
    userWeekdayTIme.user = User.objects.get(id=2)
    userWeekdayTIme.weekday = '1'
    userWeekdayTIme.start_time = 8
    userWeekdayTIme.end_time = 20
    userWeekdayTIme.save()

    userWeekdayTIme = UserWeekDayTime()
    userWeekdayTIme.user = User.objects.get(id=3)
    userWeekdayTIme.weekday = '4'
    userWeekdayTIme.start_time = 10
    userWeekdayTIme.end_time = 19
    userWeekdayTIme.save()

    userWeekdayTIme = UserWeekDayTime()
    userWeekdayTIme.user = User.objects.get(id=4)
    userWeekdayTIme.weekday = '5'
    userWeekdayTIme.start_time = 9
    userWeekdayTIme.end_time = 21
    userWeekdayTIme.save()

    userServiceShip = UserServiceShip()
    userServiceShip.user = User.objects.get(id=2)
    userServiceShip.service = Service.objects.get(id=1)
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
    case.care_type = 'home'
    case.name = '王大明'
    case.gender = 'M'
    case.age = 70
    case.weight = 67
    case.disease_remark = 'Test'
    case.conditions_remark = 'Test'
    case.is_alltime_service = True
    case.start_datetime = datetime.datetime(2022,7,20).replace(tzinfo=pytz.UTC)
    case.end_datetime = datetime.datetime(2022,8,20).replace(tzinfo=pytz.UTC)
    case.save()

    case = Case()
    case.user = User.objects.get(id=3)
    case.servant = User.objects.get(id=4)
    case.county = County.objects.get(id=77)
    case.care_type = 'hospital'
    case.name = '陳小芬'
    case.gender = 'F'
    case.age = 72
    case.weight = 56
    case.is_open_for_search = True
    case.disease_remark = 'Test'
    case.conditions_remark = 'Test'
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

    caseWeektimeDay = CaseWeekDayTime()
    caseWeektimeDay.case = Case.objects.get(id=1)
    caseWeektimeDay.weekday = '5'
    caseWeektimeDay.start_time = 10
    caseWeektimeDay.end_time = 18
    caseWeektimeDay.save()

    caseWeektimeDay = CaseWeekDayTime()
    caseWeektimeDay.case = Case.objects.get(id=2)
    caseWeektimeDay.weekday = '3'
    caseWeektimeDay.start_time = 9
    caseWeektimeDay.end_time = 19
    caseWeektimeDay.save()
    
    caseServiceShip = CaseServiceShip()
    caseServiceShip.case = Case.objects.get(id=1)
    caseServiceShip.service = Service.objects.get(id=5)
    caseServiceShip.save()

    caseServiceShip = CaseServiceShip()
    caseServiceShip.case = Case.objects.get(id=2)
    caseServiceShip.service = Service.objects.get(id=9)
    caseServiceShip.save()

    order = Order()
    order.case = Case.objects.get(id=1)
    order.state = 'unPaid'
    order.total_money =(((Case.objects.get(id=1).end_datetime) - (Case.objects.get(id=1).start_datetime)).days) * (Case.objects.get(id=1).servant.home_one_day_wage)
    order.save()

    order = Order()
    order.case = Case.objects.get(id=2)
    order.state = 'paid'
    caseWeekDaytimes = CaseWeekDayTime.objects.filter(case=Case.objects.get(id=2))
    start_date = Case.objects.get(id=2).start_datetime.date()
    end_date = Case.objects.get(id=2).end_datetime.date()
    total_hours = 0
    for caseWeekDaytime in caseWeekDaytimes:
        total_hours += (days_count([int(caseWeekDaytime.weekday)], start_date, end_date)) * (caseWeekDaytime.end_time - caseWeekDaytime.start_time)
    print(total_hours)
    order.total_money = total_hours * (Case.objects.get(id=2).servant.hospital_hour_wage)
    order.save()

    review = Review()
    review.order = Order.objects.get(id=1)
    review.case_offender_rating = 4.8
    review.case_offender_comment = 'good'
    review.servant_rating = 5
    review.servant_comment = 'nice'
    review.save()

    review = Review()
    review.order = Order.objects.get(id=2)
    review.case_offender_rating = 4.5
    review.case_offender_comment = 'very good'
    review.servant_rating = 4.3
    review.servant_comment = 'very nice'
    review.save()

    message = Message()
    message.case = Case.objects.get(id=1)
    message.user = User.objects.get(id=2)
    message.content = 'Hello'
    message.save()

    message = Message()
    message.case = Case.objects.get(id=2)
    message.user = User.objects.get(id=3)
    message.content = 'Test'
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