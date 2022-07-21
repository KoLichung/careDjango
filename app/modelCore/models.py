import pathlib
from unicodedata import category
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.forms import FloatField
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
    phone = models.CharField(max_length=10, unique=True)
    objects = UserManager()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    name = models.CharField(max_length=255)

    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,default=MALE)

    email = models.CharField(max_length= 100, blank = True, null=True)
    address = models.CharField(max_length= 100, blank = True, null=True)
    image = models.ImageField(upload_to=image_upload_handler, blank=True, null=True)
    line_id = models.CharField(max_length= 100, blank = True, null=True, unique=True)

    is_servant = models.BooleanField(default=False)
    rating = models.FloatField(default=0, blank = True, null=True)

    is_home = models.BooleanField(default=False)
    home_hour_wage = models.IntegerField(default=0, blank = True, null=True)
    home_half_day_wage = models.IntegerField(default=0, blank = True, null=True)
    home_one_day_wage = models.IntegerField(default=0, blank = True, null=True)
    
    is_hospital = models.BooleanField(default=False)
    hospital_hour_wage = models.IntegerField(default=0, blank = True, null=True)
    hospital_half_day_wage = models.IntegerField(default=0, blank = True, null=True)
    hospital_one_day_wage = models.IntegerField(default=0, blank = True, null=True)

    about_me = models.TextField(default='', blank = True, null=True)
    is_continuous_time = models.BooleanField(default=True)

    background_image = models.ImageField(upload_to=image_upload_handler, blank=True, null=True)

    ATMInfoBankCode = models.CharField(max_length=20, default='', blank = True, null=True)
    ATMInfoBranchBankCode = models.CharField(max_length=20, default='', blank = True, null=True)
    ATMInfoAccount = models.CharField(max_length=20, default='', blank = True, null=True)

    USERNAME_FIELD = 'phone'

class Service(models.Model):
    name = models.CharField(max_length= 100, unique=True)
    remark = models.CharField(max_length= 150, blank = True, null=True)
    is_increase_price = models.BooleanField(default=False)
    

    def __str__(self):
        return self.name

class UserWeekDayTime(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name='user_weekday'
    )
    WEEKDAY_CHOICES = [
        ('0', 'Sunday'),
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
    ]
    weekday = models.CharField(max_length=1, choices=WEEKDAY_CHOICES,)
    start_time = models.FloatField(default=0, blank=True, null=True)
    end_time = models.FloatField(default=24, blank=True, null=True)

class UserServiceShip(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.RESTRICT
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.RESTRICT
    )
    increase_percent = models.FloatField(default=0, blank = True, null=True)
    
class Language(models.Model):
    name = models.CharField(max_length= 100)
    def __str__(self):
        return self.name

class UserLanguage(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name='languages'
    )
    language =  models.ForeignKey(
        Language,
        on_delete=models.RESTRICT
    )
    remark = models.CharField(max_length= 100, null=True, blank=True)

class License(models.Model):
    name = models.CharField(max_length= 100, unique=True)
    remark = models.CharField(max_length= 150, null=True, blank=True)
    def __str__(self):
        return self.name

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

class City(models.Model):
    name = models.CharField(max_length = 255, blank=True, null=True)
    def __str__(self):
            return self.name

class County(models.Model):
    city =  models.ForeignKey(
        City,
        on_delete=models.RESTRICT,
    )
    name = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
            return self.name

class UserServiceLocation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name='user_locations',
    )
    city = models.ForeignKey(
        City,
        on_delete=models.RESTRICT,
        null=True,
        blank=True
    )
    county =  models.ForeignKey(
        County,
        on_delete=models.RESTRICT,
    )
    tranfer_fee = models.IntegerField(default=0, blank=True, null=True)

class Case(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        default=''
    )

    servant = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        blank = True,
        null=True,
        related_name='servant_cases'
    )
    
    city = models.ForeignKey(
        City,
        on_delete=models.RESTRICT,
        null=True,
        blank=True
    )

    county = models.ForeignKey(
        County,
        on_delete=models.RESTRICT
    )

    CARETYPE_CHOICES = [
        ('home', '居家照顧'),
        ('hospital', '醫院看護'),
    ]
    care_type = models.CharField(max_length=10, choices=CARETYPE_CHOICES,default='')

    name = models.CharField(max_length= 100, blank=True, null=True)

    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,default=MALE)

    age = models.IntegerField(default=0, blank=True, null=True)
    weight = models.IntegerField(default=0, blank=True, null=True)
    
    disease_remark = models.CharField(max_length= 255, blank=True, null=True)
    conditions_remark = models.CharField(max_length= 255, blank=True, null=True)

    is_continuous_time = models.BooleanField(default=False)

    is_taken = models.BooleanField(default=False)
    is_open_for_search = models.BooleanField(default=False)

    weekday = models.CharField(max_length=100, blank=True, null=True)
    start_time = models.FloatField(default=0, blank=True, null=True)
    end_time = models.FloatField(default=24, blank=True, null=True)
    start_datetime = models.DateTimeField(auto_now=False, blank=True, null=True)
    end_datetime = models.DateTimeField(auto_now=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)

