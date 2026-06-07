from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.register, name = 'register'),
    path('login/', views.user_login, name = 'login'), 
    path('logout/', auth_views.LogoutView.as_view(next_page='posts:post_list'), name='logout'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='user/password_reset.html',
            email_template_name='user/password_reset_email.html',
            subject_template_name='user/password_reset_subject.txt',
            success_url=reverse_lazy('user:password_reset_done'),
        ),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html', 
                                                    success_url=reverse_lazy('user:password_reset_complete')),
                                                    name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),
        name='password_reset_complete'
    ),
]