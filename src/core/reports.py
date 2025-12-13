"""
Reporting and statistics utilities
"""
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
import json


class UserReports:
    """Generate user-related reports"""
    
    @staticmethod
    def get_user_statistics():
        """Get overall user statistics"""
        from accounts.models import CustomUser
        
        total_users = CustomUser.objects.count()
        approved_users = CustomUser.objects.filter(is_approved=True).count()
        pending_users = CustomUser.objects.filter(is_approved=False).count()
        active_users = CustomUser.objects.filter(is_active=True).count()
        
        return {
            'total_users': total_users,
            'approved_users': approved_users,
            'pending_users': pending_users,
            'active_users': active_users,
            'approval_rate': (approved_users / total_users * 100) if total_users > 0 else 0,
        }
    
    @staticmethod
    def get_department_statistics():
        """Get statistics by department"""
        from accounts.models import CustomUser, Department
        
        stats = []
        for dept in Department.objects.all():
            total = CustomUser.objects.filter(department=dept).count()
            approved = CustomUser.objects.filter(
                department=dept,
                is_approved=True
            ).count()
            
            stats.append({
                'department': dept.name,
                'total_users': total,
                'approved_users': approved,
                'approval_rate': (approved / total * 100) if total > 0 else 0,
            })
        
        return stats
    
    @staticmethod
    def get_registration_statistics():
        """Get registration statistics"""
        from accounts.models import CustomUser
        
        now = timezone.now()
        last_7_days = CustomUser.objects.filter(
            date_joined__gte=now - timedelta(days=7)
        ).count()
        
        last_30_days = CustomUser.objects.filter(
            date_joined__gte=now - timedelta(days=30)
        ).count()
        
        return {
            'last_7_days': last_7_days,
            'last_30_days': last_30_days,
            'average_daily': last_7_days / 7 if last_7_days > 0 else 0,
        }


class ContentReports:
    """Generate content-related reports"""
    
    @staticmethod
    def get_project_statistics():
        """Get project statistics"""
        from core.models import Project
        
        total = Project.objects.count()
        featured = Project.objects.filter(is_featured=True).count()
        
        return {
            'total_projects': total,
            'featured_projects': featured,
            'average_projects_per_dept': total / Project.objects.values('department').distinct().count() if total > 0 else 0,
        }
    
    @staticmethod
    def get_event_statistics():
        """Get event statistics"""
        from core.models import Event
        from django.utils import timezone
        
        now = timezone.now()
        total = Event.objects.count()
        upcoming = Event.objects.filter(event_date__gte=now).count()
        past = Event.objects.filter(event_date__lt=now).count()
        
        return {
            'total_events': total,
            'upcoming_events': upcoming,
            'past_events': past,
        }
    
    @staticmethod
    def get_announcement_statistics():
        """Get announcement statistics"""
        from core.models import Announcement
        
        total = Announcement.objects.count()
        published = Announcement.objects.filter(is_published=True).count()
        draft = Announcement.objects.filter(is_published=False).count()
        
        return {
            'total_announcements': total,
            'published_announcements': published,
            'draft_announcements': draft,
        }


class EngagementReports:
    """Generate user engagement reports"""
    
    @staticmethod
    def get_active_users_report():
        """Get active users in last 30 days"""
        from accounts.models import CustomUser
        from django.contrib.sessions.models import Session
        
        now = timezone.now()
        active_sessions = Session.objects.filter(
            expire_date__gte=now
        ).count()
        
        return {
            'active_sessions': active_sessions,
        }
    
    @staticmethod
    def get_engagement_by_department():
        """Get engagement metrics by department"""
        from accounts.models import CustomUser, Department
        from core.models import Project, Event
        
        stats = []
        for dept in Department.objects.all():
            members = CustomUser.objects.filter(department=dept).count()
            projects = Project.objects.filter(department=dept).count()
            events = Event.objects.filter(department=dept).count()
            
            stats.append({
                'department': dept.name,
                'members': members,
                'projects': projects,
                'events': events,
            })
        
        return stats


class ReportExporter:
    """Export reports in various formats"""
    
    @staticmethod
    def export_to_json(data):
        """Export report data to JSON"""
        return json.dumps(data, indent=2, default=str)
    
    @staticmethod
    def export_to_csv(data, headers):
        """Export report data to CSV"""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        
        if isinstance(data, list):
            writer.writerows(data)
        else:
            writer.writerow(data)
        
        return output.getvalue()
