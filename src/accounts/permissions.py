"""
Permission and role management utilities
"""
from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def get_user_role(user):
    """Get human-readable role for user"""
    if not user.is_authenticated:
        return 'Anonymous'
    
    if user.is_superuser:
        return 'Superadmin'
    elif user.is_staff:
        return 'Staff'
    elif user.is_katibu:
        return 'Secretary (Katibu)'
    elif user.is_katibu_assistance:
        return 'Secretary Assistant'
    elif user.is_department_leader:
        return 'Department Leader'
    elif user.is_approved:
        return 'Member'
    else:
        return 'Pending Member'


def has_department_permission(user, department):
    """Check if user has permission for department"""
    if not user.is_authenticated:
        return False
    
    if user.is_staff:
        return True
    
    if user.is_department_leader and user.department == department:
        return True
    
    return False


def can_edit_user(editor, target_user):
    """Check if editor can edit target user"""
    if editor == target_user:
        return True
    
    if editor.is_staff:
        return True
    
    if editor.is_department_leader and editor.department == target_user.department:
        return True
    
    return False


def can_approve_member(user, target_user):
    """Check if user can approve target user"""
    if not user.is_authenticated:
        return False
    
    if user.is_staff:
        return True
    
    if user.is_katibu or user.is_katibu_assistance:
        return True
    
    if user.is_department_leader and user.department == target_user.department:
        return True
    
    return False


def get_manageable_users(user):
    """Get users that current user can manage"""
    from accounts.models import CustomUser
    
    if user.is_staff:
        return CustomUser.objects.all()
    
    if user.is_katibu or user.is_katibu_assistance:
        return CustomUser.objects.filter(is_staff=False)
    
    if user.is_department_leader:
        return CustomUser.objects.filter(department=user.department)
    
    return CustomUser.objects.none()


def get_manageable_departments(user):
    """Get departments that current user can manage"""
    from accounts.models import Department
    
    if user.is_staff:
        return Department.objects.all()
    
    if user.is_department_leader:
        return Department.objects.filter(id=user.department_id)
    
    return Department.objects.none()


def user_role_display(user):
    """Get formatted role display for user"""
    roles = []
    
    if user.is_superuser:
        roles.append('Superadmin')
    
    if user.is_staff:
        roles.append('Staff')
    
    if user.is_katibu:
        roles.append('Secretary')
    
    if user.is_katibu_assistance:
        roles.append('Sec. Assist.')
    
    if user.is_department_leader:
        roles.append('Dept. Leader')
    
    if not roles:
        roles.append('Member' if user.is_approved else 'Pending')
    
    return ', '.join(roles)


def permission_required(*required_roles):
    """
    Decorator to check if user has required roles
    Usage: @permission_required('staff', 'katibu')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            user = request.user
            
            for role in required_roles:
                if role == 'staff' and user.is_staff:
                    return view_func(request, *args, **kwargs)
                elif role == 'katibu' and user.is_katibu:
                    return view_func(request, *args, **kwargs)
                elif role == 'leader' and user.is_department_leader:
                    return view_func(request, *args, **kwargs)
                elif role == 'approved' and user.is_approved:
                    return view_func(request, *args, **kwargs)
            
            return HttpResponseForbidden("You don't have permission to access this page.")
        
        return wrapper
    return decorator
