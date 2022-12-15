from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
 
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 2000