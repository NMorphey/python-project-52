from django.contrib.auth.models import User as _User


class User(_User):
    email = None
