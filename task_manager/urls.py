from django.contrib import admin
from django.urls import path, include
from task_manager import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='main_page'),
    path('users/', include('task_manager.users.urls')),
    path('statuses/', include('task_manager.statuses.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('login/', views.LogInView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
]
