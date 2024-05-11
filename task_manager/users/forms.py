from django.forms import ModelForm
from task_manager.users.models import User


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'password1', 'password2'
        ]
