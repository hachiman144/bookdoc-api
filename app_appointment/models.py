from django.db import models

# Create your models here.
from django.utils import timezone


class Patient(models.Model):
    """
    Patient Model
    """
    objects = models.Manager()

    first_name = models.CharField(max_length=100, default='', blank=True)
    middle_name = models.CharField(max_length=100, default='', blank=True)
    last_name = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return '%s %s' % (self.first_name.upper(), self.last_name.upper())


class Appointment(models.Model):
    """
    Booking Appointments Model
    """
    objects = models.Manager()

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, default='')
    date_from = models.DateTimeField(default=timezone.now)
    date_to = models.DateTimeField(default=timezone.now)
    comment = models.TextField(default='', blank=True, null=True)