class DiseaseCondition(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.name

class BodyCondition(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.name

class CaseDiseaseShip(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete=models.RESTRICT
    )
    disease = models.ForeignKey(
        DiseaseCondition,
        on_delete=models.RESTRICT
    )

class CaseBodyConditionShip(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete=models.RESTRICT
    )
    body_condition = models.ForeignKey(
        BodyCondition,
        on_delete=models.RESTRICT
    )

class CaseServiceShip(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete=models.RESTRICT
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.RESTRICT
    )

class Order(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete = models.CASCADE,
        related_name='orders',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )
    UNPAID = 'unPaid'
    PAID = 'paid'
    CANCELED = 'canceled'
    STATE_CHOICES = [
        (UNPAID, '未付款'),
        (PAID, '已付款'),
        (CANCELED, '已取消')
    ]
    state =  models.CharField(max_length=10, choices=STATE_CHOICES,default=UNPAID)
    
    work_hours = models.FloatField(default=0, blank = True, null=True)
    base_money = models.IntegerField(default=0, blank=True, null=True)
    platform_percent = models.FloatField(default=0, blank = True, null=True)
    platform_money = models.IntegerField(default=0, blank=True, null=True)
    total_money = models.IntegerField(default=0, blank=True, null=True)

    start_datetime = models.DateTimeField(auto_now=False, blank=True, null=True)
    end_datetime = models.DateTimeField(auto_now=False, blank=True, null=True)

    start_time = models.FloatField(default=0, blank=True, null=True)
    end_time = models.FloatField(default=24, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now=True, blank = True,null=True) 

class OrderIncreaseService(models.Model):
    order =  models.ForeignKey(
        Order,
        on_delete = models.CASCADE,
        related_name='order_service',
    )
    service = service = models.ForeignKey(
        Service,
        on_delete=models.RESTRICT
    )
    increase_percent = models.FloatField(default=0, blank = True, null=True)

    increase_money = models.IntegerField(default=0, blank=True, null=True)

class OrderWeekDay(models.Model):
    order =  models.ForeignKey(
        Order,
        on_delete = models.CASCADE,
        related_name='order_weekday',
    )
    WEEKDAY_CHOICES = [
        ('0', 'Sunday'),
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
    ]
    weekday = models.CharField(max_length=1, choices=WEEKDAY_CHOICES,)

class Review(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.RESTRICT
    )
    case = models.ForeignKey(
        Case,
        on_delete = models.CASCADE,
        null=True,
        blank=True
    )
    servant = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        null=True,
        blank=True
    )

    case_offender_rating =  models.FloatField(default=0, blank = True, null=True)
    case_offender_comment = models.CharField(max_length = 255, blank = True, null=True)
    case_offender_rating_created_at= models.DateTimeField(auto_now=False, blank = True,null=True) 

    servant_rating =  models.FloatField(default=0, blank = True, null=True)
    servant_comment = models.CharField(max_length = 255, blank = True, null=True)
    servant_rating_created_at = models.DateTimeField(auto_now=False, blank = True,null=True) 

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

class ChatRoom(models.Model):
    update_at = models.DateTimeField(auto_now=True, blank = True, null=True) 

class ChatroomUserShip(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    chatroom = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
    ) 

class Message(models.Model):
    chatroom = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    # user is the one who make message
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    case = models.ForeignKey(
        Case,
        on_delete = models.CASCADE,
        blank=True,
        null=True,
    )
    # SERVNAT = 'servant'
    # NEEDER = 'needer'
    # ID_TYPE_CHOICES = [
    #     (SERVNAT, 'servant'),
    #     (NEEDER, 'needer'),
    # ]
    # id_type = models.CharField(choices=ID_TYPE_CHOICES)
    is_this_message_only_case = models.BooleanField(default=False)
    content = models.TextField(default='', blank = True, null=True)
    create_at = models.DateTimeField(auto_now=True, blank = True,null=True) 

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
    create_at = models.DateTimeField(auto_now=True, blank = True,null=True) 
    