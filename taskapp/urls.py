from django.urls import path
from .views import task_list, task_detail, add_task, update_task, register, login, logout, confirm_delete, delete_task

urlpatterns = [
    path('', register, name='register'),
    path('login/', login, name='login'),
    path('tasks/', task_list, name='task_list'),  
    path('tasks/<int:task_id>/', task_detail, name='task_detail'),
    path('tasks/add/', add_task, name='add_task'),
    path('tasks/<int:task_id>/update/', update_task, name='update_task'),
    path('logout/', logout, name='logout'),
    path('tasks/<int:task_id>/confirm_delete/', confirm_delete, name='confirm_delete'), 
    path('tasks/<int:task_id>/delete/', delete_task, name='delete_task'),
]
