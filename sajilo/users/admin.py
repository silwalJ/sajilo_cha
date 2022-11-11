from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

from sajilo.users.models import (
    User, 
    UserDocument, 
    Medicalhistory, 
    Patient, 
    Doctor, 
    DoctorTrainingHistory, 
    DoctorWorkExperience, 
    Education,
    CustomPermission,
    Role,
)


# @admin.register(User)
# class UserAdmin(UserAdmin):
#     pass

admin.site.register(User)
admin.site.register(UserDocument)
admin.site.register(CustomPermission)
admin.site.register(Role)
admin.site.register(Medicalhistory)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(DoctorTrainingHistory)
admin.site.register(Education)
admin.site.register(DoctorWorkExperience)