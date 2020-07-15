from django.urls import path

from base.views import(
    base,
    home,
    allnews,
    allevents,
    speceficevent,
)

app_name='base'

urlpatterns = [
    path('', home, name="home"),
    path('event/<int:event_id>', speceficevent, name="speceficevent"),
    path('allnews', allnews, name="allnews"),
    path('allevents', allevents, name="allevents")
]
