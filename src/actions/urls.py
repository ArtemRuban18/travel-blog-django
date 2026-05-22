from django.urls import path
from . import views

urlpatterns = [
    path('like-post/<slug:slug>/', views.like_post, name = "like_post"),
    path('like-comment/<int:id>/', views.like_comment, name = "like_comment"),
]