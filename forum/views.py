from django.shortcuts import render, redirect, get_object_or_404
from .models import ForumPost, Like
from .forms import ForumPostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count

def forum_list(request):
    posts = ForumPost.objects.annotate(total_likes=Count('likes')).order_by('-total_likes', '-created_at')
    return render(request, 'forum_list.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            forum_post = form.save(commit=False)
            forum_post.author = request.user
            forum_post.save()
            return redirect('Forum:forum_list')
    else:
        form = ForumPostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        # User already liked this post; remove the like
        like.delete()
    return redirect('Forum:forum_list')
