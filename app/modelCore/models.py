import pathlib
from unicodedata import category
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.forms import FloatField
from django.urls import reverse
from django.db.models import Avg ,Sum 
from ckeditor_uploader.fields import RichTextUploadingField

def image_upload_handler(instance,filename):
    fpath = pathlib.Path(filename)
    new_fname = str(uuid.uuid1()) #uuid1 -> uuid + timestamp
    return f'images/{new_fname}{fpath.suffix}'

@property
def get_photo_url(self):
    if self.photo and hasattr(self.photo, 'url'):
        return self.photo.url
    else:
        return "/static/web/assets/img/generic/2.jpg"
class UserManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not phone:
            raise ValueError('Users must have an phone')
        # user = self.model(email=self.normalize_email(email), **extra_fields)
        user = self.model(
            phone = phone, 
            name=extra_fields.get('name'),
            line_id=extra_fields.get('line_id'),
            apple_id =extra_fields.get('apple_id'),
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
    apple_id = models.CharField(max_length= 100, blank = True, null=True, unique=True)

    # is_apply_servant == True => 已提交, 審核中
    # is_apply_servant == False => 未提交, or 需重新提交
    is_apply_servant = models.BooleanField(default=False) 
    is_servant_passed = models.BooleanField(default=False)
    is_fcm_notify = models.BooleanField(default=True)

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
    is_continuous_start_time = models.FloatField(default=0, blank=True, null=True)
    is_continuous_end_time = models.FloatField(default=24, blank=True, null=True)

    background_image = models.ImageField(upload_to=image_upload_handler, blank=True, null=True)

    ATMInfoBankCode = models.CharField(max_length=20, default='', blank = True, null=True)
    ATMInfoBranchBankCode = models.CharField(max_length=20, default='', blank = True, null=True)
    ATMInfoAccount = models.CharField(max_length=20, default='', blank = True, null=True)

    USERNAME_FIELD = 'phone'

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        licenses = License.objects.all()
        print(licenses)
        print('user',self)
        for license in licenses:
            if UserLicenseShipImage.objects.filter(user=self,license=license).count() == 0:
                instance = UserLicenseShipImage.objects.create(user=self,license=license)
                print(instance)

    @property
    def needer_avg_rating(self):
        avg_rating = Review.objects.filter(case__user=self,case_offender_rating__gte=1).aggregate(Avg('case_offender_rating'))['case_offender_rating__avg']
        if avg_rating != None:
            return round(avg_rating,1)
        else:
            return 0

    @property
    def needer_avg_rate_range(self):
        if Review.objects.filter(case__user=self,case_offender_rating__gte=1).count() > 0:
            avg_rating = Review.objects.filter(case__user=self,case_offender_rating__gte=1).aggregate(Avg('case_offender_rating'))['case_offender_rating__avg']
            return range(int(avg_rating))
        else:
            return range(0)

    @property
    def needer_avg_rating_is_half_star(self):
        if Review.objects.filter(case__user=self,case_offender_rating__gte=1).count() > 0:
            avg_rating = Review.objects.filter(case__user=self,case_offender_rating__gte=1).aggregate(Avg('case_offender_rating'))['case_offender_rating__avg']
            if (avg_rating -int(avg_rating)) >= 0.5:
            # 判斷
                return True
            else:
                return False
        else:
            return False

    @property
    def needer_avg_rating_empty_star_range(self):
        if Review.objects.filter(case__user=self,case_offender_rating__gte=1).count() > 0:
            avg_rating = Review.objects.filter(case__user=self,case_offender_rating__gte=1).aggregate(Avg('case_offender_rating'))['case_offender_rating__avg']
            if (avg_rating -int(avg_rating)) >= 0.5:
                return range(4-int(avg_rating))
            else:
                return range(5-int(avg_rating))
        else:
            return range(5)

    @property
    def needer_rate_nums(self):
        return Review.objects.filter(case__user=self,case_offender_rating__gte=1).count()

    @property
    def servant_avg_rating(self):
        servant_avg_rating = Review.objects.filter(servant=self,servant_rating__gte=1).aggregate(Avg('servant_rating'))['servant_rating__avg']
        if servant_avg_rating != None:
            return round(servant_avg_rating,1)
        else:
            return 0
    
    @property
    def servant_avg_rate_range(self):
        if Review.objects.filter(servant=self,servant_rating__gte=1).count() > 0:
            avg_rating = Review.objects.filter(servant=self,servant_rating__gte=1).aggregate(Avg('servant_rating'))['servant_rating__avg']
            return range(int(avg_rating))
        else:
            return range(0)

    @property
    def servant_avg_rating_is_half_star(self):
        if Review.objects.filter(servant=self,servant_rating__gte=1).count() > 0:
            avg_rating = Review.objects.filter(servant=self,servant_rating__gte=1).aggregate(Avg('servant_rating'))['servant_rating__avg']
            if (avg_rating -int(avg_rating)) >= 0.5:
            # 判斷
                return True
            else:
                return False
        else:
            return False

    @property
    def servant_avg_rating_empty_star_range(self):
        if Review.objects.filter(servant=self,servant_rating__gte=1).count() > 0:
            avg_rating = Review.objects.filter(servant=self,servant_rating__gte=1).aggregate(Avg('servant_rating'))['servant_rating__avg']
            if (avg_rating -int(avg_rating)) >= 0.5:
                return range(4-int(avg_rating))
            else:
                return range(5-int(avg_rating))
        else:
            return range(5)
    @property
    def servant_rate_nums(self):
        return Review.objects.filter(servant=self,servant_rating__gte=1).count()

class Service(models.Model):
    name = models.CharField(max_length= 100, unique=True)
    remark = models.CharField(max_length= 150, blank = True, null=True)
    is_increase_price = models.BooleanField(default=False)
    

    def __str__(self):
        return self.name

class UserWeekDayTime(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
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

    start_time_hour = models.IntegerField(default=8, blank=True, null=True)
    start_time_min = models.IntegerField(default=0, blank=True, null=True)

    end_time_hour = models.IntegerField(default=17, blank=True, null=True)
    end_time_min = models.IntegerField(default=0, blank=True, null=True)

class UserServiceShip(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ship_services',
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.RESTRICT,
        related_name='service_ships'
    )
    increase_percent = models.FloatField(default=0, blank = True, null=True)
    
class Language(models.Model):
    name = models.CharField(max_length= 100)
    def __str__(self):
        return self.name

class UserLanguage(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_languages'
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

    def save(self, *args, **kwargs):
        super(License, self).save(*args, **kwargs)
        users = User.objects.all()
        for user in users:
            if UserLicenseShipImage.objects.filter(user=user,license=self).count == 0:
                license_image_ship = UserLicenseShipImage.objects.create(user=user,license=self)
                print(license_image_ship)
        print("maybe save user_license_ship here")

class UserLicenseShipImage(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_license_images'
        )
    license = models.ForeignKey(
        License,
        on_delete=models.CASCADE,
        related_name='license_image_ships',
    )
    image = models.ImageField(upload_to=image_upload_handler, blank=True, null=True)
    isPassed = models.BooleanField(default=False)

class City(models.Model):
    name = models.CharField(max_length = 255, blank=True, null=True)
    newebpay_cityname = models.CharField(max_length = 255, blank=True, null=True)
    nameE = models.CharField(max_length = 255, blank=True, null=True, default='')
    def __str__(self):
            return self.name

class County(models.Model):
    city =  models.ForeignKey(
        City,
        on_delete=models.RESTRICT,
    )
    name = models.CharField(max_length=100, blank=True, null=True)
    addressCode = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
            return self.name

class UserServiceLocation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_locations',
    )
    city = models.ForeignKey(
        City,
        on_delete=models.RESTRICT,
        null=True,
        blank=True
    )
    # county =  models.ForeignKey(
    #     County,
    #     on_delete=models.RESTRICT,
    #     null=True,
    #     blank=True
    # )
    transfer_fee = models.IntegerField(default=0, blank=True, null=True)

class Case(models.Model):
    user = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        null=True
    )

    servant = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
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
        on_delete=models.RESTRICT,
        null=True,
        blank=True
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

    UNTAKEN = 'unTaken'
    UNCOMPLETE = 'unComplete'
    COMPLETE = 'Complete'
    CANCELED = 'Canceled'
    ENDEARLY = 'endEarly'
    STATE_CHOICES = [
        (UNTAKEN, '未承接'),
        (UNCOMPLETE, '未完成'),
        (COMPLETE,'已完成'),
        (CANCELED, '取消'),
        (ENDEARLY,'提早結束')
    ]
    state =  models.CharField(max_length=10, choices=STATE_CHOICES,default=UNTAKEN)

    age = models.IntegerField(default=0, blank=True, null=True)
    weight = models.IntegerField(default=0, blank=True, null=True)
    
    disease_remark = models.CharField(max_length= 255, blank=True, null=True)
    conditions_remark = models.CharField(max_length= 255, blank=True, null=True)

    is_continuous_time = models.BooleanField(default=False)

    is_taken = models.BooleanField(default=False)
    is_open_for_search = models.BooleanField(default=False)
    road_name = models.CharField(max_length= 255,default='')
    hospital_name = models.CharField(max_length= 255, default='')

    weekday = models.CharField(max_length=100, blank=True, null=True)
    start_time = models.FloatField(default=0, blank=True, null=True)
    end_time = models.FloatField(default=24, blank=True, null=True)
    start_datetime = models.DateTimeField(auto_now=False, blank=True, null=True)
    end_datetime = models.DateTimeField(auto_now=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=False, blank=True, null=True)
    taken_at = models.DateTimeField(auto_now=False, blank=True, null=True)
    emergencycontact_name = models.CharField(max_length=100,blank=True, null=True)
    emergencycontact_relation = models.CharField(max_length=100,blank=True, null=True)
    emergencycontact_phone = models.CharField(max_length=10,blank=True, null=True)

    @property
    def startTimeformat(self):
        hour = int(self.start_time)
        min = int((self.start_time - int(self.start_time))*60)
        if hour > 12:
            if hour < 10:
                hour_str = '0' + str(hour)
            else:
                hour_str = str(hour)
            if min <10 :
                min_str = '0' + str(min)
            else:
                min_str = str(min)
            return ('晚上 ' + hour_str + ':' + min_str)
        else:
            if hour < 10:
                hour_str = '0' + str(hour)
            else:
                hour_str = str(hour)
            if min <10 :
                min_str = '0' + str(min)
            else:
                min_str = str(min)
            return ('早上 ' + hour_str + ':' + min_str)
    
    @property
    def endTimeformat(self):
        hour = int(self.end_time)
        min = int((self.end_time - int(self.end_time))*60)
        if hour > 12:
            if hour < 10:
                hour_str = '0' + str(hour)
            else:
                hour_str = str(hour)
            if min <10 :
                min_str = '0' + str(min)
            else:
                min_str = str(min)
            return ('晚上 ' + hour_str + ':' + min_str)
        else:
            if hour < 10:
                hour_str = '0' + str(hour)
            else:
                hour_str = str(hour)
            if min <10 :
                min_str = '0' + str(min)
            else:
                min_str = str(min)
            return ('早上 ' + hour_str + ':' + min_str)

class TempCase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        null=True
    )
    servant = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        blank = True,
        null=True,
        related_name='servant_tempcase'
    )
    
    city = models.CharField(max_length= 100, blank=True, null=True)
    county = models.CharField(max_length= 100, blank=True, null=True)

    CARETYPE_CHOICES = [
        ('home', '居家照顧'),
        ('hospital', '醫院看護'),
    ]
    care_type = models.CharField(max_length=10, choices=CARETYPE_CHOICES,default='')

    name = models.CharField(max_length= 100, default='')

    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,default=MALE)

    UNTAKEN = 'unTaken'
    UNCOMPLETE = 'unComplete'
    COMPLETE = 'Complete'
    CANCELED = 'Canceled'
    ENDEARLY = 'endEarly'
    STATE_CHOICES = [
        (UNTAKEN, '未承接'),
        (UNCOMPLETE, '未完成'),
        (COMPLETE,'已完成'),
        (CANCELED, '取消'),
        (ENDEARLY,'提早結束')
    ]
    state =  models.CharField(max_length=10, choices=STATE_CHOICES,default=UNTAKEN)

    age = models.IntegerField(default=0, blank=True, null=True)
    weight = models.IntegerField(default=0, blank=True, null=True)
    
    disease_remark = models.CharField(max_length= 255, default='')
    conditions_remark = models.CharField(max_length= 255, default='')

    is_booking = models.BooleanField(default=False)
    is_continuous_time = models.BooleanField(default=False)

    is_taken = models.BooleanField(default=False)
    is_open_for_search = models.BooleanField(default=False)

    body_condition = models.CharField(max_length=255, blank=True, null=True)
    disease = models.CharField(max_length=255, blank=True, null=True)
    service = models.CharField(max_length=255, blank=True, null=True)
    increase_service = models.CharField(max_length=255, blank=True, null=True)
    road_name = models.CharField(max_length= 255,default='')
    hospital_name = models.CharField(max_length= 255, default='')

    weekday = models.CharField(max_length=100, blank=True, null=True)
    start_time = models.FloatField(default=0, blank=True, null=True)
    end_time = models.FloatField(default=24, blank=True, null=True)
    start_datetime = models.DateTimeField(auto_now=False, blank=True, null=True)
    end_datetime = models.DateTimeField(auto_now=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    emergencycontact_name = models.CharField(max_length=100, default='')
    emergencycontact_relation = models.CharField(max_length=100, default='')
    emergencycontact_phone = models.CharField(max_length=10, default='')

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
        on_delete = models.CASCADE,
        related_name='case_diseases'
    )
    disease = models.ForeignKey(
        DiseaseCondition,
        on_delete = models.CASCADE
    )

