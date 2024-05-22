from django.contrib.auth.models import User as User_

class User(User_):
    class Meta:
        proxy = True

    def __str__(self):
        return self.get_full_name()
