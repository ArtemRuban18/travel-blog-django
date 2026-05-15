from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='post_list'),
    path('category/<slug:category_slug>/', views.post_list, name = 'post_list_by_categoty'),
    path('<slug:slug>/', views.post_detail, name = 'post_detail'),
]