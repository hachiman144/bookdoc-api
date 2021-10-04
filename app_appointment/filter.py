"""
Appointment App filter
"""
from datetime import datetime, date, time

import pytz
from django.db.models import Q
from rest_framework.filters import BaseFilterBackend
import coreapi


class AppointmentFilter(BaseFilterBackend):
    """
    Appointment Filter
    """

    def get_schema_fields(self, view):
        if view.action == 'list':
            schema = [
                coreapi.Field(
                    name='date_from',
                    location='query',
                    required=False,
                    type='string',
                    description='Filter by Date Range.',
                ),
                coreapi.Field(
                    name='date_to',
                    location='query',
                    required=False,
                    type='string',
                    description='Filter by Date Range.',
                ),
                coreapi.Field(
                    name='name',
                    location='query',
                    required=False,
                    type='string',
                    description='Filter by Patient Name.',
                ),
            ]
            return schema
        return ''

    def filter_queryset(self, request, queryset, view):
        """
        Filter queryset for Grade Filter
        """

        queryset = queryset.order_by('pk')
        if view.action == 'list':
            query_params = request.query_params

            if query_params.get('date_from', '') != '' or query_params.get('date_to', '') != '':
                datetime_from = datetime.strptime(query_params.get('date_from'), '%B %d, %Y') \
                    if query_params.get('date_from', '') != '' else date.today()
                datetime_to = datetime.strptime(query_params.get('date_to'), '%B %d, %Y') \
                    if query_params.get('date_to', '') != '' else \
                    datetime.strptime(query_params.get('date_from'), '%B %d, %Y')

                start = datetime.combine(datetime_from, time.min)
                start = start.astimezone(pytz.utc)

                end = datetime.combine(datetime_to, time.max)
                end = end.astimezone(pytz.utc)

                queryset = queryset.filter(date_from__gte=start, date_from__lte=end)

            if query_params.get('name', '') != '':
                queryset = queryset.filter(patient__first_name__contains=query_params.get('name'))

        return queryset
