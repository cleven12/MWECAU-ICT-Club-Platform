"""
Async task utilities for background operations
"""
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class EmailTask:
    """Utilities for sending emails"""
    
    @staticmethod
    def send_welcome_email(user, approval_url=None):
        """Send welcome email to new user"""
        try:
            subject = f'Welcome to {settings.SITE_NAME}!'
            context = {
                'user': user,
                'approval_url': approval_url,
                'site_name': settings.SITE_NAME,
            }
            
            html_message = render_to_string('emails/registration_confirmation.html', context)
            text_message = strip_tags(html_message)
            
            send_mail(
                subject,
                text_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message,
            )
            
            logger.info(f'Welcome email sent to {user.email}')
        except Exception as e:
            logger.error(f'Failed to send welcome email to {user.email}: {str(e)}')
    
    @staticmethod
    def send_approval_email(user):
        """Send approval email to user"""
        try:
            subject = f'Your {settings.SITE_NAME} Account Has Been Approved!'
            context = {
                'user': user,
                'site_name': settings.SITE_NAME,
                'login_url': settings.LOGIN_URL,
            }
            
            html_message = render_to_string('emails/member_approved.html', context)
            text_message = strip_tags(html_message)
            
            send_mail(
                subject,
                text_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message,
            )
            
            logger.info(f'Approval email sent to {user.email}')
        except Exception as e:
            logger.error(f'Failed to send approval email to {user.email}: {str(e)}')
    
    @staticmethod
    def send_rejection_email(user):
        """Send rejection email to user"""
        try:
            subject = f'{settings.SITE_NAME} Registration Status Update'
            context = {
                'user': user,
                'site_name': settings.SITE_NAME,
            }
            
            html_message = render_to_string('emails/member_rejected.html', context)
            text_message = strip_tags(html_message)
            
            send_mail(
                subject,
                text_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message,
            )
            
            logger.info(f'Rejection email sent to {user.email}')
        except Exception as e:
            logger.error(f'Failed to send rejection email to {user.email}: {str(e)}')
    
    @staticmethod
    def send_picture_reminder_email(user, deadline):
        """Send picture upload reminder email"""
        try:
            subject = f'Profile Picture Upload Reminder - {settings.SITE_NAME}'
            context = {
                'user': user,
                'deadline_date': deadline.date(),
                'deadline_time': deadline.time(),
                'time_remaining': 'Check your dashboard',
                'upload_picture_url': settings.LOGIN_URL,
                'site_name': settings.SITE_NAME,
            }
            
            html_message = render_to_string('emails/picture_reminder.html', context)
            text_message = strip_tags(html_message)
            
            send_mail(
                subject,
                text_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message,
            )
            
            logger.info(f'Picture reminder email sent to {user.email}')
        except Exception as e:
            logger.error(f'Failed to send picture reminder email to {user.email}: {str(e)}')


class NotificationTask:
    """Utilities for sending notifications"""
    
    @staticmethod
    def notify_admins(subject, message, context=None):
        """Send notification to all admins"""
        from accounts.models import CustomUser
        
        admins = CustomUser.objects.filter(is_staff=True)
        admin_emails = [admin.email for admin in admins]
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                admin_emails,
            )
            logger.info(f'Admin notification sent: {subject}')
        except Exception as e:
            logger.error(f'Failed to send admin notification: {str(e)}')
    
    @staticmethod
    def notify_department(department, subject, message):
        """Send notification to all department members"""
        from accounts.models import CustomUser
        
        members = CustomUser.objects.filter(
            department=department,
            is_approved=True
        )
        member_emails = [member.email for member in members]
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                member_emails,
            )
            logger.info(f'Department notification sent to {department.name}')
        except Exception as e:
            logger.error(f'Failed to send department notification: {str(e)}')


class DataTask:
    """Utilities for data processing tasks"""
    
    @staticmethod
    def cleanup_old_logs(days=30):
        """Clean up old activity logs"""
        from core.activity_log import ActivityLog
        from django.utils import timezone
        from datetime import timedelta
        
        cutoff_date = timezone.now() - timedelta(days=days)
        old_logs = ActivityLog.objects.filter(created_at__lt=cutoff_date)
        count = old_logs.count()
        old_logs.delete()
        
        logger.info(f'Cleaned up {count} old activity logs')
        return count
    
    @staticmethod
    def cleanup_old_contact_messages(days=90):
        """Clean up old contact messages"""
        from core.models import ContactMessage
        from django.utils import timezone
        from datetime import timedelta
        
        cutoff_date = timezone.now() - timedelta(days=days)
        old_messages = ContactMessage.objects.filter(
            created_at__lt=cutoff_date,
            is_responded=True
        )
        count = old_messages.count()
        old_messages.delete()
        
        logger.info(f'Cleaned up {count} old contact messages')
        return count
    
    @staticmethod
    def generate_statistics():
        """Generate application statistics"""
        from accounts.models import CustomUser, Department
        from core.models import Project, Event, Announcement
        from membership.models import MembershipPayment
        
        stats = {
            'total_users': CustomUser.objects.count(),
            'approved_users': CustomUser.objects.filter(is_approved=True).count(),
            'pending_users': CustomUser.objects.filter(is_approved=False).count(),
            'total_departments': Department.objects.count(),
            'total_projects': Project.objects.count(),
            'total_events': Event.objects.count(),
            'total_announcements': Announcement.objects.filter(is_published=True).count(),
            'total_payments': MembershipPayment.objects.count(),
            'successful_payments': MembershipPayment.objects.filter(status='success').count(),
        }
        
        logger.info(f'Statistics generated: {stats}')
        return stats
