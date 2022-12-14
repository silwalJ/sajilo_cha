from sajilo.users.models import (
    USER_TYPE,
    CustomPermission, 
    Doctor, 
    DoctorTrainingHistory, 
    DoctorWorkExperience, 
    Education, 
    Patient, 
    Role
)
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers, status
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """
    user_id = serializers.CharField(source="id", read_only=True)

    class Meta:
        model = User
        fields = ("user_id", "email", "status", "user_type")


class CustomPermissionSerializers(serializers.Serializer):
    """
    Used for create, update, delete and list the permission
    """

    id = serializers.IntegerField(read_only=True, help_text="id serializer help text")
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=200)
    key = serializers.SlugField(read_only=True)

    class Meta:
        model = CustomPermission
        fields = ["id", "name", "description", "key"]

        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def create(self, validated_data):
        errors = {}
        if CustomPermission.objects.filter(name=validated_data["name"]).exists():
            errors["name"] = "Already exit permission"

        if errors:
            raise serializers.ValidationError(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errors": errors,
                }
            )
        permission = CustomPermission.objects.create(**validated_data)

        return permission

    def update(self, instance, validated_data):
        errors = {}
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        if errors:
            raise serializers.ValidationError(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errors": errors,
                }
            )
        instance.save()
        return instance


class RoleSerializer(serializers.Serializer):
    """
    Used for create, update, delete and list the role.
    Permission must be choose from existed permission in system.
    """

    id = serializers.IntegerField(read_only=True, help_text="id serializer help text")
    name = serializers.CharField(max_length=100)
    desc = serializers.CharField(max_length=200)
    permission_to_role = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(
            queryset=CustomPermission.objects.all(), write_only=True
        ),
        write_only=True,
    )
    permission = CustomPermissionSerializers(
        source="permission_to_role", read_only=True, many=True
    )

    class Meta:
        model = Role
        fields = ["id", "name", "desc", "permission_to_role", "permission", "user"]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def create(self, validated_data):
        errors = {}
        if Role.objects.filter(name=validated_data["name"]).exists():
            errors["name"] = "Role already exists."

        permission = validated_data.pop("permission_to_role")
        if errors:
            raise serializers.ValidationError(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errors": errors,
                }
            )
        role = Role.objects.create(**validated_data)

        role.permission_to_role.set(permission)

        return role

    def update(self, instance, validated_data):
        errors = {}
        permission = validated_data.pop("permission_to_role")
        instance.name = validated_data.get("name", instance.name)
        instance.desc = validated_data.get("desc", instance.desc)
        if errors:
            raise serializers.ValidationError(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errors": errors,
                }
            )
        instance.save()
        instance.permission_to_role.clear()
        instance.permission_to_role.set(permission)

        return instance

class PatientSerializer(serializers.ModelSerializer):
    """
    Patient Serializer
    """
    patient_id = serializers.IntegerField(source="id", read_only=True)
    first_name = serializers.CharField()
    middle_name = serializers.CharField(allow_blank=True, allow_null=True)
    last_name = serializers.CharField()
    bio = serializers.CharField()
    mobile_number = serializers.IntegerField()
    dob = serializers.DateField()
    religion = serializers.CharField()
    blood_group = serializers.CharField()
    gender = serializers.IntegerField()
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True, write_only=True
    )
    user_details = UserSerializer(source="user", read_only=True)
    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), required=True, write_only=True
    )
    role_details = RoleSerializer(source="role", read_only=True)
    class Meta:
        model = Patient
        fields = [
            "patient_id",
            "first_name",
            "middle_name",
            "last_name",
            "mobile_number",
            "bio",
            "dob",
            "religion",
            "gender",
            "blood_group",
            'user',
            'user_details',
            'role',
            'role_details'
        ]

class DoctorSerializer(serializers.ModelSerializer):
    """
    Doctor Serializer
    """
    doctor_id = serializers.IntegerField(source="id", read_only=True)
    first_name = serializers.CharField()
    middle_name = serializers.CharField(allow_blank=True, allow_null=True)
    last_name = serializers.CharField()
    mobile_number = serializers.IntegerField()
    dob = serializers.DateField()
    license_no = serializers.CharField()
    gender = serializers.IntegerField()
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True, write_only=True
    )
    user_details = UserSerializer(source="user", read_only=True)
    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), required=True, write_only=True
    )
    role_details = RoleSerializer(source="role", read_only=True)
    class Meta:
        model = Doctor
        fields = [
            "doctor_id",
            "first_name",
            "middle_name",
            "last_name",
            "mobile_number",
            "dob",
            "license_no",
            "gender",
            'user',
            'user_details',
            'role',
            'role_details'
        ]

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
   registration serializer for user
    """

    user_id = serializers.IntegerField(source="id", read_only=True)
    user_type = serializers.CharField(read_only=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField()
    middle_name = serializers.CharField(allow_blank=True, allow_null=True)
    last_name = serializers.CharField()
    mobile_number = serializers.IntegerField()
    dob = serializers.DateField()
    license_no = serializers.CharField()
    gender = serializers.IntegerField()

    class Meta:
        model = User
        fields = [
            "user_id",
            "email",
            "password",
            "confirm_password",
            "first_name",
            "middle_name",
            "last_name",
            "mobile_number",
            "dob",
            "license_no",
            "gender",
            'user_type',
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validate_data):
        errors = {}
        confirm_password = self._kwargs["data"].pop("confirm_password")
        password = self._kwargs["data"].pop("password")
        
        first_name = self._kwargs["data"].pop("first_name")
        middle_name = self._kwargs["data"].pop("middle_name")
        dob = self._kwargs["data"].pop("dob")
        gender = self._kwargs["data"].pop("gender")
        last_name = self._kwargs["data"].pop("last_name")
        mobile_number = self._kwargs["data"].pop("mobile_number")
        license_no = self._kwargs["data"].pop_or_none("license_no")
        user_type = self._kwargs["data"].pop("user_type")

        if user_type == USER_TYPE["1"] :
            user = User.objects.create(
                email=self._kwargs["data"].pop("email"),
                user_type=USER_TYPE["PATIENT"],
            )
            user.set_password(password)
            user.save()

            Patient.objects.create(
                user=user,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                mobile_number=mobile_number,
                license_no=license_no,
                dob=dob,
                gender=gender,
            )
        else :
            user = User.objects.create(
                email=self._kwargs["data"].pop("email"),
                user_type=USER_TYPE["DOCTOR"],
            )
            user.set_password(password)
            user.save()

            Doctor.objects.create(
                user=user,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                mobile_number=mobile_number,
                dob=dob,
                gender=gender,
            )

        if errors:
            raise serializers.ValidationError(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errors": errors,
                }
            )

        return validate_data

    def validate(self, data):
        errors = {}
        email = data["email"]
        mobile_number = data.get("mobile_number")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if User.objects.filter(email=email).exists():
            errors["email"] = "This email has already been registered."

        # if User.objects.filter(mobile_number=mobile_number).exists():
        #     errors["mobile_number"] = "Account with this phone number already exists!"

        if password != confirm_password:
            errors["password"] = "Password didn't match."

        if errors:
            raise serializers.ValidationError(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errors": errors,
                }
            )
        return data

