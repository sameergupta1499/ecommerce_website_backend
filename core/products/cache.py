from django.core.cache import cache
from django.utils.cache import _i18n_cache_key_suffix
from hashlib import md5
from django.conf import settings

def _generate_cache_header_key(key_prefix, request, params=True):
    """Return a cache key for the header cache."""
    base_url = request.build_absolute_uri()
    if not params:
        base_url = base_url.split('?')[0]
    url = md5(base_url.encode("ascii"), usedforsecurity=False)
    cache_key = "views.decorators.cache.cache_header.%s.%s" % (
        key_prefix,
        url.hexdigest(),
    )
    return _i18n_cache_key_suffix(request, cache_key)

def set_common_cache_key(request,data,params=False):
    key = _generate_cache_header_key("_common_pages_", request, params=params)
    print(data)
    cache.set(key, data)

def get_common_cache_key(request,params=False):
    key = _generate_cache_header_key("_common_pages_", request, params=params)
    data = cache.get(key)
    return data

def get_cache_key_from_request(request,prefix=None,params=True):
    key = _generate_cache_header_key(prefix, request, params=params)
    return key
    
def set_cache_data(key,data):
    cache.set(key, data)

def get_cache_data(key,data):
    data = cache.get(key)
    return data