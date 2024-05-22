from typing import Any
from django.contrib.auth import forms
from django.utils.translation import gettext_lazy as _
from task_manager.users.models import User


class UserForm(forms.UserCreationForm):

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


class UserUpdateForm(UserForm):

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username)\
                .exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                _('A user with that username already exists.'))
        return username
