import pathlib
from unicodedata import category
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.urls import reverse


def image_upload_handler(instance,filename):
    fpath = pathlib.Path(filename)
    new_fname = str(uuid.uuid1()) #uuid1 -> uuid + timestamp
    return f'images/{new_fname}{fpath.suffix}'


class UserManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not phone:
            raise ValueError('Users must have an phone')
        # user = self.model(email=self.normalize_email(email), **extra_fields)
        user = self.model(
            phone = phone, 
            name=extra_fields.get('name'),
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password, **extra_fields):
        """Creates and saves a new super user"""
        user = self.create_user(phone, password, **extra_fields)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppors using email instead of username"""
    phone = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,default='')
    email = models.CharField(max_length= 100, blank = True, null=True)
    address = models.CharField(max_length= 100, blank = True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_servant = models.BooleanField(default=False)
    line_id = models.CharField(max_length= 100, blank = True, null=True, unique=True)
    objects = UserManager()
    image = models.ImageField(upload_to=image_upload_handler, blank=True, null=True)
    USERNAME_FIELD = 'phone'

class MarkupItem(models.Model):
    name = models.CharField(max_length= 100, unique=True)
    def __str__(self):
            return self.name

class License(models.Model):
    name = models.CharField(max_length= 100, unique=True)
    def __str__(self):
        return self.name

class Servant(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    score = models.FloatField(default=0, blank = True, null=True)
    user =models.OneToOneField(User,on_delete=models.RESTRICT,unique=True,default='',related_name='servant')
    is_home = models.BooleanField(default=False)
    home_hourly_wage = models.IntegerField(default=0, blank = True, null=True)
    home_halfday_wage = models.IntegerField(default=0, blank = True, null=True)
    home_oneday_wage = models.IntegerField(default=0, blank = True, null=True)
    is_hospital = models.BooleanField(default=False)
    hospital_hourly_wage = models.IntegerField(default=0, blank = True, null=True)
    hospital_halfday_wage = models.IntegerField(default=0, blank = True, null=True)
    hospital_oneday_wage = models.IntegerField(default=0, blank = True, null=True)
    info = models.CharField(max_length= 255, blank = True, null=True)
    is_alltime_service = models.BooleanField(default=False)
    background_image = models.ImageField(upload_to=image_upload_handler, blank=True, null=True)

class ServantWeekdayTime(models.Model):
    servant = models.ForeignKey(
        Servant,
        on_delete=models.RESTRICT,
        related_name='weekdayTimes'
    )
    WEEKDAY_CHOICES = (
        ('0', 'Sunday'),
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('7', 'All'),
        
    )
    weekday = models.CharField(max_length=1, choices=WEEKDAY_CHOICES)
    start_time = models.TimeField(auto_now=False, auto_now_add=False )
    end_time = models.TimeField(auto_now=False, auto_now_add=False )

class ServantMarkupItemPrice(models.Model):
    servant = models.ForeignKey(
        Servant,
        on_delete=models.RESTRICT,
    )
    markup_item = models.ForeignKey(
        MarkupItem,
        on_delete=models.RESTRICT
    )
    pricePercent = models.FloatField(default=0, blank = True, null=True)

class ServantSkill(models.Model):
    servant = models.ForeignKey(
        Servant,
        on_delete=models.RESTRICT
    )
    languageSkill = models.CharField(max_length= 100)



class UserLicenseShipImage(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='images'
        )
    license = models.ForeignKey(
        License,
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to=image_upload_handler, blank=True, null=True)

    is_upload_image = models.BooleanField(default=False)

class ServantLicenseShipImage(models.Model):
    servant = models.ForeignKey(
        Servant,
        on_delete=models.CASCADE,
        related_name='images'
        )
    license = models.ForeignKey(
        License,
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to=image_upload_handler, blank=True, null=True)

    is_upload_image = models.BooleanField(default=False)

class Recipient(models.Model):
    name = models.CharField(max_length= 100, blank=True, null=True)
    user =models.ForeignKey(User,on_delete=models.RESTRICT,related_name='recipient')
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.IntegerField(default=0, blank = True, null=True)
    weight = models.IntegerField(default=0, blank = True, null=True)
    disease = models.CharField(max_length= 100, blank = True, null=True)
    disease_info = models.CharField(max_length= 255, blank = True, null=True)
    conditions = models.CharField(max_length= 255, blank = True, null=True)
    conditions_info = models.CharField(max_length= 255, blank = True, null=True)

class ServiceItem(models.Model):
    name = models.CharField(max_length = 100, blank = True, null=True)
    info = models.CharField(max_length = 100, blank = True, null=True)
    def __str__(self):
        return self.name

class ServantServiceItemShip(models.Model):
    servant = models.ForeignKey(
        Servant,
        on_delete=models.RESTRICT,
    )
    service_item = models.ForeignKey(
        ServiceItem,
        on_delete=models.RESTRICT,
    )

class City(models.Model):
    name = models.CharField(max_length = 255, blank = True, null=True)

    def __str__(self):
            return self.name

class CityArea(models.Model):
    city = models.CharField(max_length = 100, blank = True, null=True)
    area = models.CharField(max_length = 100, blank = True, null=True)


class Transportation(models.Model):
    servant = models.ForeignKey(
        Servant,
        on_delete=models.RESTRICT,
        related_name='transportations'
    )
    cityarea = models.ForeignKey(
        CityArea,
        on_delete=models.RESTRICT
    )
    price = models.IntegerField(default=0, null=True)
    
class Case(models.Model):
    recipient = models.ForeignKey(
        Recipient,
        on_delete=models.RESTRICT,
        default=''
    )
    servant = models.ForeignKey(
        Servant,
        on_delete=models.RESTRICT,
        blank = True,
        null=True,
        related_name='cases'
    )
    
    cityarea = models.ForeignKey(
        CityArea,
        on_delete=models.RESTRICT
    )

    markup_item = models.ForeignKey(
        ServantMarkupItemPrice,
        on_delete=models.RESTRICT,
        default=''
    )
    CARETYPE_CHOICES = (
        ('home', '居家照顧'),
        ('hospital', '醫院看護'),
    )
    care_type = models.CharField(max_length=10, choices=CARETYPE_CHOICES,default='')
    is_alltime_service = models.BooleanField(default=False)
    start_date = models.DateField(auto_now=False, blank = True,null=True)
    end_date = models.DateField(auto_now=False, blank = True,null=True) 
    start_time = models.TimeField(auto_now=False, auto_now_add=False )
    end_time = models.TimeField(auto_now=False, auto_now_add=False )

    is_taken = models.BooleanField(default=False)
    consult_all_servant = models.BooleanField(default=False)
    specify_servant_1 = models.ForeignKey(Servant,on_delete=models.CASCADE, blank = True,null=True, related_name='cases_specify_1')
    specify_servant_2 = models.ForeignKey(Servant,on_delete=models.CASCADE, blank = True,null=True, related_name='cases_specify_2')
    specify_servant_3 = models.ForeignKey(Servant,on_delete=models.CASCADE, blank = True,null=True, related_name='cases_specify_3')


class CaseServiceItemShip(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete=models.RESTRICT
    )
    service_item = models.ForeignKey(
        ServiceItem,
        on_delete=models.RESTRICT
    )

class OrderState(models.Model):
    name = models.CharField(max_length=255, null=True , blank=True)
    
    def __str__(self):
        return self.name

class Order(models.Model):

    case = models.ForeignKey(
        Case,
        on_delete = models.CASCADE,
        blank=True,
        null=True    
    )
    state =  models.ForeignKey(
        OrderState,
        on_delete=models.RESTRICT,
        null =True
    )
    address = models.CharField(max_length = 255, blank = True, null=True)
    info = models.CharField(max_length = 255, blank = True, null=True)
    createdate = models.DateTimeField(auto_now=True, blank = True,null=True) 



class OrderReview(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.RESTRICT
    )
    user_score =  models.IntegerField(default=0, blank = True, null=True)
    user_is_rated = models.BooleanField(default=False)
    user_content = models.CharField(max_length = 255, blank = True, null=True)
    user_review_createdate = models.DateTimeField(auto_now=False, blank = True,null=True) 
    servant_score =  models.IntegerField(default=0, blank = True, null=True)
    servant_is_rated = models.BooleanField(default=False)
    servant_content = models.CharField(max_length = 255, blank = True, null=True)
    servant_review_createdate = models.DateTimeField(auto_now=False, blank = True,null=True) 

class PayInfo(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.RESTRICT,
        default=''
    )
    
    PaymentType = models.CharField(max_length=100, default='', blank = True, null=True)
    MerchantID = models.CharField(max_length=100, default='', blank = True, null=True)
    
    OrderInfoMerchantTradeNo = models.CharField(max_length=100, default='', blank = True, null=True)
    OrderInfoTradeDate = models.DateTimeField(auto_now=False,null=True)
    OrderInfoTradeNo = models.CharField(max_length=100, default='', blank = True, null=True)
    OrderInfoTradeAmt = models.IntegerField(default=0, null=True)
    OrderInfoPaymentType = models.CharField(max_length=20, default='', blank = True, null=True)
    OrderInfoChargeFee = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    OrderInfoTradeStatus = models.CharField(max_length=20, default='', blank = True, null=True)

    CardInfoAuthCode = models.CharField(max_length=100, default='', blank = True, null=True)
    CardInfoGwsr = models.IntegerField(default=0, null=True)
    CardInfoProcessDate =  models.DateTimeField(auto_now=False,null=True)
    CardInfoAmount = models.IntegerField(default=0, null=True)
    CardInfoCard6No = models.CharField(max_length=20, default='', blank = True, null=True)
    CardInfoCard4No = models.CharField(max_length=20, default='', blank = True, null=True)

class Message(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        )
    servant = models.ForeignKey(
        Servant,
        on_delete=models.RESTRICT,
        default=''
    )
    SPEAKER_CHOICES = (
        ('0', 'user'),
        ('1', 'servant'),
    )
    
    speaker = models.CharField(max_length=1, choices=SPEAKER_CHOICES)

    case = models.ForeignKey(
        Case,
        on_delete = models.CASCADE,
        blank=True,
        null=True    
    )
    content = models.TextField(default='', blank = True, null=True)
    create_time = models.DateTimeField(auto_now=True, blank = True,null=True) 

class SystemMessage(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        )
    case = models.ForeignKey(
        Case,
        on_delete = models.CASCADE,
        blank=True,
        null=True    
    )
    content = models.TextField(default='', blank = True, null=True)
    create_time = models.DateTimeField(auto_now=True, blank = True,null=True) 
    