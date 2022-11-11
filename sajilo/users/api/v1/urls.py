from django.urls import path

from sajilo.users.api.v1.views import (
    UserRegistrationView, 
    DoctorLoginView,
    PatientLoginView,
)

app_name = "users_api_v1"

urlpatterns = [
    path("registration/", UserRegistrationView.as_view(), name="registration"),
    path("doctor/login/", DoctorLoginView.as_view(), name="doctor_login"),
    path("patient/login/", PatientLoginView.as_view(), name="patient_login"),
]
