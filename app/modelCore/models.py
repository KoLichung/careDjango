import pathlib
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.urls import reverse

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
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'

class MarkupItems(models.Model):
    name = models.CharField(max_length= 100, unique=True)
    price = models.IntegerField(default=0, blank = True, null=True)
    def __str__(self):
            return self.name

class Category(models.Model):
    care_type = models.CharField(max_length= 100, unique=True)
    time_type =models.CharField(max_length= 100, unique=True)
    


class LanguageSkills(models.Model):
    name = models.CharField(max_length= 100, unique=True)

    def __str__(self):
        return self.name

class License(models.Model):
    name = models.CharField(max_length= 100, unique=True)
    def __str__(self):
        return self.name

class Servant(models.Model):
    name = models.CharField(max_length= 100, unique=True)
    hourly_wage = models.IntegerField(default=0, blank = True, null=True)
    halfday_wage = models.IntegerField(default=0, blank = True, null=True)
    oneday_wage = models.IntegerField(default=0, blank = True, null=True)
    
    info = models.CharField(max_length= 255, blank = True, null=True)
    markup_items = models.ForeignKey(
        MarkupItems,
        on_delete=models.RESTRICT
    )
    skills = models.ForeignKey(
        LanguageSkills,
        on_delete=models.RESTRICT
    )
def image_upload_handler(instance,filename):
    fpath = pathlib.Path(filename)
    new_fname = str(uuid.uuid1()) #uuid1 -> uuid + timestamp
    return f'images/{new_fname}{fpath.suffix}'

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

class ServantCategoryShip(models.Model):
    servant = models.ForeignKey(
        Servant,
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
class Disease(models.Model):
    name = models.CharField(max_length = 255, blank = True, null=True)

    def __str__(self):
            return self.name

class BodyConditions(models.Model):
    name = models.CharField(max_length = 255, blank = True, null=True)

    def __str__(self):
            return self.name

class Recipient(models.Model):
    name = models.CharField(max_length= 100, unique=True)
    customer =models.ForeignKey(User,on_delete=models.RESTRICT)

    gender = models.CharField(max_length= 100, blank = True, null=True)
    age = models.IntegerField(default=0, blank = True, null=True)
    weight = models.IntegerField(default=0, blank = True, null=True)
    disease = models.ForeignKey(Disease,on_delete=models.RESTRICT)

    disease_info = models.CharField(max_length= 255, blank = True, null=True)
    conditions = models.ForeignKey(BodyConditions,on_delete=models.RESTRICT)

    conditions_info = models.CharField(max_length= 255, blank = True, null=True)

class ServiceItems(models.Model):
    name = models.CharField(max_length = 100, blank = True, null=True)
    info = models.CharField(max_length = 255, blank = True, null=True)
    def __str__(self):
            return self.name

class City(models.Model):
    name = models.CharField(max_length = 255, blank = True, null=True)

    def __str__(self):
            return self.name

class CityArea(models.Model):
    city = models.CharField(max_length = 100, blank = True, null=True)
    area = models.CharField(max_length = 100, blank = True, null=True)

class Transportation(models.Model):
    servant = cityarea = models.ForeignKey(
        Servant,
        on_delete=models.CASCADE
    )
    cityarea = cityarea = models.ForeignKey(
        CityArea,
        on_delete=models.CASCADE
    )
    
class Case(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.RESTRICT
    )
    service_items = models.ForeignKey(
        ServiceItems,
        on_delete=models.RESTRICT
    )
    cityarea = models.ForeignKey(
        CityArea,
        on_delete=models.RESTRICT
    )
    start_date = models.DateTimeField(auto_now=False, blank = True,null=True)
    end_date = models.DateTimeField(auto_now=False, blank = True,null=True) 
    start_time = models.TimeField(auto_now=False, auto_now_add=False )
    end_time = models.TimeField(auto_now=False, auto_now_add=False )


class ServantReview(models.Model):
    servant = models.ForeignKey(
        Servant,
        on_delete=models.RESTRICT
    )
    score =  models.IntegerField(default=0, blank = True, null=True)
    content = models.CharField(max_length = 255, blank = True, null=True)
    create_date = models.DateTimeField(auto_now=False, blank = True,null=True) 

class CustomerReview(models.Model):
    customer = models.ForeignKey(
        User,
        on_delete=models.RESTRICT
    )
    score =  models.IntegerField(default=0, blank = True, null=True)
    content = models.CharField(max_length = 255, blank = True, null=True)
    create_date = models.DateTimeField(auto_now=False, blank = True,null=True) 
