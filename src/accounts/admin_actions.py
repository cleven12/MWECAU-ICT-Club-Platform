"""
Admin actions for bulk operations in Django admin
"""
from django.contrib import admin, messages
from django.db.models import Q


def make_approved(modeladmin, request, queryset):
    """Admin action to approve users"""
    updated = queryset.update(is_approved=True)
    modeladmin.message_user(
        request,
        f'{updated} users approved successfully.',
        messages.SUCCESS
    )
make_approved.short_description = 'Approve selected users'


def make_rejected(modeladmin, request, queryset):
    """Admin action to reject users"""
    deleted = queryset.delete()[0]
    modeladmin.message_user(
        request,
        f'{deleted} users rejected and deleted.',
        messages.SUCCESS
    )
make_rejected.short_description = 'Reject selected users'


def make_active(modeladmin, request, queryset):
    """Admin action to activate items"""
    updated = queryset.update(is_active=True)
    modeladmin.message_user(
        request,
        f'{updated} items activated successfully.',
        messages.SUCCESS
    )
make_active.short_description = 'Activate selected items'


def make_inactive(modeladmin, request, queryset):
    """Admin action to deactivate items"""
    updated = queryset.update(is_active=False)
    modeladmin.message_user(
        request,
        f'{updated} items deactivated successfully.',
        messages.SUCCESS
    )
make_inactive.short_description = 'Deactivate selected items'


def publish_items(modeladmin, request, queryset):
    """Admin action to publish items"""
    updated = queryset.update(is_published=True)
    modeladmin.message_user(
        request,
        f'{updated} items published successfully.',
        messages.SUCCESS
    )
publish_items.short_description = 'Publish selected items'


def unpublish_items(modeladmin, request, queryset):
    """Admin action to unpublish items"""
    updated = queryset.update(is_published=False)
    modeladmin.message_user(
        request,
        f'{updated} items unpublished successfully.',
        messages.SUCCESS
    )
unpublish_items.short_description = 'Unpublish selected items'


def mark_as_featured(modeladmin, request, queryset):
    """Admin action to mark items as featured"""
    updated = queryset.update(is_featured=True)
    modeladmin.message_user(
        request,
        f'{updated} items marked as featured.',
        messages.SUCCESS
    )
mark_as_featured.short_description = 'Mark selected as featured'


def unmark_as_featured(modeladmin, request, queryset):
    """Admin action to unmark items as featured"""
    updated = queryset.update(is_featured=False)
    modeladmin.message_user(
        request,
        f'{updated} items unmarked as featured.',
        messages.SUCCESS
    )
unmark_as_featured.short_description = 'Unmark selected as featured'
