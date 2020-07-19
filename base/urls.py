from django.urls import path

from base.views import(
    base,
    home,
    allnews,
    allevents,
    speceficevent,
    speceficnews,
    profile,
)

app_name='base'

urlpatterns = [
    path('', home, name="home"),
    path('event/<int:event_id>', speceficevent, name="speceficevent"),
    path('news/<int:news_id>', speceficnews, name="speceficnews"),
    path('news', allnews, name="allnews"),
    path('events', allevents, name="allevents"),
    path('profile',profile,name="profile"),
]
