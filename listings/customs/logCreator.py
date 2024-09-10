from users.models import UserActionLog


def log_user_action(user, action, details=None, session_id=None):
    UserActionLog.objects.create(user=user, action=action, details=details, session_id=session_id)
