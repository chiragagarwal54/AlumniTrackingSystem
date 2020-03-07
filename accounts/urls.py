from django.urls import path, include

from accounts.views import (
        registration_view,
        logout_view,
        login_view,
)

app_name='accounts'


urlpatterns = [
    path('register/', registration_view, name="register"),
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name="login"),
]
