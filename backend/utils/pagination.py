"""
安全分页器 — 页码越界时返回空结果而非 404

DRF 默认 PageNumberPagination 在请求的页码超出有效范围时抛出
NotFound(404)。这会导致前端筛选条件改变后，残留的页码参数引发
404 错误。

本分页器覆盖了 paginate_queryset 方法，在页码无效时使用最后一页
（通常为空），同时覆盖 get_paginated_response 确保响应格式一致。
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from django.core.paginator import InvalidPage


class SafePageNumberPagination(PageNumberPagination):
    """页码越界时返回空页，而不是 404"""

    def paginate_queryset(self, queryset, request, view=None):
        self.request = request
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(request, paginator)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage:
            self.page = paginator.page(paginator.num_pages)

        if paginator.num_pages > 1 and self.template is not None:
            self.display_page_controls = True

        return list(self.page)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
        ]))