class CaseBodyConditionShip(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete = models.CASCADE,
        related_name='case_body_conditions'
    )
    body_condition = models.ForeignKey(
        BodyCondition,
        on_delete = models.CASCADE
    )

class CaseServiceShip(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete = models.CASCADE,
        related_name='case_services'
    )
    service = models.ForeignKey(
        Service,
        on_delete = models.CASCADE
    )

class Order(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete = models.CASCADE,
        related_name='case_orders',
    )
    user = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_orders'
    )
    servant = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        null=True,
        blank=True,
        related_name='servant_orders'
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
    
    transfer_fee = models.IntegerField(default=0, blank=True, null=True)
    number_of_transfer = models.IntegerField(default=0, blank=True, null=True)
    amount_transfer_fee = models.IntegerField(default=0, blank=True, null=True)

    wage_hour = models.IntegerField(default=0, blank=True, null=True)
    # wage_half_day = models.IntegerField(default=0, blank=True, null=True)
    # wage_one_day = models.IntegerField(default=0, blank=True, null=True)
    # hours_hour_work = models.FloatField(default=0, blank = True, null=True)
    # hours_half_day_work = models.FloatField(default=0, blank = True, null=True)
    # hours_one_day_work = models.FloatField(default=0, blank = True, null=True)

    work_hours = models.FloatField(default=0, blank = True, null=True)
    base_money = models.IntegerField(default=0, blank=True, null=True)

    platform_percent = models.FloatField(default=0, blank = True, null=True)
    platform_money = models.IntegerField(default=0, blank=True, null=True)
    
    total_money = models.IntegerField(default=0, blank=True, null=True)

    start_datetime = models.DateTimeField(auto_now=False, blank=True, null=True)
    end_datetime = models.DateTimeField(auto_now=False, blank=True, null=True)

    start_time = models.FloatField(default=0, blank=True, null=True)
    end_time = models.FloatField(default=24, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now=False, blank = True,null=True) 

    refund_money = models.IntegerField(default=0, blank=True, null=True)
    refund_apply_date = models.DateTimeField(auto_now=True, blank = True,null=True)

    @property
    def TaxAmt(self):
        tax_percent = (self.platform_percent - 2.8)
        return (self.total_money * tax_percent)/100

