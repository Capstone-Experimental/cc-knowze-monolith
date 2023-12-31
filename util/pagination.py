from rest_framework.pagination import PageNumberPagination

class ApiPagination(PageNumberPagination):
	page_size = 10
	page_size_query_param = 'page_size'
	max_page_size = 100
 
	# ?page=1&page_size=10