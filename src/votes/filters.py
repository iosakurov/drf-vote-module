import django_filters
from .models import Vote


class VoteFilter(django_filters.FilterSet):
    voter = django_filters.CharFilter(field_name='voter__user__username', lookup_expr='iexact')
    candidate = django_filters.CharFilter(field_name='candidate__user__username', lookup_expr='iexact')

    class Meta:
        model = Vote
        fields = ['id', 'candidate', 'voter', 'is_like']
