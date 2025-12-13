"""
Custom Django admin filters
"""
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _


class ApprovalStatusFilter(SimpleListFilter):
    """Filter by approval status"""
    title = _('Approval Status')
    parameter_name = 'approval'
    
    def lookups(self, request, model_admin):
        return (
            ('approved', _('Approved')),
            ('pending', _('Pending')),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'approved':
            return queryset.filter(is_approved=True)
        elif self.value() == 'pending':
            return queryset.filter(is_approved=False)


class ActiveStatusFilter(SimpleListFilter):
    """Filter by active status"""
    title = _('Active Status')
    parameter_name = 'active'
    
    def lookups(self, request, model_admin):
        return (
            ('active', _('Active')),
            ('inactive', _('Inactive')),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(is_active=True)
        elif self.value() == 'inactive':
            return queryset.filter(is_active=False)


class PublishStatusFilter(SimpleListFilter):
    """Filter by publish status"""
    title = _('Publish Status')
    parameter_name = 'published'
    
    def lookups(self, request, model_admin):
        return (
            ('published', _('Published')),
            ('draft', _('Draft')),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'published':
            return queryset.filter(is_published=True)
        elif self.value() == 'draft':
            return queryset.filter(is_published=False)


class FeaturedStatusFilter(SimpleListFilter):
    """Filter by featured status"""
    title = _('Featured Status')
    parameter_name = 'featured'
    
    def lookups(self, request, model_admin):
        return (
            ('featured', _('Featured')),
            ('not_featured', _('Not Featured')),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'featured':
            return queryset.filter(is_featured=True)
        elif self.value() == 'not_featured':
            return queryset.filter(is_featured=False)


class DateRangeFilter(SimpleListFilter):
    """Filter by date range"""
    title = _('Date Range')
    parameter_name = 'date_range'
    
    def lookups(self, request, model_admin):
        return (
            ('today', _('Today')),
            ('this_week', _('This Week')),
            ('this_month', _('This Month')),
            ('this_year', _('This Year')),
        )
    
    def queryset(self, request, queryset):
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        
        if self.value() == 'today':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            return queryset.filter(created_at__gte=start_date)
        
        elif self.value() == 'this_week':
            start_date = now - timedelta(days=now.weekday())
            return queryset.filter(created_at__gte=start_date)
        
        elif self.value() == 'this_month':
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            return queryset.filter(created_at__gte=start_date)
        
        elif self.value() == 'this_year':
            start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            return queryset.filter(created_at__gte=start_date)


class DepartmentFilter(SimpleListFilter):
    """Filter by department"""
    title = _('Department')
    parameter_name = 'department'
    
    def lookups(self, request, model_admin):
        from accounts.models import Department
        
        departments = Department.objects.all()
        return [(dept.id, dept.name) for dept in departments]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(department__id=self.value())
