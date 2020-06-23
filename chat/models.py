from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import Alumni, Faculty, User
from PIL import Image
import io

# Create your models here.

def get_sentinal_user():
    return get_user_model().objects.get_or_create(username="deleted")[0]

class Messages(models.Model):
    parent_user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_text = models.TextField()
    date_posted = models.DateTimeField(default=timezone.localtime().now)

    def __str__(self):
        tup = tuple([self.parent_user, self.message_text])
        return str(tup)

    def last_10_messages(times=0):
        if not times:
            return list(Messages.objects.order_by("date_posted"))[-30:]
        return list(Messages.objects.order_by("date_posted"))[(-30*(times+1)):(-30*times)]