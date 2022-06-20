import csv
import os
import datetime 
from datetime import timedelta
from .models import User, MarkupItem, Category, LanguageSkill, License, Servant, ServantMarkupItemPrice, ServantSkillShip, ServantLicenseShipImage, ServantCategoryShip, Recipient, ServiceItem, City, CityArea, Transportation, Case,OrderState, Order, OrderReview , CaseServiceItemShip 



            

def fakeData():
    user = User()
    user.name = 'customer01'
    user.phone = '0915323131'
    user.is_active = True
    user.is_staff =  False
    user.save()

    user = User()
    user.name = 'customer02'
    user.phone = '0985463816'
    user.is_active = True
    user.is_staff =  False
    user.save()

    user = User.objects.all()[0]

    item = MarkupItem()
    item.name = '急診室'
    item.save()

    item = MarkupItem()
    item.name = '傳播性疾病'
    item.save()

    item = MarkupItem()
    item.name = '體重超過 70 公斤'
    item.save()

    item = MarkupItem()
    item.name = '體重超過 90 公斤'
    item.save()

    category = Category()
    category.care_type = '居家照顧'
    category.time_type = '連續時間'
    category.save()

    category = Category()
    category.care_type = '居家照顧'
    category.time_type = '每週時段預定'
    category.save()

    category = Category()
    category.care_type = '醫院看護'
    category.time_type = '連續時間'
    category.save()

    category = Category()
    category.care_type = '醫院看護'
    category.time_type = '每週時段預定'
    category.save()

    skill = LanguageSkill()
    skill.name = '國語'
    skill.save()

    skill = LanguageSkill()
    skill.name = '台語'
    skill.save()

    skill = LanguageSkill()
    skill.name = '客家話'
    skill.save()

    skill = LanguageSkill()
    skill.name = '粵語'
    skill.save()

    license = License()
    license.name = 'COVID-19 疫苗接種記錄卡 /n若未提供，服務者頁面會顯示「未提供」供預訂者參考'
    license.save()

    license = License()
    license.name = '一年內良民證-警察刑事紀錄證明書 /n若未提供，服務者頁面會顯示「未提供」供預訂者參考'
    license.save()

    license = License()
    license.name = '一年內體檢表（需有B肝表面抗原 & 胸部 X 光）/n若未提供，服務者頁面會顯示「未提供」供預訂者參考'
    license.save()
    
    license = License()
    license.name = '照服員結業證書'
    license.save()
    
    license = License()
    license.name = '照服員單一級證照'
    license.save()
    
    license = License()
    license.name = '護理師證書'
    license.save()
    
    license = License()
    license.name = '護理相關畢業證書'
    license.save()

    servant = Servant()
    servant.name = 'servant01'
    servant.gender = 'Male'
    servant.hourly_wage = 250
    servant.halfday_wage = 1500
    servant.oneday_wage = 3300
    servant.info = 'test'
    servant.save()

    servant = Servant()
    servant.name = 'servant02'
    servant.gender = 'Male'
    servant.hourly_wage = 230
    servant.halfday_wage = 1400
    servant.oneday_wage = 3000
    servant.info = 'test'
    servant.save()

    servant = Servant()
    servant.name = 'servant03'
    servant.gender = 'Female'
    servant.hourly_wage = 280
    servant.halfday_wage = 1700
    servant.oneday_wage = 3500
    servant.info = 'test'
    servant.save()

    markup_price = ServantMarkupItemPrice()
    markup_price.servant = Servant.objects.get(id=1)
    markup_price.markup_item = MarkupItem.objects.get(id=2)
    markup_price.price = 1.25
    markup_price.save()

    markup_price = ServantMarkupItemPrice()
    markup_price.servant = Servant.objects.get(id=2)
    markup_price.markup_item = MarkupItem.objects.get(id=4)
    markup_price.price = 1.45
    markup_price.save()

    markup_price = ServantMarkupItemPrice()
    markup_price.servant = Servant.objects.get(id=3)
    markup_price.markup_item = MarkupItem.objects.get(id=1)
    markup_price.price = 1.3
    markup_price.save()

    servantskill = ServantSkillShip()
    servantskill.servant = Servant.objects.get(id=1)
    servantskill.skill = LanguageSkill.objects.get(id=1)
    servantskill.save()
    
    servantskill = ServantSkillShip()
    servantskill.servant = Servant.objects.get(id=1)
    servantskill.skill = LanguageSkill.objects.get(id=3)
    servantskill.save()
    
    servantskill = ServantSkillShip()
    servantskill.servant = Servant.objects.get(id=1)
    servantskill.skill = LanguageSkill.objects.get(id=4)
    servantskill.save()
    
    servantskill = ServantSkillShip()
    servantskill.servant = Servant.objects.get(id=2)
    servantskill.skill = LanguageSkill.objects.get(id=1)
    servantskill.save()
    
    servantskill = ServantSkillShip()
    servantskill.servant = Servant.objects.get(id=2)
    servantskill.skill = LanguageSkill.objects.get(id=2)
    servantskill.save()

    servantskill = ServantSkillShip()
    servantskill.servant = Servant.objects.get(id=3)
    servantskill.skill = LanguageSkill.objects.get(id=1)
    servantskill.save()

    servantskill = ServantSkillShip()
    servantskill.servant = Servant.objects.get(id=3)
    servantskill.skill = LanguageSkill.objects.get(id=2)
    servantskill.save()

    servantskill = ServantSkillShip()
    servantskill.servant = Servant.objects.get(id=3)
    servantskill.skill = LanguageSkill.objects.get(id=4)
    servantskill.save()

    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=1)
    servantlicense.license = License.objects.get(id=1)
    servantlicense.save()

    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=1)
    servantlicense.license = License.objects.get(id=3)
    servantlicense.save()

    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=1)
    servantlicense.license = License.objects.get(id=5)
    servantlicense.save()

    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=1)
    servantlicense.license = License.objects.get(id=7)
    servantlicense.save()

    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=2)
    servantlicense.license = License.objects.get(id=1)
    servantlicense.save()

    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=2)
    servantlicense.license = License.objects.get(id=4)
    servantlicense.save()

    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=3)
    servantlicense.license = License.objects.get(id=3)
    servantlicense.save()

    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=3)
    servantlicense.license = License.objects.get(id=5)
    servantlicense.save()

    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=3)
    servantlicense.license = License.objects.get(id=6)
    servantlicense.save()

    servantcategory = ServantCategoryShip()
    servantcategory.servant = Servant.objects.get(id=1)
    servantcategory.category = Category.objects.get(id=1)
    servantcategory.save()
    
    servantcategory = ServantCategoryShip()
    servantcategory.servant = Servant.objects.get(id=1)
    servantcategory.category = Category.objects.get(id=4)
    servantcategory.save()
    
    servantcategory = ServantCategoryShip()
    servantcategory.servant = Servant.objects.get(id=2)
    servantcategory.category = Category.objects.get(id=2)
    servantcategory.save()
    
    servantcategory = ServantCategoryShip()
    servantcategory.servant = Servant.objects.get(id=3)
    servantcategory.category = Category.objects.get(id=3)
    servantcategory.save()
    
    servantcategory = ServantCategoryShip()
    servantcategory.servant = Servant.objects.get(id=3)
    servantcategory.category = Category.objects.get(id=4)
    servantcategory.save()

    recipient = Recipient()
    recipient.name = 'recipient01'
    recipient.customer = User.objects.get(id=2)
    recipient.gender = 'Male'
    recipient.age = 65
    recipient.weight = 70
    recipient.disease = '無'
    recipient.disease_info = 'test'
    recipient.save()

    recipient = Recipient()
    recipient.name = 'recipient02'
    recipient.customer = User.objects.get(id=2)
    recipient.gender = 'Male'
    recipient.age = 65
    recipient.weight = 70
    recipient.disease = '無'
    recipient.disease_info = 'test'
    recipient.save()

    recipient = Recipient()
    recipient.name = 'recipient03'
    recipient.customer = User.objects.get(id=2)
    recipient.gender = 'Male'
    recipient.age = 80
    recipient.weight = 67
    recipient.disease = '關節炎'
    recipient.disease_info = 'test'
    recipient.save()

    recipient = Recipient()
    recipient.name = 'recipient04'
    recipient.customer = User.objects.get(id=3)
    recipient.gender = 'Female'
    recipient.age = 70
    recipient.weight = 55
    recipient.disease = '糖尿病'
    recipient.disease_info = 'test'
    recipient.save()

    recipient = Recipient()
    recipient.name = 'recipient05'
    recipient.customer = User.objects.get(id=3)
    recipient.gender = 'Male'
    recipient.age = 68
    recipient.weight = 95
    recipient.disease = '心臟病'
    recipient.disease_info = 'test'
    recipient.save()

    recipient = Recipient()
    recipient.name = 'recipient06'
    recipient.customer = User.objects.get(id=3)
    recipient.gender = 'Female'
    recipient.age = 72
    recipient.weight = 60
    recipient.disease = '手術照顧'
    recipient.disease_info = 'test'
    recipient.save()

    serviceitem = ServiceItem()
    serviceitem.name = '安全維護'
    serviceitem.info = '預防跌倒、陪同散步、推輪椅、心靈陪伴'
    serviceitem.save()
    
    serviceitem = ServiceItem()
    serviceitem.name = '協助進食 '
    serviceitem.info = '用餐，按醫囑給藥'
    serviceitem.save()
    
    serviceitem = ServiceItem()
    serviceitem.name = '協助如廁 '
    serviceitem.info = '大小便處理、更換尿布、會陰沖洗'
    serviceitem.save()
    
    serviceitem = ServiceItem()
    serviceitem.name = '身體清潔 '
    serviceitem.info = '沐浴、擦澡'
    serviceitem.save()
    
    serviceitem = ServiceItem()
    serviceitem.name = '陪同就醫 '
    serviceitem.info = '陪伴看診、洗腎，代領藥品'
    serviceitem.save()
    
    serviceitem = ServiceItem()
    serviceitem.name = '陪同復健'
    serviceitem.save()

    city = City()
    city.name = '基隆市'
    city.save()

    city = City()
    city.name = '台北市'
    city.save()

    city = City()
    city.name = '宜蘭縣'
    city.save()

    city = City()
    city.name = '新北市'
    city.save()

    city = City()
    city.name = '花蓮縣'
    city.save()

    city = City()
    city.name = '桃園市'
    city.save()

    city = City()
    city.name = '彰化縣'
    city.save()

    city = City()
    city.name = '南投縣'
    city.save()

    city = City()
    city.name = '台中市'
    city.save()

    city = City()
    city.name = '苗栗縣'
    city.save()


    cityarea = CityArea()
    cityarea.city = City.objects.get(id=1)
    cityarea.area = '全區'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=2)
    cityarea.area = '全區'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=2)
    cityarea.area = '中正區'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=3)
    cityarea.area = '全區'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=4)
    cityarea.area = '全區'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=5)
    cityarea.area = '全區'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=6)
    cityarea.area = '全區'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=7)
    cityarea.area = '全區'
    cityarea.save()

    cityarea = CityArea()
    cityarea.city = City.objects.get(id=7)
    cityarea.area = '彰化市'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=7)
    cityarea.area = '和美鎮'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=8)
    cityarea.area = '全區'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=8)
    cityarea.area = '南投市'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=9)
    cityarea.area = '全區'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=9)
    cityarea.area = '西屯區'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=9)
    cityarea.area = '北區'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=10)
    cityarea.area = '全區'
    cityarea.save()

    transportation = Transportation()
    transportation.servant = Servant.objects.get(id=1)
    transportation.cityarea = CityArea.objects.get(id=13)
    transportation.price = 500
    transportation.save()
 
    transportation = Transportation()
    transportation.servant = Servant.objects.get(id=1)
    transportation.cityarea = CityArea.objects.get(id=9)
    transportation.price = 0
    transportation.save()

    transportation = Transportation()
    transportation.servant = Servant.objects.get(id=1)
    transportation.cityarea = CityArea.objects.get(id=10)
    transportation.price = 300
    transportation.save()

    transportation = Transportation()
    transportation.servant = Servant.objects.get(id=1)
    transportation.cityarea = CityArea.objects.get(id=12)
    transportation.price = 500
    transportation.save()
    
    transportation = Transportation()
    transportation.servant = Servant.objects.get(id=1)
    transportation.cityarea = CityArea.objects.get(id=16)
    transportation.price = 500
    transportation.save()
    
    transportation = Transportation()
    transportation.servant = Servant.objects.get(id=2)
    transportation.cityarea = CityArea.objects.get(id=1)
    transportation.price = 200
    transportation.save()
    
    transportation = Transportation()
    transportation.servant = Servant.objects.get(id=2)
    transportation.cityarea = CityArea.objects.get(id=2)
    transportation.price = 300
    transportation.save()
    
    transportation = Transportation()
    transportation.servant = Servant.objects.get(id=2)
    transportation.cityarea = CityArea.objects.get(id=3)
    transportation.price = 400
    transportation.save()

    case = Case()
    case.recipient = Recipient.objects.get(id=2)
    case.servant = Servant.objects.get(id=1)
    case.cityarea = CityArea.objects.get(id=1)
    case.start_date = '2022-06-22'
    case.end_date = '2022-07-12'
    case.start_time = datetime.time(10,0,0)
    case.end_time = datetime.time(22,0,0)
    case.save()

    case = Case()
    case.recipient = Recipient.objects.get(id=3)
    case.servant = Servant.objects.get(id=2)
    case.cityarea = CityArea.objects.get(id=5)
    case.start_date = '2022-07-02'
    case.end_date = '2022-07-15'
    case.start_time = datetime.time(12,30,0)
    case.end_time = datetime.time(20,30,0)
    case.save()
    
    case = Case()
    case.recipient = Recipient.objects.get(id=5)
    case.servant = Servant.objects.get(id=3)
    case.cityarea = CityArea.objects.get(id=11)
    case.start_date = '2022-06-25'
    case.end_date = '2022-07-25'
    case.start_time = datetime.time(9,0,0)
    case.end_time = datetime.time(17,0,0)
    case.save()

    caseitemship = CaseServiceItemShip()
    caseitemship.case = Case.objects.get(id=1)
    caseitemship.service_item = ServiceItem.objects.get(id=2)
    caseitemship.save()
    
    caseitemship = CaseServiceItemShip()
    caseitemship.case = Case.objects.get(id=1)
    caseitemship.service_item = ServiceItem.objects.get(id=3)
    caseitemship.save()
    
    caseitemship = CaseServiceItemShip()
    caseitemship.case = Case.objects.get(id=2)
    caseitemship.service_item = ServiceItem.objects.get(id=1)
    caseitemship.save()
    
    caseitemship = CaseServiceItemShip()
    caseitemship.case = Case.objects.get(id=2)
    caseitemship.service_item = ServiceItem.objects.get(id=5)
    caseitemship.save()
        
    caseitemship = CaseServiceItemShip()
    caseitemship.case = Case.objects.get(id=3)
    caseitemship.service_item = ServiceItem.objects.get(id=2)
    caseitemship.save()

    caseitemship = CaseServiceItemShip()
    caseitemship.case = Case.objects.get(id=3)
    caseitemship.service_item = ServiceItem.objects.get(id=6)
    caseitemship.save()

    orderstate = OrderState()
    orderstate.name = '未完成'
    orderstate.save()

    orderstate = OrderState()
    orderstate.name = '已完成'
    orderstate.save()

    orderstate = OrderState()
    orderstate.name = '已取消'
    orderstate.save()

    order = Order()
    order.case = Case.objects.get(id=1)
    order.state = OrderState.objects.get(id=1)
    order.info = 'test'
    order.save()

    order = Order()
    order.case = Case.objects.get(id=2)
    order.state = OrderState.objects.get(id=3)
    order.info = 'test'
    order.save()

    order = Order()
    order.case = Case.objects.get(id=3)
    order.state = OrderState.objects.get(id=1)
    order.info = 'test'
    order.save()

    orderreview = OrderReview()
    orderreview.order = Order.objects.get(id=1)
    orderreview.customer_score = 5
    orderreview.customer_content = 'Test'
    orderreview.servant_score = 5
    orderreview.servant_content = 'Test'
    orderreview.save()
    
    orderreview = OrderReview()
    orderreview.order = Order.objects.get(id=2)
    orderreview.customer_score = 4
    orderreview.customer_content = 'Test'
    orderreview.servant_score = 5
    orderreview.servant_content = 'Test'
    orderreview.save()
    
    orderreview = OrderReview()
    orderreview.order = Order.objects.get(id=3)
    orderreview.customer_score = 5
    orderreview.customer_content = 'Test'
    orderreview.servant_score = 4
    orderreview.servant_content = 'Test'
    orderreview.save()
