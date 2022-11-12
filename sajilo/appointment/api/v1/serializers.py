import datetime
from rest_framework import serializers, status

from sajilo.appointment.models import Appointment
from sajilo.users.api.v1.serializers import DoctorSerializer, PatientSerializer
from sajilo.users.models import Doctor, Patient


class MakeAppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), required=True, write_only=True
    )
    patient_details = PatientSerializer(source="user", read_only=True)

    doctor = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(), required=True, write_only=True
    )
    doctor_details = DoctorSerializer(source="user", read_only=True)
    date = serializers.DateField()
    time = serializers.TimeField()
    status = serializers.CharField()
    class Meta:
        model = Appointment
        fields = ('patient', 'doctor', 'date', 'time', 'status')

    def validate(self, data):
        if data["appointment_date"] < datetime.date.today():
            raise serializers.ValidationError(
                {
                    "status": "failure",
                    "statusCode": 1,
                    "value_error": "appointment date should be greater than today",
                }
            )

        if data["appointment_time"] < datetime.datetime.now().time():
            raise serializers.ValidationError(
                {
                    "status": "failure",
                    "statusCode": 1,
                    "value_error": "appointment time should be greater than now",
                }
            )

        if data["appointment_date"] == datetime.date.today():
            if data["appointment_time"] < datetime.datetime.now().time():
                raise serializers.ValidationError(
                    {
                        "status": "failure",
                        "statusCode": 1,
                        "value_error": "appointment time should be greater than now",
                    }
                )

        if data["appointment_date"] == datetime.date.today():
            if data["appointment_time"] == datetime.datetime.now().time():
                raise serializers.ValidationError(
                    {
                        "status": "failure",
                        "statusCode": 1,
                        "value_error": "appointment time should be greater than now",
                    }
                )

        if data["appointment_date"] == datetime.date.today():
            if data["appointment_time"] > datetime.datetime.now().time():
                if data["appointment_time"] < datetime.datetime.now().time() + datetime.timedelta(
                    minutes=30
                ):
                    raise serializers.ValidationError(
                        {
                            "status": "failure",
                            "statusCode": 1,
                            "value_error": "appointment time should be greater than 30 minutes",
                        }
                    )

        if data["appointment_date"] == datetime.date.today():
            if data["appointment_time"] > datetime.datetime.now().time():
                if data["appointment_time"] > datetime.datetime.now().time() + datetime.timedelta(
                    minutes=30
                ):
                    if data["appointment_time"] < datetime.datetime.now().time() + datetime.timedelta(
                        minutes=60
                    ):
                        raise serializers.ValidationError(
                            {
                                "status": "failure",
                                "statusCode": 1,
                                "value_error": "appointment time should be greater than 60 minutes",
                            }
                        )

        if data["appointment_date"] == datetime.date.today():
            if data["appointment_time"] > datetime.datetime.now().time():
                if data["appointment_time"]