from django.contrib.sessions.models import Session
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from api.models import ActiveSession  # Asegúrate de importar el modelo correcto

User = get_user_model()

class LimitConcurrentSessionsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            session, created = ActiveSession.objects.get_or_create(
                user=request.user,
                session_key=request.session.session_key
            )

            if not created:
                session.last_activity = timezone.now()
                session.save()

            active_sessions = ActiveSession.objects.filter(user=request.user)

            if active_sessions.count() > 1:
                oldest_session = active_sessions.order_by('last_activity').first()
                Session.objects.filter(session_key=oldest_session.session_key).delete()
                oldest_session.delete()

    def process_response(self, request, response):
        if request.user.is_authenticated:
            if request.path == '/logout/':
                ActiveSession.objects.filter(
                    user=request.user,
                    session_key=request.session.session_key
                ).delete()
        return response