class DoctorTrainingHistorySerializer(serializers.Serializer):
    """
    Doctor Training History Serializer
    """
    training_id = serializers.CharField(source="id", read_only=True)
    name = serializers.CharField()
    from_date = serializers.DateField()
    to_date = serializers.DateField()
    place_type = serializers.CharField()
    place = serializers.CharField()
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True, write_only=True
    )
    user_details = UserSerializer(source="user", read_only=True)

    class Meta:
        model = DoctorTrainingHistory
        fields = (
            "training_id",
            "name",
            "from_date",
            "to_date",
            "place_type",
            "place",
            "user"
        )

class DoctorRegistrationSerializer(serializers.ModelSerializer):
    """
   registration serializer for patient
    """

    registration_id = serializers.IntegerField(source="id", read_only=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField()
    middle_name = serializers.CharField(allow_blank=True, allow_null=True)
    last_name = serializers.CharField()
    mobile_number = serializers.IntegerField()
    dob = serializers.DateField()
    license_no = serializers.CharField()
    gender = serializers.IntegerField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "confirm_password",
            "first_name",
            "middle_name",
            "last_name",
            "mobile_number",
            "dob",
            "gender"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validate_data):
        errors = {}
        password = self._kwargs["data"].pop("password")

        self._kwargs["data"].pop("confirm_password")

        first_name = self._kwargs["data"].pop("first_name")
        middle_name = self._kwargs["data"].pop("middle_name")
        dob = self._kwargs["data"].pop("dob")
        gender = self._kwargs["data"].pop("gender")
        last_name = self._kwargs["data"].pop("last_name")
        mobile_number = self._kwargs["data"].pop("mobile_number")

        user = User.objects.create(
            email=self._kwargs["data"].pop("email"),
            user_type=USER_TYPE["PATIENT"],
        )

        if errors:
            raise serializers.ValidationError(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errors": errors,
                }
            )

        user.set_password(password)
        user.save()

        Patient.objects.create(
            user=user,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            mobile_number=mobile_number,
            dob=dob,
            gender=gender,
        )
        return validate_data

    def validate(self, data):
        errors = {}
        email = data["email"]
        mobile_number = data["mobile_number"]
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if User.objects.filter(email=email).exists():
            errors["email"] = "This email has already been registered."

        if Patient.objects.filter(mobile_number=mobile_number).exists():
            errors["phone_number"] = "Account with this phone number already exists!"

        if password != confirm_password:
            errors["password"] = "Password didn't match."

        if errors:
            raise serializers.ValidationError(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errors": errors,
                }
            )
        return data

