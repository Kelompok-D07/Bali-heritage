from django.shortcuts import render, get_object_or_404, redirect
from .models import Forum
from .forms import ForumForm
from django.contrib.auth.decorators import login_required

def forum_list(request):
    forums = Forum.objects.all().order_by('-created_at')
    return render(request, 'forum/forum_list.html', {'forums': forums})

def forum_detail(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    return render(request, 'forum/forum_detail.html', {'forum': forum})

@login_required
def forum_create(request):
    if request.method == 'POST':
        form = ForumForm(request.POST)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.author = request.user
            forum.save()
            return redirect('forum_detail', pk=forum.pk)
    else:
        form = ForumForm()
    return render(request, 'forum/forum_form.html', {'form': form})

@login_required
def forum_like(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    if request.user in forum.likes.all():
        forum.likes.remove(request.user)
    else:
        forum.likes.add(request.user)
    return redirect('forum_detail', pk=pk)
