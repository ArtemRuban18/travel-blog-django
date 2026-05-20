from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('category/<slug:category_slug>/', views.post_list, name = 'post_list_by_category'),
    path('<slug:slug>/', views.post_detail, name = 'post_detail'),
    path('search/?query=<str:query>/', views.post_search, name = 'post_search'),
]