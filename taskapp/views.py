from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Tasks, UserDetail
from .forms import TaskForm , UserForm, UpdateTaskForm
from django.contrib.auth import  login as auth_login,logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserDetail.objects.create(user=user)
            auth_login(request, user)
            return redirect('login')
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def task_list(request):
    tasks = Tasks.objects.filter(user=request.user)
    return render(request, 'view_tasks.html', {'tasks': tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.assign_to = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form, 'action': 'Add'})

@login_required
def update_task(request, task_id):
    task = get_object_or_404(Tasks, id=task_id, user=request.user)

    if request.method == 'POST':
        form = UpdateTaskForm(request.POST, instance=task)
        if form.is_valid():
            updated_task = form.save(commit=False)
            original_task = Tasks.objects.get(pk=task_id)
            updated_fields = {}

            for field in form.changed_data:
                original_value = getattr(original_task, field)
                updated_value = getattr(updated_task, field)
                updated_fields[field] = {'from': original_value, 'to': updated_value}

            updated_task.save()
            task.add_update_history(request.user, updated_fields)
            return redirect('task_list')
    else:
        form = UpdateTaskForm(instance=task)

    return render(request, 'update_task.html', {'form': form, 'action': 'Update'})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Tasks, id=task_id, user=request.user)
    
    return render(request, 'task_detail.html', {'task': task})

def delete_task(request, task_id):
    task = get_object_or_404(Tasks, id=task_id, user=request.user)
    task.delete()
    return redirect('task_list')

def confirm_delete(request, task_id):
    task = get_object_or_404(Tasks, id=task_id, user=request.user)
    return render(request, 'confirm_delete.html', {'task': task})
