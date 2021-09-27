from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from app_appointment.filter import AppointmentFilter
from app_appointment.models import Appointment
from app_appointment.serializers import AppointmentDefaultSerializer, AppointmentCreateSerializer, \
    AppointmentUpdateSerializer
from app_appointment.utils import get_boolean_value


class AppointmentView(viewsets.ModelViewSet):
    """
    Appointment View
    """

    http_method_names = ['post', 'get', 'patch', 'delete']
    # permission_classes = (AllowAnyOnGetMethod,)
    filter_backends = (AppointmentFilter,)
    queryset = Appointment.objects.all()

    serializer_class = AppointmentDefaultSerializer
    action_serializers = {
        'list': AppointmentDefaultSerializer,
        'create': AppointmentCreateSerializer,
        'partial_update': AppointmentUpdateSerializer
    }

    def get_serializer_class(self):
        """
        Retrieve the appropriate serializer for every request method
        """
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]

        return super(AppointmentView, self).get_serializer_class()

    def list(self, request, *args, **kwargs):
        """
        List Appointments
        """
        queryset = self.filter_queryset(self.get_queryset())

        if get_boolean_value(request.GET.get('paginate', 'true')):
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create an Appointment
        - REQUIRED
        - NOTE
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            try:
                instance = serializer.save()
                return Response({
                    'message': 'Appointment Successfully Set.',
                    'data': AppointmentDefaultSerializer(instance).data
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    'message': e
                }, status.HTTP_400_BAD_REQUEST)
        return Response({
            'message': 'Invalid data.',
            'error': serializer.errors
        }, status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
        Update a Appointment details
        - REQUIRED
        - NOTE
        """
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)

        if serializer.is_valid():
            instance = serializer.save()
            return Response({
                'message': 'Appointment details is updated successfully.',
                'data': AppointmentDefaultSerializer(instance).data
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Invalid data.',
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
