from accounts.models import User, Alumni
from college.models import College, Department
import django_filters

class UserFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    college = django_filters.ModelChoiceFilter(queryset=College.objects.all())

    class Meta:
        model = User
        fields = ['full_name', 'first_name', 'last_name', 'college', ]
