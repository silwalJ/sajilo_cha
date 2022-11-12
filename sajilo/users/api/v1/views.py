import json

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from sajilo.core.pagination import CustomPagination


from sajilo.users.api.v1.serializers import (
    UserRegistrationSerializer,
    DoctorLoginSerializer,
    PatientLoginSerializer,
    UserSerializer,
)
from sajilo.users.models import Role, User

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

@extend_schema(
    operation_id="List all user master data",
    description="List all user master data",
    request=UserSerializer,
)
class UserDataList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination