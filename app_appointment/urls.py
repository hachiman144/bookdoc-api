"""
Student App Urls
"""
from django.urls import path, include
from rest_framework import routers

from app_appointment.views import AppointmentView

appointment_router = routers.DefaultRouter()
appointment_router.register('appointment', AppointmentView)

urlpatterns = [
    path('', include(appointment_router.urls))
]
