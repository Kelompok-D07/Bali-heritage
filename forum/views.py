# forum/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Forum, Like
from django.contrib.auth.decorators import login_required
from django.db.models import (
    Count, Exists, OuterRef, Value, BooleanField,
    Case, When, Q, IntegerField
)
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from django.utils.html import escape, mark_safe
from Homepage.models import Restaurant  # Import Restaurant
import re
import uuid
from django.core.paginator import Paginator

def highlight_text(text, search_query):
    # Escape the text to prevent XSS
    text = escape(text)
    # Use regex to replace the search term with highlighted version
    pattern = re.compile(re.escape(search_query), re.IGNORECASE)
    highlighted_text = pattern.sub(
        lambda m: f'<span class="bg-yellow-200">{m.group()}</span>',
        text
    )
    return mark_safe(highlighted_text)

def forum_list(request):
    search_query = request.GET.get('q', '').strip()
    forums = Forum.objects.annotate(total_likes=Count('likes'))

    if request.user.is_authenticated:
        user_likes = Like.objects.filter(user=request.user, forum=OuterRef('pk'))
        forums = forums.annotate(has_liked=Exists(user_likes))
    else:
        forums = forums.annotate(has_liked=Value(False, output_field=BooleanField()))

    forums = forums.order_by('-created_at')

    if search_query:
        forums = forums.annotate(
            is_title_match=Case(
                When(title__icontains=search_query, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            is_content_match=Case(
                When(content__icontains=search_query, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
        ).filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        ).annotate(
            search_rank=Case(
                When(is_title_match=True, then=Value(1)),
                When(is_content_match=True, then=Value(2)),
                output_field=IntegerField(),
            )
        ).order_by('search_rank', '-created_at')

    # Apply highlighting without modifying original fields
    for forum in forums:
        if search_query:
            if forum.is_title_match:
                forum.highlighted_title = highlight_text(forum.title, search_query)
            else:
                forum.highlighted_title = escape(forum.title)

            if forum.is_content_match:
                forum.highlighted_content = highlight_text(forum.content, search_query)
            else:
                forum.highlighted_content = escape(forum.content)
        else:
            forum.highlighted_title = escape(forum.title)
            forum.highlighted_content = escape(forum.content)

    return render(request, 'forum_list.html', {
        'forums': forums,
        'search_query': search_query,
    })

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Forum, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, forum=post)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'success': True,
            'liked': liked,
            'total_likes': post.total_likes(),
        }
        return JsonResponse(data)
    else:
        return redirect('forum:forum_list')

@login_required
def create_post(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        recommendations_ids = request.POST.getlist('recommendations')

        # Validate input
        if not title or not content:
            return JsonResponse({'success': False, 'error': 'Title and content are required.'}, status=400)

        # Escape user input to prevent XSS
        title = escape(title)
        content = escape(content)

        # Create the new forum post
        post = Forum.objects.create(
            title=title,
            content=content,
            author=request.user,
            created_at=timezone.now()
        )

        # Add recommendations if any
        if recommendations_ids:
            try:
                recommendations_ids = [uuid.UUID(id_) for id_ in recommendations_ids]
                restaurants = Restaurant.objects.filter(id__in=recommendations_ids)
                post.recommendations.set(restaurants)
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid recommendations.'}, status=400)
        else:
            post.recommendations.clear()

        # Prepare data to return
        recommendations_data = []
        for rec in post.recommendations.all():
            recommendations_data.append({
                'id': str(rec.id),
                'name': rec.name,
            })

        data = {
            'success': True,
            'post': {
                'id': str(post.id),
                'title': post.title,
                'content': post.content,
                'recommendations': recommendations_data,
                'author': post.author.username,
                'created_at': post.created_at.strftime('%Y-%m-%d %H:%M'),
                'total_likes': post.total_likes(),
                'has_liked': False,
            }
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=400)

@login_required
def get_post(request, post_id):
    post = get_object_or_404(Forum, id=post_id)

    # Check if the current user is the author
    if post.author != request.user:
        return JsonResponse({'success': False, 'error': 'You are not allowed to edit this post.'}, status=403)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        recommendations = post.recommendations.all()
        recommendations_ids = [str(rec.id) for rec in recommendations]
        recommendations_names = {str(rec.id): rec.name for rec in recommendations}
        data = {
            'success': True,
            'post': {
                'id': str(post.id),
                'title': post.title,
                'content': post.content,
                'recommendations': recommendations_ids,
                'recommendations_names': recommendations_names,
            }
        }
        return JsonResponse(data)
    else:
        return HttpResponseBadRequest('Invalid request.')

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Forum, id=post_id)

    # Check if the current user is the author
    if post.author != request.user:
        return JsonResponse({'success': False, 'error': 'You are not allowed to edit this post.'}, status=403)

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        recommendations_ids = request.POST.getlist('recommendations')

        # Validate input
        if not title or not content:
            return JsonResponse({'success': False, 'error': 'Title and content are required.'}, status=400)

        # Escape user input to prevent XSS
        title = escape(title)
        content = escape(content)

        # Update the post
        post.title = title
        post.content = content
        post.save()

        # Update recommendations
        if recommendations_ids:
            try:
                recommendations_ids = [uuid.UUID(id_) for id_ in recommendations_ids]
                restaurants = Restaurant.objects.filter(id__in=recommendations_ids)
                post.recommendations.set(restaurants)
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid recommendations.'}, status=400)
        else:
            post.recommendations.clear()

        # Prepare data to return
        recommendations_data = []
        for rec in post.recommendations.all():
            recommendations_data.append({
                'id': str(rec.id),
                'name': rec.name,
            })

        data = {
            'success': True,
            'post': {
                'id': str(post.id),
                'title': post.title,
                'content': post.content,
                'recommendations': recommendations_data,
            }
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=400)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Forum, id=post_id)

    # Check if the current user is the author
    if post.author != request.user:
        return JsonResponse({'success': False, 'error': 'You are not allowed to delete this post.'}, status=403)

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        post.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=400)

def restaurant_search(request):
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))

    restaurants = Restaurant.objects.filter(name__icontains=query).order_by('name')

    # Use Paginator if the list is long
    paginator = Paginator(restaurants, 10)  # 10 restaurants per page
    restaurants_page = paginator.get_page(page)

    results = []
    for restaurant in restaurants_page:
        results.append({
            'id': str(restaurant.id),  # Ensure ID is converted to string
            'text': restaurant.name,
        })

    data = {
        'results': results,
        'pagination': {
            'more': restaurants_page.has_next()
        }
    }
    return JsonResponse(data)
