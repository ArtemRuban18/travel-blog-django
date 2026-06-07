from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from apps.posts.models import Post, Comment
from .models import Likes
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required

@login_required
def like_post(request, slug):
    if request.method != 'POST':
        return JsonResponse({'status': 'method not allowed'}, status=405)

    post = get_object_or_404(Post.published, slug=slug)
    content_type = ContentType.objects.get_for_model(Post)

    like = Likes.objects.filter(
        user=request.user,
        content_type=content_type,
        content_id=post.id,
    ).first()

    if like:
        like.delete()
        return JsonResponse({'status': 'unliked post'})

    Likes.objects.create(
        user=request.user,
        content_type=content_type,
        content_id=post.id,
    )
    return JsonResponse({'status': 'liked post'})

@login_required
def like_comment(request, id):
    if request.method != 'POST':
        return JsonResponse({'status': 'method not allowed'}, status=405)

    comment = get_object_or_404(Comment, id=id)
    content_type = ContentType.objects.get_for_model(Comment)

    like = Likes.objects.filter(
        user=request.user,
        content_type=content_type,
        content_id=comment.id,
    ).first()

    if like:
        like.delete()
        return JsonResponse({'status': 'unliked comment'})

    Likes.objects.create(
        user=request.user,
        content_type=content_type,
        content_id=comment.id,
    )
    return JsonResponse({'status': 'liked comment'})