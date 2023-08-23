from .signals import post_response, create_cached_pages

default_app_config = "core.products.apps.ProductsConfig"

post_response.connect(create_cached_pages)