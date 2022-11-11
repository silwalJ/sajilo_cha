import random
import string

from django.utils.text import slugify


def generate_random_string(N):
    res = "".join(random.choices(string.ascii_uppercase + string.digits, k=N))

    return res


def generate_key(text):
    new_key = slugify(text)
    from users.models import CustomPermission

    if CustomPermission.objects.filter(key=new_key).first():
        return generate_key(text + generate_random_string(6))
    return new_key
