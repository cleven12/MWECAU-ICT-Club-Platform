"""
API authentication and permission classes
"""
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAdminUser


class IsOwner(BasePermission):
    """
    Permission to check if user is the owner of the object
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff


class IsStaffOrReadOnly(BasePermission):
    """
    Permission that allows staff to modify, others can only read
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_staff


class IsApprovedUser(BasePermission):
    """
    Permission that checks if user is approved
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_approved


class IsDepartmentLeader(BasePermission):
    """
    Permission that checks if user is department leader
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_department_leader


class IsKatibu(BasePermission):
    """
    Permission that checks if user is Katibu (Secretary)
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_katibu


class IsLeadership(BasePermission):
    """
    Permission that checks if user is in leadership
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_leadership()


class CanManageDepartment(BasePermission):
    """
    Permission that checks if user can manage a department
    """
    def has_object_permission(self, request, view, obj):
        from accounts.permissions import has_department_permission
        return has_department_permission(request.user, obj.department)


class CanEditUser(BasePermission):
    """
    Permission that checks if user can edit another user
    """
    def has_object_permission(self, request, view, obj):
        from accounts.permissions import can_edit_user
        return can_edit_user(request.user, obj)


class CustomTokenAuthentication(TokenAuthentication):
    """
    Custom token authentication with additional validation
    """
    keyword = 'Bearer'
    
    def authenticate_credentials(self, key):
        """
        Authenticate token and check if user is active
        """
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            return None
        
        if not token.user.is_active:
            return None
        
        return (token.user, token)


API_PERMISSION_CLASSES = [
    IsAuthenticated,
]

API_AUTHENTICATION_CLASSES = [
    TokenAuthentication,
    SessionAuthentication,
]
