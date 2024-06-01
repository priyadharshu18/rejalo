from django.contrib import admin
from .models import Tasks, TasksAdmin

admin.site.register(Tasks, TasksAdmin)