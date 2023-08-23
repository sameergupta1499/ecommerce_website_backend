from rest_framework import generics
from django_filters import rest_framework as filters
from .models import Products
from .filters import ProductsFilter
from .serializers import ProductsSerializer
from .paginator import CustomPagination
from .consts import CachePrefix
from django.db.models.functions import Lower
from utilities.utils import count_database_hits
from django.db import connection
from rest_framework.response import Response
from django.utils.cache import _generate_cache_key
from utilities.cache import get_cache_key_from_request,set_cache_data,get_cache_data,get_page_from_request
from utilities.utils import count_database_hits_with_details
# from .signals import post_response

class BaseProductListView(generics.ListAPIView):
    queryset = Products.objects.all().order_by('id')
    serializer_class = ProductsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductsFilter
    pagination_class = CustomPagination
    
    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def custom_paginate_queryset(self, queryset,req_page=None):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request,req_page=req_page, view=self)
    
    @property
    def get_current_page(self):
        page_number = self.request.GET.get('p', '1')
        return page_number
    
    def get_cached_paginated_data(self,queryset,curr_page_num=None):
        if curr_page_num is None:
            curr_page_num = self.get_current_page
        cache_list_key = get_cache_key_from_request(self.request, page=curr_page_num)
        cache_data = get_cache_data(cache_list_key)    #getting cache key from redis
        if cache_data:
            return cache_data 
        paginated_queryset = self.custom_paginate_queryset(queryset,req_page=curr_page_num)  
        serializer = self.get_serializer(paginated_queryset, many=True)
        response = self.get_paginated_response(serializer.data)
        data = response.data
        set_cache_data(cache_list_key, data)         #setting cache data 
        

        return data
    
    def get_cached_common_data(self):
        cache_page_key = get_cache_key_from_request(self.request,page=None)
        cache_data = get_cache_data(cache_page_key)    #getting cache key from redis
        if cache_data:
            return cache_data
        data = {}
        seller_params = {key: ','.join(values) for key, values in self.request.GET.lists() if key != 'brands'}
        category_params = {key: ','.join(values) for key, values in self.request.GET.lists() if key != 'category'}
        # brands_in_filtered_queryset = queryset.order_by('seller').values_list('seller',flat=True).distinct('seller')   #getting brands in the filtered queryset
        seller_queryset = ProductsFilter(seller_params, queryset=self.get_queryset()).qs
        category_queryset = ProductsFilter(category_params, queryset=self.get_queryset()).qs

        #LOGIC: We run the filtered_queryset again for seller and category with original self.get_queryset (only has page filter). For seller we don't consider 
        # seller as a filter because we want all the sellers that provides the requested filtered response. Same goes for category.
        data["seller"] = seller_queryset.order_by('seller').values_list('seller',flat=True).distinct('seller')
        data["category"] = category_queryset.order_by('category').values_list('category',flat=True).distinct('category')
        data["gender"] = (self.get_queryset()).order_by('gender').values_list('gender',flat=True).distinct('gender')
        # data["sizes"] = list(set(queryset.values_list('sizes', flat=True)))
        set_cache_data(cache_page_key, data)
        return data
        

        
class ProductsListView(BaseProductListView):

    def get_queryset(self):
        page = self.kwargs['page']  # Access the captured category from the URL
        queryset = Products.objects.filter(page=page).order_by('id')
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())    #filters out the products based on request params.
        data = self.get_cached_paginated_data(queryset)
        common_data = self.get_cached_common_data()
        data.update(common_data)
        from core.products.signals import post_response
        post_response.send(sender=self,queryset=queryset)
        print("called created_pages")
        return Response(data)