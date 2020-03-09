from django.db import models

class College(models.Model):
    name = models.CharField(max_length=200)
    year_of_establish = models.IntegerField()
    address = models.TextField(null=True)
    website = models.URLField(max_length=300, null=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
