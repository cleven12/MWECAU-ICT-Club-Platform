"""
Search and filtering utilities for enhanced querysets
"""
from django.db.models import Q, F
from django.core.paginator import Paginator


class SearchHelper:
    """Helper for searching models"""
    
    @staticmethod
    def search_users(query):
        """Search users by name, email, or registration number"""
        from accounts.models import CustomUser
        
        return CustomUser.objects.filter(
            Q(full_name__icontains=query) |
            Q(email__icontains=query) |
            Q(reg_number__icontains=query)
        )
    
    @staticmethod
    def search_projects(query):
        """Search projects by title or description"""
        from core.models import Project
        
        return Project.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    
    @staticmethod
    def search_announcements(query):
        """Search announcements"""
        from core.models import Announcement
        
        return Announcement.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )


class FilterHelper:
    """Helper for filtering querysets"""
    
    @staticmethod
    def filter_by_department(queryset, department_id):
        """Filter by department"""
        return queryset.filter(department_id=department_id)
    
    @staticmethod
    def filter_by_status(queryset, status):
        """Filter by status"""
        if status == 'active':
            return queryset.filter(is_active=True)
        elif status == 'inactive':
            return queryset.filter(is_active=False)
        return queryset
    
    @staticmethod
    def filter_by_approval(queryset, approved=True):
        """Filter by approval status"""
        return queryset.filter(is_approved=approved)
    
    @staticmethod
    def filter_published(queryset):
        """Filter published items"""
        return queryset.filter(is_published=True)
    
    @staticmethod
    def filter_featured(queryset):
        """Filter featured items"""
        return queryset.filter(is_featured=True)


class SortHelper:
    """Helper for sorting querysets"""
    
    @staticmethod
    def sort_by_date(queryset, field='created_at', ascending=False):
        """Sort by date"""
        order = field if ascending else f'-{field}'
        return queryset.order_by(order)
    
    @staticmethod
    def sort_by_name(queryset, field='name', ascending=True):
        """Sort by name"""
        order = field if ascending else f'-{field}'
        return queryset.order_by(order)
    
    @staticmethod
    def sort_by_popularity(queryset):
        """Sort by popularity (comment count)"""
        from django.db.models import Count
        return queryset.annotate(comment_count=Count('comments')).order_by('-comment_count')


class PaginationHelper:
    """Helper for pagination"""
    
    @staticmethod
    def paginate(queryset, page=1, per_page=20):
        """Paginate queryset"""
        paginator = Paginator(queryset, per_page)
        
        try:
            page_obj = paginator.page(page)
        except:
            page_obj = paginator.page(1)
        
        return page_obj
    
    @staticmethod
    def get_pagination_context(queryset, page, per_page=20):
        """Get pagination context for templates"""
        page_obj = PaginationHelper.paginate(queryset, page, per_page)
        
        return {
            'page_obj': page_obj,
            'paginator': page_obj.paginator,
            'is_paginated': page_obj.has_other_pages(),
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
        }


class QueryOptimizer:
    """Helper for optimizing queries"""
    
    @staticmethod
    def optimize_user_queryset(queryset):
        """Optimize user queryset with select_related and prefetch_related"""
        return queryset.select_related(
            'department',
            'course'
        ).prefetch_related(
            'courses',
            'projects',
            'events'
        )
    
    @staticmethod
    def optimize_project_queryset(queryset):
        """Optimize project queryset"""
        return queryset.select_related(
            'department',
            'created_by'
        ).prefetch_related(
            'comments'
        )
    
    @staticmethod
    def optimize_event_queryset(queryset):
        """Optimize event queryset"""
        return queryset.select_related(
            'department'
        ).prefetch_related(
            'attendees'
        )
