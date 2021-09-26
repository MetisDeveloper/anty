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
    portalcode = models.IntegerField()
    detail1 = models.TextField(max_length=30)
    detail2 = models.TextField(max_length=30)
    detail3 = models.TextField(max_length=30, null=True)
    firstname = models.TextField(max_length=15)
    firstname_furi = models.TextField(max_length=20, null=True)
    lastname= models.TextField(max_length=15)
    lastname_furi = models.TextField(max_length=20, null=True)
    tel = models.CharField(max_length=32, null=False)
    primary = models.BooleanField(default=False)
