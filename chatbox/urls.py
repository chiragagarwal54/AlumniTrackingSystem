from django.urls import path, include
from chatbox.views import Chat
import trix

urlpatterns = [
    path('trix/',include('trix.urls')),
    path('chat/',Chat,name='chat'),
]