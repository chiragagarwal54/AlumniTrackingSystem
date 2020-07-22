from django.urls import path

from base.views import(
    base,
    home,
    allnews,
    allevents,
    speceficevent,
    speceficnews,
    profile,
    searchalumni,
    speceficstory,
    autocomplete
)

app_name='base'

urlpatterns = [
    path('', home, name="home"),
    path('profile/<slug:user_name>/<int:user_id>', profile, name="profile"),
    path('event/<int:event_id>', speceficevent, name="speceficevent"),
    path('news/<int:news_id>', speceficnews, name="speceficnews"),
    path('story/<int:story_id>', speceficstory, name="speceficstory"),
    path('news', allnews, name="allnews"),
    path('events', allevents, name="allevents"),
    path('searchalumni', searchalumni, name="searchalumni"),
    path('autocomplete', autocomplete, name="autocomplete")
]