class DoctorTrainingHistorySerializer(serializers.Serializer):
    """
    Doctor Training History Serializer
    """
    training_id = serializers.CharField(source="id", read_only=True)
    name = serializers.CharField()
    from_date = serializers.DateField()
    to_date = serializers.DateField()
    place_type = serializers.CharField()
    place = serializers.CharField()
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True, write_only=True
    )
    user_details = UserSerializer(source="user", read_only=True)

    class Meta:
        model = DoctorTrainingHistory
        fields = (
            "training_id",
            "name",
            "from_date",
            "to_date",
            "place_type",
            "place",
            "user"
        )

class DoctorWorkExperienceSerializer(serializers.Serializer):
    work_id = serializers.CharField(source="id", read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True, write_only=True
    )
    user_details = UserSerializer(source="user", read_only=True)
    from_date = serializers.DateField()
    to_date = serializers.DateField()
    organization = serializers.CharField()
    designation = serializers.CharField()
    department = serializers.CharField()
    level = serializers.CharField()
    is_first_service = serializers.BooleanField()
    is_current_service = serializers.BooleanField()

    class Meta:
        model = DoctorWorkExperience
        fields = (
            "work_id",
            "user",
            "from_date",
            "to_date",
            "organization",
            "designation",
            "department",
            "level",
            "is_first_service",
            "is_current_service",
        )

class Education(serializers.Serializer):
    education_id = serializers.CharField(source="id", read_only=True)
    degree = serializers.CharField()
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True, write_only=True
    )
    user_details = UserSerializer(source="user", read_only=True)
    institution = serializers.CharField()
    percentage = serializers.FloatField()
    passed_year = serializers.DateField()
    level = serializers.CharField()
    educational_file = serializers.FileField()

    class Meta:
        model = Education
        fields = (
            "education_id",
            "degree",
            "user",
            "institution",
            "percentage",
            "level",
            "educational_file"
        )


