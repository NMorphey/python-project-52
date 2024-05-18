from django.contrib.auth.models import User as _User


class User(_User):
    email = None

    def __str__(self):
        return self.get_full_name()
