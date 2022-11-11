import uuid

from rest_framework import serializers


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


def pop_or_none(dict_, key):
    try:
        return dict_.pop(key)
    except KeyError:
        return None


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


def generate_code(n):
    return uuid.uuid4().hex[:n].upper()


def file_size_validator(upload_file, file_max_size=2 * 1024 * 1024):
    if upload_file is not None and upload_file.size > file_max_size:
        raise serializers.ValidationError(
            f"File size must be smaller than {file_max_size}"
        )
