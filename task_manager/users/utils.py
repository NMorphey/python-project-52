from django.contrib.messages import error
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


def check_access_to_modify(function):
    def inner(self, request, *args, **kwargs):
        if kwargs['pk'] != request.user.id:
            error(
                request, _('You are not authorized to modify other users.')
            )
            return redirect('users_index')
        return function(self, request, *args, **kwargs)
    return inner
