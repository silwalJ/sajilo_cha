from django.db import models
from django.utils.translation import gettext_lazy as _

class BaseModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class TimeStampAbstractModel(models.Model):
    """Inherit from this class to add timestamp fields in the model class"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserCreatedUpdatedBy(TimeStampAbstractModel):
    """Inherit from this class to add created_by and updated_by fields in the model class"""

    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_created_by",
    )
    updated_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_updated_by",
    )
    is_deleted = models.BooleanField(default=False)

    admin_objects = models.Manager()
    objects = BaseModelManager()

    class Meta:
        abstract = True
