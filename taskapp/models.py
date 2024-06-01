from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
import pytz

class Tasks(models.Model):
    statuses = [
        ('Not Started', 'Not Started'),
        ('Started', 'Started'),
        ('Ongoing', 'Ongoing'),
        ('Dropped', 'Dropped'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100, default="Task Name")
    status = models.CharField(max_length=20, default='Not Started', choices=statuses)
    priority = models.CharField(max_length=20)
    deadline = models.DateField()
    remarks = models.CharField(max_length=100, default='Task not started yet')
    last_updated = models.DateTimeField(auto_now=True)

    update_history = models.JSONField(default=list)

    def add_update_history(self, user, updated_fields):
        relevant_fields = {'status', 'remarks'}
        filtered_updates = {field: (getattr(self, field), updated_fields[field]) for field in relevant_fields if field in updated_fields}

        if filtered_updates:
            timestamp_utc = timezone.now()
            timestamp_ist = timestamp_utc.astimezone(pytz.timezone('Asia/Kolkata'))

            update_entry = {
                'user': user.username,
                'timestamp': timestamp_ist.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_fields': {field: {'from': values[0], 'to': values[1]} for field, values in filtered_updates.items()},
            }
            self.update_history.append(update_entry)
            self.save()

class TasksAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'status', 'priority', 'deadline', 'remarks', 'last_updated')
    list_filter = ['status', 'priority', 'deadline']
    exclude = ('update_history',) 
    

class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

