from django.urls import path
from rest_framework.routers import DefaultRouter
from sajilo.users.api.v1 import views

from sajilo.users.api.v1.views import (
    PatientUserList,
    UserRegistrationView, 
    DoctorLoginView,
    DoctorUserList,
    PatientLoginView,
    UserDataList,
    CreateRoleView,
    ListRoleView,
    UpdateRoleView,
    DestroyRoleView,
)

app_name = "users_api_v1"


urlpatterns = [
    path("registration/", UserRegistrationView.as_view(), name="registration"),
    path("doctor/login/", DoctorLoginView.as_view(), name="doctor_login"),
    path("patient/login/", PatientLoginView.as_view(), name="patient_login"),
    path("list/", UserDataList.as_view(), name="list-user"),
    path("doctor/list/", DoctorUserList.as_view(), name="doctor-list"),
    path("patient/list/", PatientUserList.as_view(), name="patient-list"),
    path(
        "request-role/create/",
        CreateRoleView.as_view(),
        name="create_request-role",
    ),
    path(
        "request-role/list/",
        ListRoleView.as_view(),
        name="list_request-role",
    ),
    path(
        "request-role/update/<int:pk>/",
        UpdateRoleView.as_view(),
        name="update_request-role",
    ),
    path(
        "request-role/delete/<int:pk>/",
        DestroyRoleView.as_view(),
        name="delete_request-role",
    )
]
