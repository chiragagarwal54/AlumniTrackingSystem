from django.db import models
from accounts.models import User, Alumni, Faculty

class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    organisation = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.title
