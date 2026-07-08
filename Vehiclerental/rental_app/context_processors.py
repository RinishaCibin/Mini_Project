from .models import Notification


def notifications(request):

    if request.user.is_authenticated:

        notifications = Notification.objects.filter(
            user=request.user
        ).order_by('-created_at')

        unread_count = notifications.filter(
            is_read=False
        ).count()

        return {
            "notifications": notifications[:5],
            "unread_count": unread_count
        }

    return {
        "notifications": [],
        "unread_count": 0
    }