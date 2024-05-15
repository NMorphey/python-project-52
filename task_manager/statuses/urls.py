from django.urls import path
from task_manager.statuses import views


urlpatterns = [
    path('', views.StatusesIndexView.as_view(), name='statuses_index'),
    path('create/',
         views.StatusCreateView.as_view(), name='create_status'),
    path('<int:pk>/update/',
         views.StatusUpdateView.as_view(), name='update_status'),
    path('<int:pk>/detele/',
         views.StatusDeleteView.as_view(), name='delete_status')
]
