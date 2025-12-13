"""
Decorators for common view functionalities
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden


def approval_required(view_func):
    """Decorator to require user approval"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        if not request.user.is_approved:
            messages.warning(request, 'Your account is pending approval. Please wait for admin approval.')
            return redirect('accounts:pending_approval')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def picture_required(view_func):
    """Decorator to require profile picture"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        if not request.user.profile_picture:
            messages.warning(request, 'Please upload your profile picture.')
            return redirect('accounts:upload_picture')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def leadership_required(view_func):
    """Decorator to require leadership role"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        if not (request.user.is_department_leader or request.user.is_superuser):
            return HttpResponseForbidden('You do not have permission to access this page.')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def department_leader_required(view_func):
    """Decorator to require department leader role"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        if not request.user.is_department_leader:
            return HttpResponseForbidden('Only department leaders can access this page.')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def staff_required(view_func):
    """Decorator to require staff status"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        if not request.user.is_staff:
            return HttpResponseForbidden('Staff access required.')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def admin_required(view_func):
    """Decorator to require admin/superuser status"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        if not request.user.is_superuser:
            return HttpResponseForbidden('Admin access required.')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper
