from rest_framework.pagination import PageNumberPagination

class GeneralListPagination(PageNumberPagination):
    page_size = 5
