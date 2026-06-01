from .models import Category


def categories(request):
    return {
        'categories': Category.objects.all(),
    }

def profile(request):
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        return {
            'profile': request.user.profile,
        }
    return {}
