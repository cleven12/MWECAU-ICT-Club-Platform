"""
Management command to test email configuration and send test emails
Usage: python manage.py test_email --recipient=user@example.com
       python manage.py test_email --check-config
"""
import logging
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from accounts.email_service import EmailService
from accounts.models import CustomUser

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Test email configuration and send test emails'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--recipient',
            type=str,
            help='Email address to send test email to'
        )
        
        parser.add_argument(
            '--check-config',
            action='store_true',
            help='Check email configuration without sending email'
        )
        
        parser.add_argument(
            '--test-user',
            type=int,
            help='Send test email to a specific user by ID'
        )
    
    def handle(self, *args, **options):
        check_config = options.get('check_config', False)
        recipient = options.get('recipient')
        test_user_id = options.get('test_user')
        
        if check_config:
            self.check_email_config()
        elif test_user_id:
            self.send_test_email_to_user(test_user_id)
        elif recipient:
            self.send_test_email(recipient)
        else:
            raise CommandError('Please provide either --check-config, --recipient, or --test-user')
    
    def check_email_config(self):
        """Check if email configuration is valid"""
        self.stdout.write(self.style.SUCCESS('\nChecking Email Configuration...'))
        
        try:
            # Check settings
            self.stdout.write(f'\nEmail Configuration:')
            self.stdout.write(f'  EMAIL_BACKEND: {settings.EMAIL_BACKEND}')
            self.stdout.write(f'  EMAIL_HOST: {settings.EMAIL_HOST}')
            self.stdout.write(f'  EMAIL_PORT: {settings.EMAIL_PORT}')
            self.stdout.write(f'  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}')
            self.stdout.write(f'  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}')
            self.stdout.write(f'  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}')
            
            # Check if password is set
            if settings.EMAIL_HOST_PASSWORD:
                self.stdout.write(f'  EMAIL_HOST_PASSWORD: {"*" * 10}')
            else:
                self.stdout.write(self.style.WARNING('  EMAIL_HOST_PASSWORD: NOT SET'))
            
            # Validate configuration
            if EmailService._validate_email_config():
                self.stdout.write(self.style.SUCCESS('\n✓ Email configuration is valid!'))
            else:
                self.stdout.write(self.style.ERROR('\n✗ Email configuration is invalid!'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n✗ Error checking configuration: {str(e)}'))
            logger.error(f"Error checking email config: {str(e)}", exc_info=True)
    
    def send_test_email(self, recipient):
        """Send a test email to the specified recipient"""
        self.stdout.write(f'Sending test email to {recipient}...')
        
        try:
            success, error = EmailService.send_single_email(
                subject='Test Email from ICT Club',
                recipient_email=recipient,
                html_template='emails/test_email.html',
                context={
                    'recipient_email': recipient,
                    'timestamp': str(__import__('django.utils.timezone', fromlist=['now']).now())
                },
                plain_message='This is a test email from ICT Club. If you received this, email configuration is working correctly!',
                fail_silently=False
            )
            
            if success:
                self.stdout.write(self.style.SUCCESS(f'\n✓ Test email sent successfully to {recipient}'))
                logger.info(f"Test email sent to {recipient}")
            else:
                self.stdout.write(self.style.ERROR(f'\n✗ Failed to send test email: {error}'))
                logger.error(f"Failed to send test email to {recipient}: {error}")
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n✗ Exception while sending test email: {str(e)}'))
            logger.error(f"Exception sending test email: {str(e)}", exc_info=True)
    
    def send_test_email_to_user(self, user_id):
        """Send test email to a user by ID"""
        try:
            user = CustomUser.objects.get(id=user_id)
            self.stdout.write(f'Sending test email to {user.full_name} ({user.email})...')
            
            success, error = EmailService.send_single_email(
                subject='Test Email from ICT Club',
                recipient_email=user.email,
                html_template='emails/test_email.html',
                context={
                    'user': user,
                    'recipient_email': user.email,
                    'timestamp': str(__import__('django.utils.timezone', fromlist=['now']).now())
                },
                plain_message='This is a test email from ICT Club.',
                fail_silently=False
            )
            
            if success:
                self.stdout.write(self.style.SUCCESS(f'\n✓ Test email sent successfully to {user.full_name}'))
                logger.info(f"Test email sent to user {user.id}")
            else:
                self.stdout.write(self.style.ERROR(f'\n✗ Failed to send test email: {error}'))
                
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User with ID {user_id} not found'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Exception: {str(e)}'))
            logger.error(f"Exception in test_email command: {str(e)}", exc_info=True)
