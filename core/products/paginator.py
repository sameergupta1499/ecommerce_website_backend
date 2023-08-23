from rest_framework.pagination import PageNumberPagination
from django.core.paginator import InvalidPage
from rest_framework.exceptions import NotFound
from collections import OrderedDict

class CustomPagination(PageNumberPagination):
    page_size = 50
    page_query_param = 'p'

    def paginate_queryset(self, queryset, request, req_page=None,view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        self.request = request
        page_size = self.get_page_size(request)
        if not page_size:
            return None
        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(request, paginator)
        
        if req_page:    #Custom: change page number based on method arguments
            page_number = req_page      
        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        # if paginator.num_pages > 1 and self.template is not None:
        #     # The browsable API should display pagination controls.
        #     self.display_page_controls = True

        return list(self.page)


    def get_page_size(self, request):
        page_size = request.query_params.get('page_size')
        if page_size:
            return int(page_size)
        return self.page_size
    
    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['total_pages'] = self.page.paginator.num_pages
        response.data['current_page'] = self.page.number
        return response
    
    