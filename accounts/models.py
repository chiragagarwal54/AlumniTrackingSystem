from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings

class MyAccountManager(BaseUserManager):
    def create_user(self, email, unique_id, first_name, last_name, college, dob, department, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not unique_id:
            raise ValueError("Users must have a valid unique Id")
        if not first_name:
            raise ValueError("Users must enter First Name")
        if not last_name:
            raise ValueError("Users must enter Last Name")
        if not college:
            raise ValueError("Users must select a college")
        if not dob:
            raise ValueError("Users must enter a valid Date of Birth")
        if not department:
            raise ValueError("Users must select a department")

        user = self.model(
                email=self.normalize_email(email),
                unique_id=unique_id,
                first_name=first_name,
                last_name=last_name,
                college=college,
                dob=dob,
                department=department,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, unique_id, first_name, last_name, dob, college, department, password):
        user = self.create_user(
                email=self.normalize_email(email),
                unique_id=unique_id,
                password=password,
                first_name=first_name,
                last_name=last_name,
                dob=dob,
                college=college,
                department=department,
        )

        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email =                 models.EmailField(verbose_name="EmailId", max_length=100, unique=True)
    username =              models.CharField(max_length=100)
    date_joined =           models.DateTimeField(verbose_name="Date Joined", auto_now_add=True)
    unique_id =             models.CharField(max_length=50, unique=True)
    last_login =            models.DateTimeField(verbose_name="Last Login", auto_now=True)
    is_admin =              models.BooleanField(default=False)
    is_active =             models.BooleanField(default=True)
    is_staff =              models.BooleanField(default=False)
    is_superuser =          models.BooleanField(default=False)
    first_name =            models.CharField(max_length=100)
    last_name =             models.CharField(max_length=100)
    dob =                   models.DateField(null=True)
    college =               models.CharField(max_length=200, null=True)
    department =            models.CharField(max_length=200, null=True)
    year_of_graduation =    models.DateField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['unique_id','first_name','last_name','college','dob','department']

    objects = MyAccountManager()

    def __str__(self):
        return self.unique_id + ", " + self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_Label):
        return True
