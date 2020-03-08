from django.urls import path, include

from accounts.views import (
        alumni_signup_view,
        faculty_signup_view,
        logout_view,
        login_view,
        signup_view,
)

app_name='accounts'


urlpatterns = [
    path('signup/alumni/', alumni_signup_view.as_view(), name="alumni_signup"),
    path('signup/faculty/', faculty_signup_view.as_view(), name="faculty_signup"),
    path('signup/', signup_view, name="signup"),
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name="login"),
]
