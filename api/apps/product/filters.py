import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr='icontains')
    description = django_filters.CharFilter(field_name="description", lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['title', 'description']