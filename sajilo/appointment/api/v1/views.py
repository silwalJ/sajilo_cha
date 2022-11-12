from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from sajilo.core.pagination import CustomPagination
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from sajilo.appointment.api.v1.serializers import (
    MakeAppointmentSerializer,
)
from sajilo.appointment.models import Appointment


@extend_schema(
    operation_id="Update request attendance",
    description="Update request attendance",
    request=MakeAppointmentSerializer,
)
class UpdateAppointmentView(UpdateAPIView):
    """
    This is a Appointment Update View.
    """

    queryset = Appointment.objects.all()
    serializer_class = MakeAppointmentSerializer
    http_method_names = ["patch"]

    def partial_update(self, request, pk):
        attendance = get_object_or_404(Appointment, pk=pk)
        serializer = self.serializer_class(attendance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.update(attendance, serializer.validated_data)
            return Response(
                {
                    "status": "success",
                    "statusCode": status.HTTP_200_OK,
                    "message": "Missed Appointment Updated Successfully",
                    "data": serializer.data,
                }
            )


@extend_schema(
    operation_id="Appointment View API for Thumb",
    description="For view the Appointment",
    request=MakeAppointmentSerializer,
)
class ListAppointmentView(ListAPIView):
    """
    This is a view to list all the attendance done.
    """

    queryset = Appointment.objects.exclude(source="web")
    serializer_class = MakeAppointmentSerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        kwargs["module"] = "Appointment"
        serializer = super().list(self, ListAppointmentView)
        return Response(
            {
                "Status": "success",
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data,
            },
        )


@extend_schema(
    operation_id="Create Appointment API",
    description=" For attendance create with check_in and check_out time.",
    request=MakeAppointmentSerializer,
)
class CreateAppointmentView(CreateAPIView):
    """
    This is to create the attendance.
    """

    queryset = Appointment.objects.all()
    serializer_class = MakeAppointmentSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            many=isinstance(request.data, list),
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "status": "success",
                "statusCode": status.HTTP_201_CREATED,
                "message": "Appointment Created Successfully",
                "data": serializer.data,
            }
        )


@extend_schema(
    operation_id="Appointment Delete API",
    description="For delete the Appointment",
    request=MakeAppointmentSerializer,
)
class DestroyAppointmentView(DestroyAPIView):
    """
    This is to delete the attendance View.
    """

    queryset = Appointment.objects.all()
    serializer_class = MakeAppointmentSerializer
    # permission_classes = [AdminOnly]

    def destroy(self, request, pk):
        attend = get_object_or_404(Appointment, pk=pk)
        attend.delete()
        return Response(
            {
                "status": "success",
                "statusCode": status.HTTP_204_NO_CONTENT,
                "message": f"Appointment of {attend.user} Successfully Deleted",
            }
        )

