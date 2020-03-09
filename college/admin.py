from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from college.models import College, Department

admin.site.register(College)
admin.site.register(Department)
