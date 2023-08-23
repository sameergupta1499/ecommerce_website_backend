from django_filters import rest_framework as filters
from .models import Products
from django.db import models

class ProductsFilter(filters.FilterSet):
    brands = filters.BaseInFilter(field_name="seller", lookup_expr='in')
    category = filters.BaseInFilter(field_name="category", lookup_expr='in')
    ordering = filters.OrderingFilter(
        fields=(
            ('price', 'price_lth'),
            ('-price', 'price_htl'),
            ('-ratingtotal', 'ratingtotal_htl'),
            ('-discount', 'discount_htl'),
            ('-rating', 'rating_htl'),
            ('id', 'recommended'),
        )
    )
    def get_ordering(self, request, queryset, view):
        # Get the provided ordering value from the request parameters
        ordering = super().get_ordering(request, queryset, view)

        # If no explicit ordering is provided, use 'recommended' as the default
        if not ordering:
            return 'recommended'

        return ordering 
    class Meta:
        model = Products
        fields = (
            'id',
            'name',
            'price',
            "ordering",
            'mrp',
            'rating',
            'ratingtotal',
            'discount',
            'category',
            'gender',
            'page',
            'product_id',
            'sizes',
            'brands'
        )