from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm, PostForm
from .forms import SearchForm
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth.decorators import login_required
from .signals import send_notification_email
from django.core.exceptions import PermissionDenied

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
    post_tags_ids = post.tags.values_list('id', flat = True)
    similar_posts = Post.published.filter(tags__in = post_tags_ids).exclude(id = post.id)
    similar_posts = similar_posts.annotate(same_page=Count('tags')).order_by('-same_page', '-publish')[:4]

    #create comments for posts
    new_comment = None
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit = False)
                new_comment.post = post
                new_comment.save()
        else:
            form = CommentForm()
    else:
        return redirect('login')
    return render(request, 'post_detail.html', {'form': form})

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                similarity = TrigramSimilarity('title', query),
            ).filter(similarity__gt = 0.3).order_by('-similarity')
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