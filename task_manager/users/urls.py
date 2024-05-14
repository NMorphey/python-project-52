from django.urls import path
from task_manager.users import views


urlpatterns = [
    path('', views.UsersIndexView.as_view(), name='users_index'),
    path('create/', views.RegistrationView.as_view(), name='registration'),
    path('<int:id>/update', views.UpdateUserView.as_view(), name='update_user'),  # noqa: E501
    path('<int:id>/delete/', views.DeleteUserView.as_view(), name='delete_user')  # noqa: E501
]
