import csv
import os
import datetime 
from datetime import timedelta
from .models import ServantCityAreaShip, User, MarkupItem, Category,License, Servant, ServantMarkupItemPrice, Weekday
from .models import ServantSkill,UserLicenseShipImage, ServantLicenseShipImage, ServantCategoryShip, Recipient, ServiceItem,  CityArea, Transportation, Case,OrderState, Order, OrderReview , CaseServiceItemShip 
from .models import City, CityArea ,ServantWeekdayTimeShip,Weekday,ServantServiceItemShip

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
            county = CityArea()
            county.city = city
            county.area = county_name
            county.save()
            print(city.name + " " + county.area)
            

def fakeData():
    user = User()
    user.name = 'user01'
    user.phone = '0915323131'
    user.is_active = True
    user.is_staff =  False
    user.save()

    user = User()
    user.name = 'user02'
    user.phone = '0985463816'
    user.is_active = True
    user.is_staff =  False
    user.save()

    user = User()
    user.name = 'user03'
    user.phone = '0985463888'
    user.is_active = True
    user.is_staff =  False
    user.is_servant = True
    user.save()

    user = User()
    user.name = 'user04'
    user.phone = '0985490816'
    user.is_active = True
    user.is_staff =  False
    user.is_servant = True
    user.save()

    user = User()
    user.name = 'user05'
    user.phone = '0985478816'
    user.is_active = True
    user.is_staff =  False
    user.is_servant = True
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

    license = License()
    license.name = '身分證正面'
    license.save()

    license = License()
    license.name = '身分證反面'
    license.save()

    license = License()
    license.name = '健保卡正面'
    license.save()

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

    weekday = Weekday()
    weekday.name = '0'
    weekday.save()

    weekday = Weekday()
    weekday.name = '1'
    weekday.save()

    weekday = Weekday()
    weekday.name = '2'
    weekday.save()

    weekday = Weekday()
    weekday.name = '3'
    weekday.save()

    weekday = Weekday()
    weekday.name = '4'
    weekday.save()

    weekday = Weekday()
    weekday.name = '5'
    weekday.save()

    weekday = Weekday()
    weekday.name = '6'
    weekday.save()

    weekday = Weekday()
    weekday.name = '7'
    weekday.save()

    servant = Servant()
    servant.user = User.objects.get(id=4)
    servant.gender = 'M'
    servant.home_hourly_wage = 250
    servant.home_halfday_wage = 1500
    servant.home_oneday_wage = 3300
    servant.hospital_hourly_wage = 270
    servant.hospital_halfday_wage = 1600
    servant.hospital_oneday_wage = 3400
    servant.info = 'test'
    servant.save()

    servant = Servant()
    servant.user = User.objects.get(id=5)
    servant.gender = 'M'
    servant.home_hourly_wage = 240
    servant.home_halfday_wage = 1450
    servant.home_oneday_wage = 3000
    servant.hospital_hourly_wage = 250
    servant.hospital_halfday_wage = 1550
    servant.hospital_oneday_wage = 3300
    servant.info = 'test'
    servant.save()

    servant = Servant()
    servant.user = User.objects.get(id=6)
    servant.gender = 'F'
    servant.home_hourly_wage = 330
    servant.home_halfday_wage = 1800
    servant.home_oneday_wage = 3700
    servant.hospital_hourly_wage = 350
    servant.hospital_halfday_wage = 1950
    servant.hospital_oneday_wage = 4000
    servant.info = 'test'
    servant.save()

 

    markup_price = ServantMarkupItemPrice()
    markup_price.servant = Servant.objects.get(id=1)
    markup_price.markup_item = MarkupItem.objects.get(id=2)
    markup_price.pricePercent = 1.25
    markup_price.save()

    markup_price = ServantMarkupItemPrice()
    markup_price.servant = Servant.objects.get(id=2)
    markup_price.markup_item = MarkupItem.objects.get(id=4)
    markup_price.pricePercent = 1.45
    markup_price.save()

    markup_price = ServantMarkupItemPrice()
    markup_price.servant = Servant.objects.get(id=3)
    markup_price.markup_item = MarkupItem.objects.get(id=1)
    markup_price.pricePercent = 1.3
    markup_price.save()


    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=2)
    userlicense.license = License.objects.get(id=1)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=2)
    userlicense.license = License.objects.get(id=2)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=2)
    userlicense.license = License.objects.get(id=3)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=3)
    userlicense.license = License.objects.get(id=1)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=3)
    userlicense.license = License.objects.get(id=2)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=3)
    userlicense.license = License.objects.get(id=3)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=4)
    userlicense.license = License.objects.get(id=1)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=4)
    userlicense.license = License.objects.get(id=2)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=4)
    userlicense.license = License.objects.get(id=3)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=5)
    userlicense.license = License.objects.get(id=1)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=5)
    userlicense.license = License.objects.get(id=2)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=5)
    userlicense.license = License.objects.get(id=3)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=6)
    userlicense.license = License.objects.get(id=1)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=6)
    userlicense.license = License.objects.get(id=2)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=6)
    userlicense.license = License.objects.get(id=3)
    userlicense.save()


    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=1)
    servantlicense.license = License.objects.get(id=4)
    servantlicense.save()

    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=1)
    servantlicense.license = License.objects.get(id=7)
    servantlicense.save()

    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=1)
    servantlicense.license = License.objects.get(id=8)
    servantlicense.save()

    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=1)
    servantlicense.license = License.objects.get(id=9)
    servantlicense.save()

    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=2)
    servantlicense.license = License.objects.get(id=4)
    servantlicense.save()

    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=2)
    servantlicense.license = License.objects.get(id=7)
    servantlicense.save()

    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=3)
    servantlicense.license = License.objects.get(id=6)
    servantlicense.save()

    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=3)
    servantlicense.license = License.objects.get(id=8)
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
    recipient.user = User.objects.get(id=2)
    recipient.gender = 'M'
    recipient.age = 65
    recipient.weight = 70
    recipient.disease = '無'
    recipient.disease_info = 'test'
    recipient.save()

    recipient = Recipient()
    recipient.name = 'recipient02'
    recipient.user = User.objects.get(id=2)
    recipient.gender = 'M'
    recipient.age = 65
    recipient.weight = 70
    recipient.disease = '無'
    recipient.disease_info = 'test'
    recipient.save()

    recipient = Recipient()
    recipient.name = 'recipient03'
    recipient.user = User.objects.get(id=2)
    recipient.gender = 'M'
    recipient.age = 80
    recipient.weight = 67
    recipient.disease = '關節炎'
    recipient.disease_info = 'test'
    recipient.save()

    recipient = Recipient()
    recipient.name = 'recipient04'
    recipient.user = User.objects.get(id=3)
    recipient.gender = 'F'
    recipient.age = 70
    recipient.weight = 55
    recipient.disease = '糖尿病'
    recipient.disease_info = 'test'
    recipient.save()

    recipient = Recipient()
    recipient.name = 'recipient05'
    recipient.user = User.objects.get(id=3)
    recipient.gender = 'M'
    recipient.age = 68
    recipient.weight = 95
    recipient.disease = '心臟病'
    recipient.disease_info = 'test'
    recipient.save()

    recipient = Recipient()
    recipient.name = 'recipient06'
    recipient.user = User.objects.get(id=3)
    recipient.gender = 'F'
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
    serviceitem.name = '協助進食'
    serviceitem.info = '用餐，按醫囑給藥'
    serviceitem.save()
    
    serviceitem = ServiceItem()
    serviceitem.name = '協助如廁'
    serviceitem.info = '大小便處理、更換尿布、會陰沖洗'
    serviceitem.save()
    
    serviceitem = ServiceItem()
    serviceitem.name = '身體清潔'
    serviceitem.info = '沐浴、擦澡'
    serviceitem.save()
    
    serviceitem = ServiceItem()
    serviceitem.name = '陪同就醫'
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

    servantcityareaship = ServantCityAreaShip()
    servantcityareaship.servant = Servant.objects.get(id=1)
    servantcityareaship.cityarea = CityArea.objects.get(id=1)
    servantcityareaship.save()

    servantcityareaship = ServantCityAreaShip()
    servantcityareaship.servant = Servant.objects.get(id=1)
    servantcityareaship.cityarea = CityArea.objects.get(id=3)
    servantcityareaship.save()

    servantcityareaship = ServantCityAreaShip()
    servantcityareaship.servant = Servant.objects.get(id=1)
    servantcityareaship.cityarea = CityArea.objects.get(id=6)
    servantcityareaship.save()

    servantcityareaship = ServantCityAreaShip()
    servantcityareaship.servant = Servant.objects.get(id=1)
    servantcityareaship.cityarea = CityArea.objects.get(id=10)
    servantcityareaship.save()

    servantcityareaship = ServantCityAreaShip()
    servantcityareaship.servant = Servant.objects.get(id=2)
    servantcityareaship.cityarea = CityArea.objects.get(id=2)
    servantcityareaship.save()

    servantcityareaship = ServantCityAreaShip()
    servantcityareaship.servant = Servant.objects.get(id=2)
    servantcityareaship.cityarea = CityArea.objects.get(id=4)
    servantcityareaship.save()

    servantcityareaship = ServantCityAreaShip()
    servantcityareaship.servant = Servant.objects.get(id=2)
    servantcityareaship.cityarea = CityArea.objects.get(id=8)
    servantcityareaship.save()

    servantcityareaship = ServantCityAreaShip()
    servantcityareaship.servant = Servant.objects.get(id=2)
    servantcityareaship.cityarea = CityArea.objects.get(id=9)
    servantcityareaship.save()

    servantcityareaship = ServantCityAreaShip()
    servantcityareaship.servant = Servant.objects.get(id=3)
    servantcityareaship.cityarea = CityArea.objects.get(id=1)
    servantcityareaship.save()

    servantcityareaship = ServantCityAreaShip()
    servantcityareaship.servant = Servant.objects.get(id=3)
    servantcityareaship.cityarea = CityArea.objects.get(id=4)
    servantcityareaship.save()

    servantcityareaship = ServantCityAreaShip()
    servantcityareaship.servant = Servant.objects.get(id=3)
    servantcityareaship.cityarea = CityArea.objects.get(id=5)
    servantcityareaship.save()

    servantcityareaship = ServantCityAreaShip()
    servantcityareaship.servant = Servant.objects.get(id=3)
    servantcityareaship.cityarea = CityArea.objects.get(id=12)
    servantcityareaship.save()

    transportation = Transportation()
    transportation.servantCityArea = ServantCityAreaShip.objects.get(id=1)
    transportation.price = 500
    transportation.save()
 
    transportation = Transportation()
    transportation.servantCityArea = ServantCityAreaShip.objects.get(id=2)
    transportation.price = 0
    transportation.save()

    transportation = Transportation()
    transportation.servantCityArea = ServantCityAreaShip.objects.get(id=3)
    transportation.price = 300
    transportation.save()

    transportation = Transportation()
    transportation.servantCityArea = ServantCityAreaShip.objects.get(id=4)
    transportation.price = 500
    transportation.save()
    
    transportation = Transportation()
    transportation.servantCityArea = ServantCityAreaShip.objects.get(id=5)
    transportation.price = 500
    transportation.save()
    
    transportation = Transportation()
    transportation.servantCityArea = ServantCityAreaShip.objects.get(id=1)
    transportation.price = 200
    transportation.save()
    
    transportation = Transportation()
    transportation.servantCityArea = ServantCityAreaShip.objects.get(id=6)
    transportation.price = 300
    transportation.save()
    
    transportation = Transportation()
    transportation.servantCityArea = ServantCityAreaShip.objects.get(id=7)
    transportation.price = 400
    transportation.save()

    case = Case()
    case.recipient = Recipient.objects.get(id=2)
    case.servant = Servant.objects.get(id=1)
    case.cityarea = ServantCityAreaShip.objects.filter(servant=Servant.objects.get(id=1)).order_by('id')[1].cityarea
    case.category = ServantCategoryShip.objects.filter(servant=Servant.objects.get(id=1)).order_by('id')[0].category
    case.markup_item = ServantMarkupItemPrice.objects.filter(servant=Servant.objects.get(id=1)).order_by('id')[0]
    case.start_date = '2022-06-22'
    case.end_date = '2022-07-12'
    case.start_time = datetime.time(10,0,0)
    case.end_time = datetime.time(22,0,0)
    case.save()

    case = Case()
    case.recipient = Recipient.objects.get(id=3)
    case.servant = Servant.objects.get(id=2)
    case.cityarea = ServantCityAreaShip.objects.filter(servant=Servant.objects.get(id=2)).order_by('id')[3].cityarea
    case.category = ServantCategoryShip.objects.filter(servant=Servant.objects.get(id=2)).order_by('id')[0].category
    case.markup_item = ServantMarkupItemPrice.objects.filter(servant=Servant.objects.get(id=2)).order_by('id')[0]
    case.start_date = '2022-07-02'
    case.end_date = '2022-07-15'
    case.start_time = datetime.time(12,30,0)
    case.end_time = datetime.time(20,30,0)
    case.save()
    
    case = Case()
    case.recipient = Recipient.objects.get(id=5)
    case.servant = Servant.objects.get(id=3)
    case.cityarea = ServantCityAreaShip.objects.filter(servant=Servant.objects.get(id=3)).order_by('id')[2].cityarea
    case.category = ServantCategoryShip.objects.filter(servant=Servant.objects.get(id=3)).order_by('id')[1].category
    case.markup_item = ServantMarkupItemPrice.objects.filter(servant=Servant.objects.get(id=3)).order_by('id')[0]
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
    orderreview.user_score = 5
    orderreview.user_is_rated = True
    orderreview.user_content = 'Test'
    orderreview.servant_score = 5
    orderreview.servant_is_rated = True
    orderreview.servant_content = 'Test'
    orderreview.save()
    
    orderreview = OrderReview()
    orderreview.order = Order.objects.get(id=2)
    orderreview.user_score = 4
    orderreview.user_is_rated = True
    orderreview.user_content = 'Test'
    orderreview.servant_score = 5
    orderreview.servant_is_rated = True
    orderreview.servant_content = 'Test'
    orderreview.save()
    
    orderreview = OrderReview()
    orderreview.order = Order.objects.get(id=3)
    orderreview.save()
