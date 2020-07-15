from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from accounts.models import User, Alumni, Faculty
from django.db.models.signals import pre_save
from django.utils.text import slugify


def upload_event_image_location(instance, filename):
    file_path = 'event/{event_id}/{filename}'.format(
        event_id=str(instance.id),
        filename=filename
    )
    return file_path


def upload_notice_image_location(instance, filename):
    file_path = 'notice/{notice_id}/{filename}'.format(
        notice_id=str(instance.id),
        filename=filename
    )
    return file_path


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=300)
    image = models.ImageField(upload_to=upload_event_image_location, null=True, blank=True)
    body = models.CharField(max_length=1000)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.title

class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    date_time = models.DateTimeField(auto_now=True)
    body = models.CharField(max_length=1000)
    slug = models.SlugField()

    def __str__(self):
        return self.title

class Notice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to=upload_event_image_location, null=True, blank=True)
    body = models.CharField(max_length=1000)

    def __str__(self):
        return self.title

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = models.TextField()
    date_time = models.DateTimeField(auto_now=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title


@receiver(post_delete, sender=Event)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


@receiver(post_delete, sender=Notice)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

def pre_save_Event(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(pre_save_Event, sender=Event)

def pre_save_News(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(pre_save_News, sender=News)

def pre_save_Story(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(pre_save_Story, sender=Story)
