from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('apps.posts.urls', 'posts'), namespace='posts')),
    path('users/', include(('apps.user.urls', 'user'), namespace='user')),
    path('actions/', include(('apps.actions.urls', 'actions'), namespace='actions')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 