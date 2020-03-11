from django import forms
from trix.widgets import TrixEditor

class MessageForm(forms.Form):
    content = forms.CharField(widget=TrixEditor)