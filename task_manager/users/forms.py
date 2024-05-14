from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from task_manager.users.models import User
from django.utils.translation import gettext_lazy as _


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'password1', 'password2'
        ]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'form-control', 'required': True}
            )
            self.fields[field].widget.attrs['placeholder'] = \
                self.fields[field].label


class LoginForm(UserForm):

    class Meta:
        model = User
        fields = ['username', 'password1']
