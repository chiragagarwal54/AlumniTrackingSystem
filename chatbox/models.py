from django.db import models
from accounts.models import User
from froala_editor.fields import FroalaField
from trix.fields import TrixField
# Create your models here.

class Message(models.Model):
    pub_date = models.DateTimeField()
    message_text = TrixField('Content')
    sent_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.sent_by.username



