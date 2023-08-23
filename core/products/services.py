# def set_list_cache(self,queryset,req_page=):

#     serializer = self.get_serializer(page, many=True)
#     return self.get_paginated_response(serializer.data)
#     cached_data = cache.get(cache_key)
#     if cached_data is None:
#         # Data is not in cache, retrieve it from the source and set cache
#         data = ...  # Get or generate your data
#         cache.set(cache_key, data)
#         return Response(data)
#     else:
#         # Data is in cache, return it
#         return Response(cached_data)

def get_cached_paginated_response(self,queryset,curr_page_num=None):
    if curr_page_num is None:
        curr_page_num = self.get_current_page
    paginated_queryset = self.custom_paginate_queryset(queryset,req_page=curr_page_num)
    serializer = self.get_serializer(paginated_queryset, many=True)
    response = self.get_paginated_response(serializer.data)