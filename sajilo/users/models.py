from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .helper import generate_key
from .managers import CustomUserManager
from sajilo.users.utils import generate_code
from sajilo.core.models import TimeStampAbstractModel

USER_TYPE = [("1", "doctor"), ("2", "patient"), ("3", "super_user")]

GENDER = (
    ("1", "Male"),
    ("2", "Female"),
    ("3", "Others"),
)

BLOOD_GROUP = [
    ("A+", "A+"),
    ("A-", "A-"),
    ("B+", "B+"),
    ("B-", "B-"),
    ("O+", "O+"),
    ("O-", "O-"),
    ("AB+", "AB+"),
    ("AB-", "AB-"),
]

class User(AbstractUser, TimeStampAbstractModel):
    """Default user for tlms."""

    email = models.EmailField(_("Email Address"), unique=True, null=True, blank=True)

    username = None  # type: ignore
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    middle_name = None
    extra_fields = dict
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    user_type = models.CharField(max_length=1, choices=USER_TYPE, null=True)
    objects = CustomUserManager()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.email



"""Creating custom permission for Role"""


class CustomPermission(TimeStampAbstractModel):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    key = models.SlugField(max_length=120, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.key = generate_key(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.key


"""For defining role of the user | For user type Admin """


class Role(TimeStampAbstractModel):
    name = models.CharField(max_length=50, unique=True)
    desc = models.TextField(_("Descriptions of Role"), blank=True, null=True)
    permission_to_role = models.ManyToManyField(CustomPermission, related_name="role")

    def __str__(self):
        return self.name


"""For staff users"""
class UserDocument(models.Model): 
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    document_name = models.CharField(max_length=100, null=True, blank=True)
    document = models.FileField(upload_to="documents/", null=True, blank=True)

    class Meta:
        verbose_name = "User Document"
        verbose_name_plural = "User Document"

    def __str__(self):
        return f"{self.document_name}"

class Medicalhistory(models.Model):
    medical_history = models.TextField(null=True, blank=True)
    allergies = models.TextField(null=True, blank=True)
    reports = models.ForeignKey(
        UserDocument, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.medical_history

    class Meta:
        verbose_name = "Medical History"
        verbose_name_plural = "Medical History"


class Patient(models.Model):

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=20)
    user = models.OneToOneField(
        User, 
        blank=True, 
        on_delete=models.CASCADE
    )
    bio = models.TextField(null=True, blank=True)
    medical_history = models.ForeignKey(
        Medicalhistory, on_delete=models.SET_NULL, null=True, blank=True
    )
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, blank=True
    )
    dob_AD = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER, null=True, blank=True)
    religion = models.CharField(max_length=255, null=True, blank=True)
    blood_group = models.CharField(
        max_length=5, choices=BLOOD_GROUP, null=True, blank=True
    )
    free_trail = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.first_name}  {self.last_name}"

    def get_user_mail(self):
        return self.user.email

    @property
    def get_full_name(self):
        full_name = " ".join(
            [self.first_name or "", self.middle_name or "", self.last_name or ""]
        )

        return " ".join(full_name.split())

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patient"


# For doctor user
LOCATION_TYPE = [
    ("1", "Nepal"),
    ("2", "Foreign Country"),
]
class DoctorTrainingHistory(TimeStampAbstractModel):
    name = models.CharField(max_length=255)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    location_type = models.CharField(max_length=1, choices=LOCATION_TYPE, default="1")
    location = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )


class DoctorWorkExperience(TimeStampAbstractModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True
    )
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)
    designation = models.CharField(max_length=255, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    level = models.CharField(max_length=100, null=True, blank=True)
    is_first_service = models.BooleanField(default=False)
    is_current_service = models.BooleanField(default=False)


class Education(models.Model):
    degree = models.CharField(max_length=255)
    institution_name = models.CharField(max_length=400, null=True, blank=True)
    percentage = models.FloatField(null=True)
    passed_year = models.DateField(null=True, blank=True)
    level = models.CharField(max_length=100, null=True)
    educational_file = models.FileField(
        upload_to="educational_files/", null=True, blank=True
    )

class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    license_no = models.CharField(max_length=100)
    dob = models.DateField(blank=True, null=True, verbose_name="Date of Birth")
    gender = models.CharField(max_length=20, choices=GENDER)
    address = models.CharField(max_length=20, null=True, blank=True)
    training = models.ForeignKey(
        DoctorTrainingHistory, on_delete=models.SET_NULL, null=True, blank=True
    )
    work_experience = models.ForeignKey(
        DoctorWorkExperience, on_delete=models.SET_NULL, null=True, blank=True
    )
    education = models.ForeignKey(
        Education, on_delete=models.SET_NULL, null=True, blank=True
    )
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.first_name}  {self.last_name}"

    @property
    def get_full_name(self):
        full_name = " ".join(
            [self.first_name or "", self.middle_name or "", self.last_name or ""]
        )

        return " ".join(full_name.split())

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctor"


PLACE_TYPE = [
    ("1", "Nepal"),
    ("2", "Foreign Country"),
]