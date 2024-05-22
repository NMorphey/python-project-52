from task_manager.utils import error_flash
from django.shortcuts import redirect


def check_access_to_modify(function):
    def inner(self, request, *args, **kwargs):
        if kwargs['pk'] != request.user.id:
            error_flash(
                request, 'You are not authorized to modify other users.'
            )
            return redirect('users_index')
        return function(self, request, *args, **kwargs)
    return inner
