from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from college.models import College, Department

def upload_user_image_location(instance, filename):
    file_path = 'user/{user_id}/{filename}'.format(
        user_id=str(instance.id),
        filename=filename
    )
    return file_path


class User(AbstractUser):
    is_verified = models.BooleanField(default=False)
    is_alumni = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to=upload_user_image_location)
    profile_complete = models.BooleanField(default=0)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.SlugField(editable=False, null=True, blank=True)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    dob = models.DateField(null=True)
    system_date_joined = models.DateTimeField(
        verbose_name="Date Joined", auto_now=True
    )
    system_last_login = models.DateTimeField(verbose_name="Last Login", auto_now=True)
    email = models.EmailField(null=True, unique=True)

class Position(models.Model):
    position_name = models.CharField(max_length=200)

    def __str__(self):
        return self.position_name


class Alumni(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year_of_passing = models.IntegerField(null=True)
    unique_id = models.CharField(unique=True, max_length=200)
    profile_verified = models.BooleanField(default=0)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return (
            self.user.first_name
            + " "
            + self.user.last_name
        )


class Faculty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    college_joined_year = models.IntegerField(null=True)
    research_interest = models.CharField(max_length=300, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return (
            self.user.first_name
            + " "
            + self.user.last_name
            + ", "
            + self.user.department.name
            + ", "
            + self.user.college.name
        )
