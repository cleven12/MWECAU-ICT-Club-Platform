"""
Notification system utilities
"""
import logging
from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


class NotificationTypes:
    """Notification type constants"""
    
    USER_APPROVED = 'user_approved'
    USER_REJECTED = 'user_rejected'
    PICTURE_REMINDER = 'picture_reminder'
    EVENT_UPCOMING = 'event_upcoming'
    ANNOUNCEMENT_NEW = 'announcement_new'
    PROJECT_UPDATE = 'project_update'
    COMMENT_REPLY = 'comment_reply'
    MESSAGE_RECEIVED = 'message_received'


class NotificationManager:
    """Manage user notifications"""
    
    @staticmethod
    def create_notification(user, notification_type, title, message, related_object=None):
        """Create a new notification"""
        from accounts.models import Notification
        
        try:
            notification = Notification.objects.create(
                user=user,
                notification_type=notification_type,
                title=title,
                message=message,
                related_object=related_object,
                created_at=timezone.now()
            )
            logger.info(f'Notification created for {user.email}: {notification_type}')
            return notification
        except Exception as e:
            logger.error(f'Failed to create notification: {str(e)}')
            return None
    
    @staticmethod
    def get_user_notifications(user, unread_only=False):
        """Get user notifications"""
        from accounts.models import Notification
        
        notifications = Notification.objects.filter(user=user)
        
        if unread_only:
            notifications = notifications.filter(is_read=False)
        
        return notifications.order_by('-created_at')
    
    @staticmethod
    def mark_as_read(notification):
        """Mark notification as read"""
        try:
            notification.is_read = True
            notification.read_at = timezone.now()
            notification.save()
            return True
        except Exception as e:
            logger.error(f'Failed to mark notification as read: {str(e)}')
            return False
    
    @staticmethod
    def mark_all_as_read(user):
        """Mark all user notifications as read"""
        from accounts.models import Notification
        
        try:
            count = Notification.objects.filter(
                user=user,
                is_read=False
            ).update(
                is_read=True,
                read_at=timezone.now()
            )
            return count
        except Exception as e:
            logger.error(f'Failed to mark all notifications as read: {str(e)}')
            return 0
    
    @staticmethod
    def delete_notification(notification):
        """Delete a notification"""
        try:
            notification.delete()
            return True
        except Exception as e:
            logger.error(f'Failed to delete notification: {str(e)}')
            return False


class NotificationDispatcher:
    """Dispatch notifications to users"""
    
    @staticmethod
    def notify_user_approval(user):
        """Notify user about approval"""
        NotificationManager.create_notification(
            user=user,
            notification_type=NotificationTypes.USER_APPROVED,
            title='Account Approved',
            message='Your account has been approved! Please upload your profile picture within 72 hours.'
        )
    
    @staticmethod
    def notify_user_rejection(user, reason=''):
        """Notify user about rejection"""
        message = f'Your registration has been rejected. Reason: {reason}' if reason else 'Your registration has been rejected.'
        
        NotificationManager.create_notification(
            user=user,
            notification_type=NotificationTypes.USER_REJECTED,
            title='Registration Rejected',
            message=message
        )
    
    @staticmethod
    def notify_picture_reminder(user):
        """Notify user about picture upload deadline"""
        from core.utils import get_time_remaining
        
        time_left = get_time_remaining(user.picture_deadline)
        
        NotificationManager.create_notification(
            user=user,
            notification_type=NotificationTypes.PICTURE_REMINDER,
            title='Picture Upload Reminder',
            message=f'Please upload your profile picture. Time remaining: {time_left}'
        )
    
    @staticmethod
    def notify_event_upcoming(user, event):
        """Notify user about upcoming event"""
        NotificationManager.create_notification(
            user=user,
            notification_type=NotificationTypes.EVENT_UPCOMING,
            title=f'Upcoming Event: {event.title}',
            message=f'Event starts on {event.event_date}',
            related_object=event
        )
    
    @staticmethod
    def notify_new_announcement(users, announcement):
        """Notify multiple users about new announcement"""
        for user in users:
            NotificationManager.create_notification(
                user=user,
                notification_type=NotificationTypes.ANNOUNCEMENT_NEW,
                title=f'New Announcement: {announcement.title}',
                message=announcement.content[:100],
                related_object=announcement
            )


class NotificationPreferences:
    """Manage user notification preferences"""
    
    @staticmethod
    def get_user_preferences(user):
        """Get user notification preferences"""
        try:
            from accounts.models import NotificationPreference
            pref, _ = NotificationPreference.objects.get_or_create(user=user)
            return pref
        except:
            return None
    
    @staticmethod
    def set_preference(user, notification_type, enabled):
        """Set notification preference"""
        try:
            from accounts.models import NotificationPreference
            pref = NotificationPreferences.get_user_preferences(user)
            
            if pref:
                setattr(pref, f'{notification_type}_enabled', enabled)
                pref.save()
                return True
        except Exception as e:
            logger.error(f'Failed to set notification preference: {str(e)}')
        
        return False