class OrderIncreaseService(models.Model):
    order =  models.ForeignKey(
        Order,
        on_delete = models.CASCADE,
        related_name='order_increase_services',
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.RESTRICT
    )
    increase_percent = models.FloatField(default=0, blank = True, null=True)

    increase_money = models.IntegerField(default=0, blank=True, null=True)

class OrderWeekDay(models.Model):
    order =  models.ForeignKey(
        Order,
        on_delete = models.CASCADE,
        related_name='order_weekdays',
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
        on_delete=models.CASCADE,
        related_name='order_reviews'
    )
    case = models.ForeignKey(
        Case,
        on_delete = models.CASCADE,
        null=True,
        blank=True,
        related_name='case_reviews'
    )
    servant = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='servant_reviews'
    )

    case_offender_rating =  models.FloatField(default=0, blank = True, null=True)
    case_offender_comment = models.CharField(max_length = 255, blank = True, null=True)
    case_offender_rating_created_at= models.DateTimeField(auto_now=False, blank = True,null=True) 

    servant_rating =  models.FloatField(default=0, blank = True, null=True)
    servant_comment = models.CharField(max_length = 255, blank = True, null=True)
    servant_rating_created_at = models.DateTimeField(auto_now=False, blank = True,null=True) 

    @property
    def servant_rating_range(self):
        # return range(6)
        return range(int(self.servant_rating))
    
    @property
    def servant_rating_is_half_star(self):
        if (self.servant_rating -int(self.servant_rating)) >= 0.5:
        # 判斷
            return True
        else:
            return False

    @property
    def servant_rating_empty_star_range(self):
        if (self.servant_rating -int(self.servant_rating)) >= 0.5:
            return range(4-int(self.servant_rating))
        else:
            return range(5-int(self.servant_rating))

    @property
    def case_offender_rating_range(self):
        # return range(6)
        return range(int(self.case_offender_rating))
    
    @property
    def case_offender_rating_is_half_star(self):
        if (self.case_offender_rating -int(self.case_offender_rating)) >= 0.5:
        # 判斷
            return True
        else:
            return False

    @property
    def case_offender_rating_empty_star_range(self):
        if (self.case_offender_rating -int(self.case_offender_rating)) >= 0.5:
            return range(4-int(self.case_offender_rating))
        else:
            return range(5-int(self.case_offender_rating))
    
