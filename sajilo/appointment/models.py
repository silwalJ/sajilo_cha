from django.db import models

from sajilo.core.models import TimeStampAbstractModel
from sajilo.users.models import Doctor, Patient

APPOINTMENT_STATUS = [
    ("1", "Appointed"),
    ("2", "Ongoing"),
    ("3", "Completed")
]

class Hospital(TimeStampAbstractModel):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    website = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Clinic(TimeStampAbstractModel):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    website = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Pharmacy(TimeStampAbstractModel):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    website = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Appointment(TimeStampAbstractModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=1, choices=APPOINTMENT_STATUS, default='1')

    class Meta:
        db_table = 'appointment'
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'

    def __str__(self):
        return f'{self.patient} - {self.doctor}'

    def get_absolute_url(self):
        return reverse('appointment:appointment-detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('appointment:appointment-update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('appointment:appointment-delete', kwargs={'pk': self.pk})

    def get_list_url(self):
        return reverse('appointment:appointment-list')

    def get_create_url(self):
        return reverse('appointment:appointment-create')

    def get_status(self):
        return dict(APPOINTMENT_STATUS)[self.status]

    def get_doctor_name(self):
        return self.doctor.user.get_full_name()

    def get_patient_name(self):
        return self.patient.user.get_full_name()

    def get_patient_email(self):
        return self.patient.user.email

    def get_doctor_email(self):
        return self.doctor.user.email

    def get_patient_phone(self):
        return self.patient.user.phone

    def get_doctor_phone(self):
        return self.doctor.user.phone

    def get_patient_address(self):
        return self.patient.user.address

    def get_doctor_address(self):
        return self.doctor.user.address
