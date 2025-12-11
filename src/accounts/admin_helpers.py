"""
Admin helper utilities for customized admin interface
"""
from django.contrib import admin
from django.db.models import QuerySet
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count


class AdminColorMixin:
    """Mixin for colored admin status displays"""
    
    @staticmethod
    def get_status_badge(status, options=None):
        """
        Get colored badge for status
        
        Args:
            status: Status string
            options: Dict with status to color mapping
        
        Returns:
            HTML formatted badge
        """
        defaults = {
            'approved': '#28a745',  # green
            'pending': '#ffc107',   # yellow
            'rejected': '#dc3545',  # red
            'active': '#17a2b8',    # info
            'inactive': '#6c757d',  # gray
            'draft': '#ffc107',     # yellow
            'published': '#28a745', # green
            'archived': '#6c757d',  # gray
        }
        
        if options:
            defaults.update(options)
        
        color = defaults.get(status.lower(), '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; display: inline-block;">{}</span>',
            color,
            status
        )
    
    @staticmethod
    def get_approval_badge(is_approved):
        """Get approval status badge"""
        if is_approved:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; '
                'border-radius: 3px; display: inline-block;">✓ Approved</span>'
            )
        return format_html(
            '<span style="background-color: #ffc107; color: black; padding: 3px 8px; '
            'border-radius: 3px; display: inline-block;">⏳ Pending</span>'
        )


class AdminActionsMixin:
    """Mixin for common admin actions"""
    
    def make_approved(self, request, queryset):
        """Action to approve users"""
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} users approved')
    make_approved.short_description = 'Approve selected users'
    
    def make_pending(self, request, queryset):
        """Action to mark as pending"""
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} users marked as pending')
    make_pending.short_description = 'Mark selected as pending'
    
    def make_active(self, request, queryset):
        """Action to activate items"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} items activated')
    make_active.short_description = 'Activate selected items'
    
    def make_inactive(self, request, queryset):
        """Action to deactivate items"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} items deactivated')
    make_inactive.short_description = 'Deactivate selected items'
    
    def publish_items(self, request, queryset):
        """Action to publish items"""
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} items published')
    publish_items.short_description = 'Publish selected items'
    
    def unpublish_items(self, request, queryset):
        """Action to unpublish items"""
        updated = queryset.update(is_published=False)
        self.message_user(request, f'{updated} items unpublished')
    unpublish_items.short_description = 'Unpublish selected items'


class AdminFiltersMixin:
    """Mixin for custom admin filters"""
    
    @staticmethod
    def get_approval_filter():
        """Get approval status filter list"""
        return ('is_approved', 'is_active', 'is_published')
    
    @staticmethod
    def get_department_filter():
        """Get department filter list"""
        return ('department',)
    
    @staticmethod
    def get_date_filter():
        """Get date-based filter list"""
        return ('created_at', 'updated_at', 'date_joined')


class AdminSearchMixin:
    """Mixin for search configuration"""
    
    @staticmethod
    def get_user_search_fields():
        """Get search fields for users"""
        return ('full_name', 'email', 'reg_number', 'department__name')
    
    @staticmethod
    def get_content_search_fields():
        """Get search fields for content"""
        return ('title', 'description', 'content')


class AdminReadonlyMixin:
    """Mixin for readonly field management"""
    
    @staticmethod
    def get_timestamp_readonly():
        """Get readonly fields for timestamps"""
        return ('created_at', 'updated_at', 'date_joined')
    
    @staticmethod
    def get_audit_readonly():
        """Get readonly fields for audit info"""
        return ('created_at', 'updated_at', 'created_by', 'updated_by')


class InlineAdminHelper:
    """Helper for inline admin configuration"""
    
    @staticmethod
    def get_course_inline(extra=1):
        """Get course inline configuration"""
        class CourseInline(admin.TabularInline):
            model = None  # Will be set by subclass
            extra = extra
            fields = ('name', 'code', 'is_active')
            readonly_fields = ('created_at',)
        
        return CourseInline
    
    @staticmethod
    def get_project_inline(extra=1):
        """Get project inline configuration"""
        class ProjectInline(admin.TabularInline):
            model = None  # Will be set by subclass
            extra = extra
            fields = ('title', 'department', 'is_featured')
        
        return ProjectInline


class AdminListDisplayHelper:
    """Helper for configuring list_display"""
    
    @staticmethod
    def user_list_display():
        """Get list_display for users"""
        return ('full_name', 'email', 'reg_number', 'department', 
                'approval_status', 'picture_status', 'date_joined')
    
    @staticmethod
    def content_list_display():
        """Get list_display for content"""
        return ('title', 'department', 'publish_status', 'featured_status', 'created_at')
    
    @staticmethod
    def event_list_display():
        """Get list_display for events"""
        return ('title', 'event_date', 'location', 'department', 'attendees_count')


class AdminQuerysetHelper:
    """Helper for optimizing admin querysets"""
    
    @staticmethod
    def get_user_queryset(queryset: QuerySet) -> QuerySet:
        """Optimize user queryset with select_related"""
        return queryset.select_related(
            'department',
            'course'
        ).prefetch_related(
            'courses'
        )
    
    @staticmethod
    def get_content_queryset(queryset: QuerySet) -> QuerySet:
        """Optimize content queryset"""
        return queryset.select_related(
            'department',
            'created_by'
        ).annotate(
            comment_count=Count('comments')
        )


class AdminExportHelper:
    """Helper for exporting admin data"""
    
    @staticmethod
    def export_to_csv(queryset, fields):
        """
        Export queryset to CSV format
        
        Args:
            queryset: QuerySet to export
            fields: Fields to include
        
        Returns:
            CSV content as string
        """
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(fields)
        
        # Write data
        for obj in queryset:
            row = [getattr(obj, field, '') for field in fields]
            writer.writerow(row)
        
        return output.getvalue()
    
    @staticmethod
    def export_to_json(queryset, fields):
        """
        Export queryset to JSON format
        
        Args:
            queryset: QuerySet to export
            fields: Fields to include
        
        Returns:
            JSON content as string
        """
        import json
        
        data = []
        for obj in queryset:
            item = {field: str(getattr(obj, field, '')) for field in fields}
            data.append(item)
        
        return json.dumps(data, indent=2, default=str)