class PayInfo(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.RESTRICT,
        default=''
    )
    
    PaymentType = models.CharField(max_length=100, default='', blank = True, null=True)
    MerchantID = models.CharField(max_length=100, default='', blank = True, null=True)
    
    OrderInfoMerchantOrderNo = models.CharField(max_length=100, default='', blank = True, null=True)
    OrderInfoTradeDate = models.DateTimeField(auto_now=False,null=True)
    OrderInfoTradeNo = models.CharField(max_length=100, default='', blank = True, null=True)
    OrderInfoTradeAmt = models.IntegerField(default=0, null=True)
    OrderInfoPaymentType = models.CharField(max_length=20, default='', blank = True, null=True)
    OrderInfoPayTime = models.DateTimeField(auto_now=False,null=True)
    OrderInfoTradeStatus = models.CharField(max_length=20, default='', blank = True, null=True)

    EscrowBank = models.CharField(max_length=10, default='', blank = True, null=True)
    AuthBank = models.CharField(max_length=10, default='', blank = True, null=True)
    Auth = models.CharField(max_length=6, default='', blank = True, null=True)

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

class ChatroomMessage(models.Model):
    chatroom = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='chatroom_messages',
    )
    # user is the one who make message
    user = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        null=True
    )
    case = models.ForeignKey(
        Case,
        on_delete = models.CASCADE,
        blank=True,
        null=True,
    )
    order = models.ForeignKey(
        Order,
        on_delete = models.CASCADE,
        blank=True,
        null=True,
    )

    is_this_message_only_case = models.BooleanField(default=False)
    content = models.TextField(default='', blank = True, null=True)
    create_at = models.DateTimeField(auto_now=True, blank = True,null=True) 

    image = models.ImageField(upload_to=image_upload_handler, blank=True, null=True)
    is_read_by_other_side = models.BooleanField(default=False)

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
    order = models.ForeignKey(
        Order,
        on_delete = models.CASCADE,
        blank=True,
        null=True,
    )
    content = models.TextField(default='', blank = True, null=True)
    create_at = models.DateTimeField(auto_now=True, blank = True,null=True) 
    
