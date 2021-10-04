from datetime import datetime

from rest_framework import serializers

from app_appointment.models import Patient, Appointment
from app_appointment.utils import save_validated_data


class PatientDefaultSerializer(serializers.ModelSerializer):
    """
    Patient Serializer
    """

    class Meta:
        model = Patient
        fields = '__all__'


class PatientCreateSerializer(serializers.ModelSerializer):
    """
    Patient Serializer
    """

    class Meta:
        model = Patient
        fields = '__all__'


class PatientUpdateSerializer(serializers.ModelSerializer):
    """
    Patient Serializer
    """

    class Meta:
        model = Patient
        fields = ['first_name', 'middle_name', 'last_name']


class AppointmentDefaultSerializer(serializers.ModelSerializer):
    """
    Appointment Serializer
    """

    patient = PatientDefaultSerializer()

    class Meta:
        model = Appointment
        fields = '__all__'


class AppointmentCreateSerializer(serializers.ModelSerializer):
    """
    Appointment Serializer
    """

    first_name = serializers.CharField(default='', write_only=True)
    middle_name = serializers.CharField(default='', write_only=True, allow_blank=True)
    last_name = serializers.CharField(default='', write_only=True)
    comment = serializers.CharField(default='', write_only=True, allow_blank=True)
    date_from = serializers.CharField(default='', write_only=True)
    date_to = serializers.CharField(default='', write_only=True)

    class Meta:
        model = Appointment
        fields = ['first_name', 'middle_name', 'last_name', 'comment', 'date_from', 'date_to']

    def validate(self, attrs):
        errors = dict()

        if attrs.get('first_name') == "" or attrs.get('last_name') == "":
            errors['generic'] = 'Name is Incomplete.'

        if attrs.get('date_from') != "" and attrs.get('date_to') != "":
            datetime_from = datetime.strptime(attrs.get('date_from'), '%B, %d %Y %I:%M%p')
            datetime_to = datetime.strptime(attrs.get('date_to'), '%B, %d %Y %I:%M%p')

            # See if patient already exists
            appointment = Appointment.objects.filter(
                date_from__gte=datetime_from,
                date_to__lte=datetime_to,
            ).first()

            if appointment:
                errors['generic'] = 'No Overbooking!'

        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def save(self, **kwargs):
        data = save_validated_data(self.validated_data.items(), kwargs.items())

        # See if patient already exists
        patient = Patient.objects.filter(
            first_name=data.get('first_name').lower(),
            middle_name=data.get('middle_name').lower(),
            last_name=data.get('last_name').lower(),
        ).first()

        if not patient:
            # Create Patient
            patient = Patient.objects.create(
                first_name=data.get('first_name').lower(),
                middle_name=data.get('middle_name').lower(),
                last_name=data.get('last_name').lower()
            )

        datetime_from = datetime.strptime(data.get('date_from'), '%B, %d %Y %I:%M%p')
        datetime_to = datetime.strptime(data.get('date_to'), '%B, %d %Y %I:%M%p')
        appointment = Appointment.objects.create(
            patient=patient,
            date_from=datetime_from,
            date_to=datetime_to,
            comment=data.get('comment')
        )

        return appointment


class AppointmentUpdateSerializer(serializers.ModelSerializer):
    """
    Appointment Serializer
    """
    first_name = serializers.CharField(default='', write_only=True)
    middle_name = serializers.CharField(default='', write_only=True, allow_blank=True)
    last_name = serializers.CharField(default='', write_only=True)
    date_from = serializers.CharField(default='', write_only=True)
    date_to = serializers.CharField(default='', write_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'

    def validate(self, attrs):
        errors = dict()

        if attrs.get('first_name') == "" or attrs.get('last_name') == "":
            errors['generic'] = 'Name is Incomplete.'

        if attrs.get('date_from') != "" and attrs.get('date_to') != "":
            datetime_from = datetime.strptime(attrs.get('date_from'), '%B, %d %Y %I:%M%p')
            datetime_to = datetime.strptime(attrs.get('date_to'), '%B, %d %Y %I:%M%p')

            # See if patient already exists
            appointment = Appointment.objects.filter(
                date_from__gte=datetime_from,
                date_to__lte=datetime_to,
            ).first()

            if appointment:
                errors['generic'] = 'No Overbooking!'

        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def save(self, **kwargs):
        data = save_validated_data(self.validated_data.items(), kwargs.items())
        appointment = self.instance

        appointment.patient.first_name = data.get('first_name')
        appointment.patient.middle_name = data.get('middle_name')
        appointment.patient.last_name = data.get('last_name')
        appointment.patient.save()

        datetime_from = datetime.strptime(data.get('date_from'), '%B, %d %Y %I:%M%p')
        datetime_to = datetime.strptime(data.get('date_to'), '%B, %d %Y %I:%M%p')

        appointment.date_from = datetime_from
        appointment.date_to = datetime_to
        appointment.comment = data.get('comment')
        appointment.save()

        return appointment
