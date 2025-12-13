"""
Django signals for accounts app
- Send email when user account is approved
- Send email when user account is rejected
- Comprehensive error handling and logging
"""
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import CustomUser
from .email_service import EmailService

logger = logging.getLogger(__name__)


@receiver(post_save, sender=CustomUser)
def send_approval_notification(sender, instance, created, update_fields, **kwargs):
    """
    Signal to send approval email when user's is_approved field changes to True
    
    Triggered when:
    - User's is_approved field is updated to True
    - Sends confirmation email to user
    - Sets approval timestamp
    """
    # Only process update signals (not create)
    if created:
        return
    
    # Check if is_approved was just updated to True
    if update_fields and 'is_approved' in update_fields:
        if instance.is_approved:
            try:
                # Send approval email with proper error handling
                success, error = EmailService.send_approval_email(instance)
                
                if success:
                    logger.info(f"Approval email sent to {instance.email} for user {instance.full_name}")
                else:
                    logger.error(f"Failed to send approval email to {instance.email}: {error}")
                
                # Set approved_at timestamp
                if not instance.approved_at:
                    instance.approved_at = timezone.now()
                    instance.save(update_fields=['approved_at'])
                    logger.info(f"Approval timestamp set for user {instance.full_name}")
                    
            except Exception as e:
                logger.error(
                    f"Exception in approval signal for user {instance.full_name}: {str(e)}",
                    exc_info=True
                )
