"""
Override pagination setup
"""

from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'current': self.page.number,
                'first': 1,
                'last': self.page.paginator.num_pages,
                'next': self.page.next_page_number() if self.page.has_next() else None,
                'previous': self.page.previous_page_number() if self.page.has_previous() else None,
            },
            'count': self.page.paginator.count,
            'showing': len(data),
            'results': data
        })
