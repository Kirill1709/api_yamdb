import django_filters as filters

from .models import Title


class TitleFilter(filters.FilterSet):

    category = filters.CharFilter(
        field_name='category__slug', lookup_expr='exact')
    genre = filters.CharFilter(field_name='genre__slug', lookup_expr='exact')
    name = filters.CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        fields = ('name', 'category', 'genre', 'year')
        model = Title
