from django.urls import path
from rest_framework.routers import DefaultRouter

from sajilo.appointment.api.v1.views import (
    UpdateAppointmentView,
    ListAppointmentView,
    CreateAppointmentView,
    DestroyAppointmentView,
)

app_name = "appointment_api_v1"

router = DefaultRouter()


urlpatterns = [
    path(
        "request-attendance/create/",
        CreateAppointmentView.as_view(),
        name="create_request-attendance",
    ),
    path(
        "request-attendance/list/",
        ListAppointmentView.as_view(),
        name="list_request-attendance",
    ),
    path(
        "request-attendance/update/<int:pk>/",
        UpdateAppointmentView.as_view(),
        name="update_request-attendance",
    ),
    path(
        "request-attendance/delete/<int:pk>/",
        DestroyAppointmentView.as_view(),
        name="delete_request-attendance",
    ),
]

urlpatterns += router.urls
