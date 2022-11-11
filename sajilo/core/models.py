from django.db import models
from django.utils.translation import gettext_lazy as _

class TimeStampAbstractModel(models.Model):
    """Inherit from this class to add timestamp fields in the model class"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
