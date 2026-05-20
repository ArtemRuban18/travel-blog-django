from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate
from .forms import CommentForm

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
    post = Post.published.get(slug = slug)
    post_tags_ids = post.tags.values_list('id', flat = True)
    similar_posts = Post.published.filter(tags__in = post_tags_ids).exclude(id = post.id)
    similar_posts = similar_posts.annotate(same_page = Count('tags')).order_by('-same_page', '-publish')[:4]

    #create comments for posts
    new_comment = None
    if request.user is authenticate:
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

 