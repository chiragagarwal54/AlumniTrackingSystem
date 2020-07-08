from django.urls import path

from base.views import(
    base,
    home,
    allnews,
)

app_name='base'

urlpatterns = [
    path('', home, name="home"),
    path('allnews', allnews, name="allnews"),
]
