from django.http import JsonResponse
from posts.models import Post, Comment
from .models import Likes
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required

@login_required
def like_post(request, slug):
    post = Post.published.get(slug = slug)

    ct = ContentType.objects.get_for_model(Post)

    Likes.objects.create(
        user = request.user,
        content_type = ct,
        content_id = post.id
    )
    
    return JsonResponse({"status": "liked post"})

@login_required
def like_comment(request, id):
    comment = Comment.objects.get(id = id)

    ct = ContentType.objects.get_for_model(Comment)

    Likes.objects.create(
        user = request.user,
        content_type = ct,
        content_id = comment.id
    )
    return JsonResponse({"status": "liked comment"})