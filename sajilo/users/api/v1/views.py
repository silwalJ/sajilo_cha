import json

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
)
from sajilo.core.pagination import CustomPagination
from django.contrib.auth import get_user_model


from sajilo.users.api.v1.serializers import (
    DoctorSerializer,
    PatientSerializer,
    RoleSerializer,
    UserRegistrationSerializer,
    DoctorLoginSerializer,
    PatientLoginSerializer,
    UserSerializer,
)
from sajilo.users.models import USER_TYPE, Doctor, Patient, Role, User

class UserRegistrationView(CreateAPIView):

    serializer_class = UserRegistrationSerializer
    permission_classes = ()

    @extend_schema(
        operation_id="User Registration API",
        description="Creates user with given username and password.",
        request=UserRegistrationSerializer,
    )
    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            print(headers)
            return Response(
                {
                    "status": "success",
                    "detail": ("User Created Successfully!."),
                    "data": serializer.data,
                },
                status.HTTP_201_CREATED,
                headers=headers,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorLoginView(APIView):
    permission_classes = ()
    serializer_class = DoctorLoginSerializer

    @extend_schema(
        operation_id="User Login API",
        description="Login user with email and password and returns refresh and access token",
        request=DoctorLoginSerializer,
        responses={
            status.HTTP_200_OK: inline_serializer(
                "User login successful",
                fields={
                    "detail": serializers.CharField(
                        default="User login successfully done"
                    )
                },
            ),
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                "user_login_unsuccessful",
                fields={
                    "email": serializers.CharField(default="User login unsuccessful.")
                },
            ),
        },
    )
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            
            return Response(
                {
                    "status": "Success",
                    "statusCode": status.HTTP_200_OK,
                    "data": serializer.validated_data,
                    "message": "Login Successful",
                }
            )

        else:
            return Response(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "data": serializer.data,
                    "message": "something went wrong",
                },
            )


class PatientLoginView(APIView):
    permission_classes = ()
    serializer_class = PatientLoginSerializer

    @extend_schema(
        operation_id="User Login API",
        description="Login user with email and password and returns refresh and access token",
        request=PatientLoginSerializer,
        responses={
            status.HTTP_200_OK: inline_serializer(
                "User login successful",
                fields={
                    "detail": serializers.CharField(
                        default="User login successfully done"
                    )
                },
            ),
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                "user_login_unsuccessful",
                fields={
                    "email": serializers.CharField(default="User login unsuccessful.")
                },
            ),
        },
    )
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():

            return Response(
                {
                    "status": "Success",
                    "statusCode": status.HTTP_200_OK,
                    "data": serializer.validated_data,
                    "message": "Login Successful",
                    "user_type": request.data["user_type"],
                }
            )

        else:
            return Response(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "data": serializer.data,
                    "message": "something went wrong",
                },
            )

User = get_user_model()
@extend_schema(
    operation_id="List all user master data",
    description="List all user master data",
    request=UserSerializer,
)
class UserDataList(APIView):
    permission_classes = ()
    serializer_class = UserSerializer

    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

@extend_schema(
    operation_id="List patient user master data",
    description="List patient user master data",
    request=PatientSerializer,
)
class PatientUserList(APIView):
    permission_classes = ()
    serializer_class = PatientSerializer

    def get(self, request):
        patient = Patient.objects.all()
        serializer = PatientSerializer(patient, many=True)
        return Response(serializer.data)

@extend_schema(
    operation_id="List doctor user master data",
    description="List doctor user master data",
    request=DoctorSerializer,
)
class DoctorUserList(APIView):
    permission_classes = ()
    serializer_class = DoctorSerializer

    def get(self, request):
        doctor = Doctor.objects.all()
        serializer = DoctorSerializer(doctor, many=True)
        return Response(serializer.data)

@extend_schema(
    operation_id="Update request attendance",
    description="Update request attendance",
    request=RoleSerializer,
)
class UpdateRoleView(UpdateAPIView):
    """
    This is a Role Update View.
    """

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    http_method_names = ["patch"]

    def partial_update(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        serializer = self.serializer_class(role, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.update(role, serializer.validated_data)
            return Response(
                {
                    "status": "success",
                    "statusCode": status.HTTP_200_OK,
                    "message": "Missed Role Updated Successfully",
                    "data": serializer.data,
                }
            )


@extend_schema(
    operation_id="Role View API for Thumb",
    description="For view the Role",
    request=RoleSerializer,
)
class ListRoleView(ListAPIView):
    """
    This is a view to list all the attendance done.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    pagination_class = CustomPagination

    def list(self, request):
        queryset = super().list(self, ListRoleView)
        return Response(
            {
                "status": "Success",
                "statusCode": status.HTTP_200_OK,
                "data": queryset.data,
                "message": "Role List",
            }
        )


@extend_schema(
    operation_id="Create Role API",
    description=" For attendance create with check_in and check_out time.",
    request=RoleSerializer,
)
class CreateRoleView(CreateAPIView):
    """
    This is to create the attendance.
    """

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
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
                "message": "Role Created Successfully",
                "data": serializer.data,
            }
        )


@extend_schema(
    operation_id="Role Delete API",
    description="For delete the Role",
    request=RoleSerializer,
)
class DestroyRoleView(DestroyAPIView):
    """
    This is to delete the attendance View.
    """

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    # permission_classes = [AdminOnly]

    def destroy(self, request, pk):
        attend = get_object_or_404(Role, pk=pk)
        attend.delete()
        return Response(
            {
                "status": "success",
                "statusCode": status.HTTP_204_NO_CONTENT,
                "message": f"Role of {attend.user} Successfully Deleted",
            }
        )
