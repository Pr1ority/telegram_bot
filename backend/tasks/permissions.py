from rest_framework.permissions import BasePermission


class IsBotOrAuthenticated(BasePermission):
    """Разрешает боту доступ без токена"""

    BOT_USER_AGENT = 'TaskBot/1.0'

    def has_permission(self, request, view):

        user_agent = request.headers.get('User-Agent', '')
        user_id = request.headers.get('X-User-ID')

        if user_agent == self.BOT_USER_AGENT and not user_id:
            return False

        if user_agent == self.BOT_USER_AGENT:
            return True

        return request.user and request.user.is_authenticated
