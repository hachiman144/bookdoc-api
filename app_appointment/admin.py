from django.contrib import admin

# Register your models here.
from app_appointment.models import Patient, Appointment


class PatientsAdmin(admin.ModelAdmin):
    """
    Patients Admin
    """
    search_fields = ('first_name', 'last_name')
    list_display = ('first_name', 'middle_name', 'last_name')


class AppointmentsAdmin(admin.ModelAdmin):
    """
    Appointments Admin
    """
    search_fields = ('patient__first_name', 'patient__last_name')
    list_display = ('patient', 'date_from', 'date_to', 'comment')


admin.site.register(Patient, PatientsAdmin)
admin.site.register(Appointment, AppointmentsAdmin)
