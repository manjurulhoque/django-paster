from django.contrib.auth.models import User
from django.utils.timezone import now

from .models import Paste


def recent_pastes(request):
    pastes = Paste.objects.order_by('-created_at').filter(status=1, expire_time__gt=now())[:5]
    return {'pastes': pastes}


def my_recent_pastes(request):
    context = {}
    if request.user.is_authenticated:
        my_recent_pastes = request.user.pastes.all()
        context['my_recent_pastes'] = my_recent_pastes
    return context