class UserStore(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    MerchantID = models.CharField(max_length = 255, blank = True, null=True)
    MerchantHashKey = models.CharField(max_length = 255, blank = True, null=True)
    MerchantIvKey = models.CharField(max_length = 255, blank = True, null=True)
    LoginAccount = models.CharField(max_length = 100, blank = True, null=True)
    MemberUnified = models.CharField(max_length = 100, blank = True, null=True)

class BlogCategory(models.Model):
    name = models.CharField(max_length = 255, blank = True, null=True)

class BlogPost(models.Model):
    title = models.CharField(max_length = 255, blank = True, null=True)
    body = RichTextUploadingField(config_name='default')

    STATE_CHOICES = [
        ('draft', 'draft'),
        ('publish', 'publish'),
    ]
    state = models.CharField(max_length=10, choices=STATE_CHOICES)

    cover_image = models.ImageField(upload_to=image_upload_handler, blank=True, null=True)

    create_date = models.DateField(blank = True, null=True)
    publish_date = models.DateField(blank = True, null=True)

    def __str__(self):
        return self.title

class BlogPostCategoryShip(models.Model):
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='ship_categories',
    )
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.CASCADE,
        related_name='ship_posts',
    )

class MonthSummary(models.Model):
    month_date = models.DateField(null=True)

    # 訂單產生就計營收(所有的當月訂單, 有paid, unPaid, canceled)
    month_revenue = models.IntegerField(default=0)
    # 訂單最終沒付款成功, 就是 cancel 的訂單, cancel 的訂單金額總和
    month_cancel_amount = models.IntegerField(default=0)

    # 成功請款的訂單金額總和(paid的當月訂單)
    month_pay_amount = models.IntegerField(default=0)
    # 退款的訂單金額總和(當月訂單的 refund money)
    month_refound_amount = models.IntegerField(default=0)

    # 平台收入, 成功請款的訂單, 依平台比例收取費用之總和 (paid 訂單的 paltform money 相加)
    month_platform_revenue = models.IntegerField(default=0)

class AssistancePost(models.Model):
    title = models.CharField(max_length = 255, blank = True, null=True)
    body = RichTextUploadingField(config_name='default')
    create_date = models.DateField(blank = True, null=True)