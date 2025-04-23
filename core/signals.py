from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils import timezone
from .models import SessionLog

def get_client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')

@receiver(user_logged_in)
def log_session_start(sender, request, user, **kwargs):
    # garante que a sessão já exista
    if not request.session.session_key:
        request.session.save()
    SessionLog.objects.create(
        user=user,
        session_key=request.session.session_key,
        login_time=timezone.now(),
        ip=get_client_ip(request)
    )

@receiver(user_logged_out)
def log_session_end(sender, request, user, **kwargs):
    sk = request.session.session_key
    try:
        sl = SessionLog.objects.filter(
            user=user,
            session_key=sk,
            logout_time__isnull=True
        ).latest('login_time')
        sl.logout_time = timezone.now()
        sl.save()
    except SessionLog.DoesNotExist:
        pass
