from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class Prefectures(models.Model):
    name =  models.TextField(max_length=4)


class User(AbstractUser):
    username = models.CharField(_('username'), max_length=32, null=True, default="ゲスト")
    email = models.EmailField(_('email address'), unique=True)
    tel = models.CharField(_('tel'), max_length=32, null=False)
    stripe_id = models.TextField(max_length=50, null=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Profile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    intro = models.TextField(max_length=100000)
    firstnmae_furi = models.TextField(max_length=20, null=True)
    lastname_furi = models.TextField(max_length=20, null=True)

class Follow(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')


class Point(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    point = models.IntegerField()

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prefecture = models.ForeignKey(Prefectures, on_delete=models.CASCADE)
    postalcode = models.IntegerField()
    detail1 = models.TextField(max_length=30)
    detail2 = models.TextField(max_length=30)
    detail3 = models.TextField(max_length=30, null=True)
    detail4 = models.TextField(max_length=30, null=True)
    kana1 = models.TextField(max_length=30)
    kana2 = models.TextField(max_length=30)
    kana3 = models.TextField(max_length=30, null=True)
    kana4 = models.TextField(max_length=30, null=True)
    firstname = models.TextField(max_length=15)
    firstname_furi = models.TextField(max_length=20, null=True)
    lastname= models.TextField(max_length=15)
    lastname_furi = models.TextField(max_length=20, null=True)
    tel = models.CharField(max_length=32, null=False)



class Line_user(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    name = models.TextField(max_length=10, null=True)
    line_id  = models.TextField(max_length=30)
    message_status = models.IntegerField()
    broadcast = models.TextField(max_length=1000, null=True)


class Brand(models.Model):
    name = models.TextField(max_length=30)
    image_url = models.TextField(max_length=100)
    code = models.BooleanField(default=False)

class Gender(models.Model):
    name = models.TextField(max_length=30)
    image_url = models.TextField(max_length=100, null=True)


class Category(models.Model):
    name = models.TextField(max_length=30)
    image_url = models.TextField(max_length=100, null=True)



class Temp_used_product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.TextField(max_length=30)
    intro = models.TextField(max_length=1000, null=True)
    base_price = models.IntegerField()



class Sche_sipping_date(models.Model):
    display = models.TextField(max_length=10)


class Product_status(models.Model):
    display = models.TextField(max_length=1000)


class Hope_sell(models.Model):
    display = models.TextField(max_length=1000)


class Used_product(models.Model):
    temp_product = models.ForeignKey(Temp_used_product, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_user')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, related_name='buyer_user')
    price = models.IntegerField()
    explain = models.TextField(max_length=1000)
    schedule = models.ForeignKey(Sche_sipping_date, on_delete=models.CASCADE)
    status = models.ForeignKey(Product_status, on_delete=models.CASCADE)
    hope = models.ForeignKey(Hope_sell, on_delete=models.CASCADE)
    is_released = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

class Used_product_image(models.Model):
    used_product = models.ForeignKey(Used_product, on_delete=models.CASCADE)
    path = models.TextField(max_length=1000)


class favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Used_product, on_delete=models.CASCADE)