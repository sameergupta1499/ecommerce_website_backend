from django.urls import path
from .views import ProductsListView


urlpatterns = [
    path('products/<str:page>/', ProductsListView.as_view(), name='products-list'),
]
