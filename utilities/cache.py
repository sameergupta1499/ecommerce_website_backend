from django.core.cache import cache
from django.utils.cache import _i18n_cache_key_suffix
from hashlib import md5
from django.conf import settings
from urllib.parse import urlparse, parse_qs
from django.http import QueryDict   #use to query the parameters in an api
from urllib.parse import urlunparse


def sort_query_dict(query_dict):
    sorted_items = sorted(query_dict.items())
    sorted_query_dict = QueryDict('', mutable=True)
    for key, value in sorted_items:
        sorted_query_dict.appendlist(key, value)
    return sorted_query_dict

def change_page_to_current(api,page):
    parsed_url = urlparse(api)
    path = parsed_url.path
    query_string = parsed_url.query
    query_dict = QueryDict(query_string).copy()
    query_dict['p']=page
    query_dict_sorted = sort_query_dict(query_dict)
    if not page:    #for common page wide query, meaning where page is None
        query_dict_sorted.pop('p')
    url=urlunparse(("", "", path, "", query_dict_sorted.urlencode(), ""))
    return url

def _generate_cache_header_key(request, page="0"):
    """Return a cache key for the header cache."""
    base_path = request.get_full_path()   #will have everything except domain name
    url = change_page_to_current(base_path,page)
    cache_key = url
    return cache_key
    
def get_cache_key_from_request(request,page=None):
    key = _generate_cache_header_key(request, page=page)
    return key
    
def set_cache_data(key,data):
    cache.set(key, data,settings.CACHE_MIDDLEWARE_SECONDS)

def get_cache_data(key):
    data = cache.get(key)
    return data

def get_page_from_request(request):
    page_number = request.GET.get('p', '1')
    return page_number
