from threading import Thread
from django.dispatch import Signal
from rest_framework import exceptions
post_response = Signal()

def create_cached_pages(sender,**kwargs):
    import time

    def long_running_task():
        self = sender
        queryset = kwargs["queryset"]
        time.sleep(2)
        curr_page = int(self.get_current_page)
        i = curr_page
        while (i < curr_page + 5):    #Caching next 5 pages
            i += 1
            try:
                self.get_cached_paginated_data(queryset,curr_page_num=i)
                self.get_cached_common_data()
            except exceptions.NotFound:    #for page number not there
                pass
    t = Thread(target=long_running_task)
    t.start()
    pass








# from django.dispatch import receiver
# from django.core.signals import request_finished
# from django.dispatch import Signal
# import time
# # post_response = Signal()

# from background_task import background
# @background(schedule=1)
# def create_cached_pages(arg1, arg2):
#     from core.products.views import BaseProductListView
#     # self = kwargs["response"]
#     # print("Create1 cached pages signal triggered.",self)
#     # queryset = self.filter_queryset(self.get_queryset())
#     # data = self.get_cached_paginated_data(queryset,curr_page_num='283')
#     print("here timer started",arg1, arg2)
#     # time.sleep(5)
#     # Perform your desired actions here
#     print("Create cached pages signal triggered.")
#     # Additional functionality