class DoctorRegistrationSerializer(serializers.ModelSerializer):
    """
    Trainee Serializer
    """

    doctor_id = serializers.CharField(source="id", read_only=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    middle_name = serializers.CharField()
    last_name = serializers.CharField(required=True)
    mobile_number = serializers.CharField()
    license_no = serializers.CharField(required=True)
    dob = serializers.DateField()
    gender = serializers.CharField(required=True)
    address = serializers.CharField()

    class Meta:
        model = Doctor
        fields = (
            "doctor_id",
            "first_name",
            "middle_name",
            "last_name",
            "mobile_number",
            "license_no",
            "dob",
            "gender",
            "address",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validate_data):
        errors = {}
        password = self._kwargs["data"].pop("password")

        confirm_password = self._kwargs["data"].pop("confirm_password")

        first_name = self._kwargs["data"].pop("first_name")
        middle_name = self._kwargs["data"].pop("middle_name")
        dob = self._kwargs["data"].pop("dob")
        gender = self._kwargs["data"].pop("gender")
        last_name = self._kwargs["data"].pop("last_name")
        mobile_number = self._kwargs["data"].pop("mobile_number")
        license_no = self._kwargs["data"].pop("license_no")
        address = self._kwargs["data"].pop("address")

        user = User.objects.create(
            email=self._kwargs["data"].pop("email"),
            user_type=USER_TYPE["DOCTOR"],
        )

        if errors:
            raise serializers.ValidationError(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errors": errors,
                }
            )

        user.set_password(password)
        user.save()

        Patient.objects.create(
            user=user,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            mobile_number=mobile_number,
            dob=dob,
            gender=gender,
            license_no = license_no,
            address = address,
        )
        return validate_data

    def validate(self, data):
        errors = {}
        email = data["email"]
        mobile_number = data["mobile_number"]
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if User.objects.filter(email=email).exists():
            errors["email"] = "This email has already been registered."

        if Patient.objects.filter(mobile_number=mobile_number).exists():
            errors["phone_number"] = "Account with this phone number already exists!"

        if password != confirm_password:
            errors["password"] = "Password didn't match."

        if errors:
            raise serializers.ValidationError(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errors": errors,
                }
            )
        return data


class DoctorLoginSerializer(TokenObtainPairSerializer, serializers.ModelSerializer):
    """
    Used for user login.
    """

    email = serializers.EmailField()
    password = serializers.CharField()
    user_type = serializers.CharField()

    class Meta:
        model = User
        fields = ["email", "password", "user_type"]
        extra_kwargs = {"password": {"write_only": True}}

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        role = None
        try:
            doctor = Doctor.objects.get(user=user)
            role = doctor.user__user_type

        except Exception as e:
            print(e)
        token["user_type"] = role

        return token

    def validate(self, attrs):
        errors = {}
        email = attrs.get("email")
        password = attrs.get("password")
        user_type = attrs.get("user_type")

        user = authenticate(email=email, password=password)
        # email exist
        if not user:
            if User.objects.filter(email=email).exists():
                errors["email"] = "Invalid Credential"

        # Login Panel Verification
        elif not (user_type in ["1", "2"]):
            errors["invalid_link"] = "Please use valid user type"

        elif user_type == "2" and user.user_type != user_type:
            errors[
                "invalid_link"
            ] = "Please use your login panel, you are not doctor user"

        # elif user_type == "1" and not User.objects.filter(user=user).exists():
        #     errors[
        #         "invalid_link"
        #     ] = "Please register first"

        elif not user.is_superuser:
            if not user.status == "1":
                errors["email"] = "Email not verified"

        if errors:
            raise serializers.ValidationError(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errors": errors,
                }
            )
        user.save()

        refresh = self.get_token(user)

        response = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return response

class PatientLoginSerializer(TokenObtainPairSerializer, serializers.ModelSerializer):
    """
    Used for user login.
    """

    email = serializers.EmailField()
    password = serializers.CharField()
    user_type = serializers.CharField()

    class Meta:
        model = User
        fields = ["email", "password", "user_type"]
        extra_kwargs = {"password": {"write_only": True}}

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        role = None
        try:
            patient = Patient.objects.get(user=user)
            role = patient.user__user_type

        except Exception as e:
            print(e)
        token["user_type"] = role

        return token

    def validate(self, attrs):
        errors = {}
        email = attrs.get("email")
        password = attrs.get("password")
        user_type = attrs.get("user_type")

        user = authenticate(email=email, password=password)
        if user:
            user_type = user.user_type


        # email exist
        if not user:
            if User.objects.filter(email=email).exists():
                errors["email"] = "Invalid Credentials"

        # Login Panel Verification
        elif not (user_type in ["1", "2"]):
            errors["invalid_link"] = "Please use valid user type"

        elif user_type == "1" and user.user_type != user_type:
            errors[
                "invalid_link"
            ] = "Please use your login panel, you are not patient user"

        # elif user_type == "1" and not User.objects.filter(user=user).exists():
        #     errors[
        #         "invalid_link"
        #     ] = "Please register first"
       
        elif not user.is_superuser:
            if not user.status == "2":
                errors["email"] = "Email not verified"

        refresh = self.get_token(user)

        response = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        if errors:
            raise serializers.ValidationError(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errors": errors,
                }
            )
        return response
