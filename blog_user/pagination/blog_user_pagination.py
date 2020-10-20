from rest_framework import pagination


class BlogUserPagination(pagination.PageNumberPagination):

    # 每页显示的数量
    page_size = 20
    # 每页显示的最大数量
    max_page_size = 50
    # 搜索的参数关键字，即 ?
    page_query_param = 'page'
    # 控制每页显示数量的关键字
    page_size_query_param = 'size'
