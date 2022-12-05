from reviews.models import Title
from django_filters import FilterSet, filters

class TitleFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    genre = filters.CharFilter(field_name='genre__slug')
    category = filters.CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ('name', 'category', 'genre', 'year')
