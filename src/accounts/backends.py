"""
Custom authentication backend for ICT Club
Supports authentication using email, registration number, or username
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()


class EmailOrRegNumberBackend(ModelBackend):
    """
    Custom backend to authenticate users using email, registration number, or username
    Allows flexible login using any of these credentials
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Override authenticate to support email and registration number
        
        Args:
            request: HTTP request object
            username: Can be username, email, or registration number
            password: User's password
            
        Returns:
            User instance if authentication successful, None otherwise
        """
        try:
            # Try to find user by email, registration number, or username
            user = User.objects.get(
                Q(email__iexact=username) |
                Q(reg_number__iexact=username) |
                Q(username__iexact=username)
            )
        except User.DoesNotExist:
            # Run the default password hasher once to reduce timing
            # difference between existing and non-existing users
            User().set_password(password)
            return None
        except User.MultipleObjectsReturned:
            # This shouldn't happen with unique constraints, but handle it
            user = User.objects.filter(
                Q(email__iexact=username) |
                Q(reg_number__iexact=username) |
                Q(username__iexact=username)
            ).first()
            if user is None:
                return None
        
        # Check password and active status
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
    
    def get_user(self, user_id):
        """Get user by ID"""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
