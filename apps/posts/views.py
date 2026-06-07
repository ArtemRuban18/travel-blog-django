from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm, PostForm
from .forms import SearchForm
from django.contrib.postgres.search import TrigramSimilarity, SearchVector
from django.contrib.auth.decorators import login_required
from .signals import send_notification_email
from django.core.exceptions import PermissionDenied
from django.db.models import F

def post_list(request, category_slug = None):
    posts = Post.published.all()
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug = category_slug)
        posts = posts.filter(category__in = [category])

    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post.published, slug = slug)
    post.views += 1
    post.save()
    post_tags_ids = post.tags.values_list('id', flat = True)
    similar_posts = Post.published.filter(tags__in = post_tags_ids).exclude(id = post.id)
    similar_posts = similar_posts.annotate(same_page=Count('tags')).order_by('-same_page', '-publish')[:4]

    comments = post.comments.order_by('-created_at')
    new_comment = None

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'similar_posts': similar_posts,
        'new_comment': new_comment,
    })

def post_search(request):
    form = SearchForm(request.GET or None)
    query = None
    results = Post.published.none()

    if form.is_valid():
        query = form.cleaned_data['query']

        results = Post.published.annotate(
            search_vector = SearchVector('title', 'body'),
            similarity = TrigramSimilarity('title', query) + TrigramSimilarity('body', query)
        ).filter(search_vector=query).order_by('-similarity')

    return render(request, 'post_search.html', {
        'form': form,
        'query': query,
        'results': results
    })

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.save()
            form.save_m2m()
            send_notification_email(sender=Post, instance=post, created=True)
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post.published, slug = slug)
    if request.user != post.author:
        raise PermissionDenied
    if request.method == 'PUT':
        form = PostForm(request.PUT, request.FILES, instance = post)
        if form.is_valid():
            form.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form':form})