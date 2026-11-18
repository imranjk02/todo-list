from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Task

def home(request):

    tasks = Task.objects.all().order_by('-created_at')
    search_query = request.GET.get('search', '')

    if search_query:

        tasks = tasks.filter(title__icontains=search_query)

    status = request.GET.get('status', 'all')

    if status == 'completed':
        tasks = tasks.filter(completed=True)

    elif status == 'pending':
        tasks = tasks.filter(completed=False)

    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(completed=True).count()
    pending_tasks = Task.objects.filter(completed=False).count()

    context = {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'search_query': search_query,
        'status': status
    }
    return render(request, 'tasks/home.html', context)


def add_task(request):

    if request.method == 'POST':

        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        if not title:

            messages.error(request, 'Task title is required.')
            return redirect('home')

        if len(title) > 200:

            messages.error(request, 'Title cannot exceed 200 characters.')
            return redirect('home')

        Task.objects.create(title=title, description=description)
        messages.success(request, 'Task added successfully!')

    return redirect('home')

def edit_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':

        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        if not title:

            messages.error(request, 'Task title is required.')
            return render(request, 'tasks/edit_task.html', {'task': task})

        if len(title) > 200:

            messages.error(request, 'Title cannot exceed 200 characters.')
            return render(request, 'tasks/edit_task.html', {'task': task})

        task.title = title
        task.description = description
        task.save()
        messages.success(request, 'Task updated successfully!')
        return redirect('home')

    return render(request, 'tasks/edit_task.html', {'task': task})


@require_POST
def complete_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    messages.success(request, 'Task status updated!')
    return redirect('home')


@require_POST
def delete_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)
    task.delete()
    messages.success(request, 'Task deleted successfully!')
    return redirect('home')