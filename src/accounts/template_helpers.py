"""
Template context processor utilities
"""
from django.conf import settings
from django.contrib.messages import get_messages


def global_context(request):
    """Add global context variables available to all templates"""
    return {
        'site_name': 'MWECAU ICT Club',
        'site_url': settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://localhost:8000',
        'support_email': settings.DEFAULT_FROM_EMAIL,
        'current_year': __import__('datetime').datetime.now().year,
        'is_authenticated': request.user.is_authenticated,
    }


def user_context(request):
    """Add user-specific context"""
    context = {}
    
    if request.user.is_authenticated:
        context.update({
            'user_department': request.user.department,
            'user_role': getattr(request.user, 'get_role_display', lambda: 'Member')(),
            'is_leadership': (
                request.user.is_department_leader or
                request.user.is_superuser
            ),
            'is_admin': request.user.is_superuser or request.user.is_staff,
        })
    
    return context


def messages_context(request):
    """Add messages to context"""
    return {
        'messages': get_messages(request),
    }


def feature_flags_context(request):
    """Add feature flags to context"""
    features = getattr(settings, 'FEATURES', {})
    
    return {
        'features': features,
    }


class TemplateHelpers:
    """Helper functions for templates"""
    
    @staticmethod
    def get_gravatar_url(email, size=200):
        """Get Gravatar URL for email"""
        import hashlib
        email_hash = hashlib.md5(email.lower().encode()).hexdigest()
        return f'https://www.gravatar.com/avatar/{email_hash}?s={size}&d=identicon'
    
    @staticmethod
    def truncate_text(text, length=100):
        """Truncate text to specified length"""
        if len(text) > length:
            return text[:length] + '...'
        return text
    
    @staticmethod
    def get_initials(full_name):
        """Get initials from full name"""
        names = full_name.split()
        if len(names) >= 2:
            return f'{names[0][0]}{names[-1][0]}'.upper()
        elif len(names) == 1:
            return names[0][0].upper()
        return ''
    
    @staticmethod
    def format_date(date, format_string='%Y-%m-%d'):
        """Format date with specified format"""
        if date is None:
            return ''
        try:
            return date.strftime(format_string)
        except:
            return str(date)
    
    @staticmethod
    def get_badge_color(status):
        """Get badge color for status"""
        color_map = {
            'pending': 'warning',
            'approved': 'success',
            'rejected': 'danger',
            'active': 'info',
            'inactive': 'secondary',
            'draft': 'warning',
            'published': 'success',
        }
        return color_map.get(status.lower(), 'secondary')
    
    @staticmethod
    def is_overdue(deadline):
        """Check if deadline is overdue"""
        from django.utils import timezone
        if deadline is None:
            return False
        return deadline < timezone.now()


class FormHelpers:
    """Template form helpers"""
    
    @staticmethod
    def add_bootstrap_class(field):
        """Add Bootstrap class to form field"""
        field.field.widget.attrs['class'] = 'form-control'
        return field
    
    @staticmethod
    def get_field_error_class(field):
        """Get error class for field if it has errors"""
        if field.errors:
            return 'is-invalid'
        return ''
    
    @staticmethod
    def get_field_help_text(field):
        """Get help text for field"""
        return field.help_text if field.help_text else ''
