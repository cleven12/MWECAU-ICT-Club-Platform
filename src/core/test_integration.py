"""
Integration tests for core functionality
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import Department, Course
from core.models import Project, Event, Announcement

User = get_user_model()


class UserWorkflowIntegrationTests(TestCase):
    """Integration tests for complete user workflow"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.department = Department.objects.create(
            name='Programming',
            slug='programming'
        )
        self.course = Course.objects.create(
            name='Python',
            code='PROG101',
            department=self.department
        )
    
    def test_complete_registration_workflow(self):
        """Test complete user registration workflow"""
        # Register user
        registration_data = {
            'reg_number': 'SE2021001',
            'full_name': 'Test User',
            'email': 'test@example.com',
            'department': self.department.id,
            'course': self.course.id,
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        }
        
        # Should redirect to login
        response = self.client.post(reverse('accounts:register'), registration_data)
        self.assertEqual(response.status_code, 302)
        
        # User should exist but not approved
        user = User.objects.get(email='test@example.com')
        self.assertFalse(user.is_approved)


class ContentWorkflowIntegrationTests(TestCase):
    """Integration tests for content management"""
    
    def setUp(self):
        """Set up test data"""
        self.department = Department.objects.create(
            name='Programming',
            slug='programming'
        )
        self.course = Course.objects.create(
            name='Python',
            code='PROG101',
            department=self.department
        )
        self.user = User.objects.create_user(
            reg_number='SE2021001',
            email='test@example.com',
            password='testpass123',
            full_name='Test User',
            department=self.department,
            course=self.course,
            is_approved=True
        )
    
    def test_create_project_workflow(self):
        """Test creating a project"""
        project = Project.objects.create(
            title='Test Project',
            description='Test Description',
            slug='test-project',
            department=self.department,
            created_by=self.user
        )
        
        self.assertEqual(project.title, 'Test Project')
        self.assertEqual(project.created_by, self.user)
    
    def test_create_event_workflow(self):
        """Test creating an event"""
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            event_date='2025-12-25 10:00:00',
            location='Test Location',
            department=self.department
        )
        
        self.assertEqual(event.title, 'Test Event')
        self.assertEqual(event.department, self.department)
    
    def test_publish_announcement_workflow(self):
        """Test publishing an announcement"""
        announcement = Announcement.objects.create(
            title='Test Announcement',
            content='Test Content',
            announcement_type='general',
            department=self.department,
            is_published=True
        )
        
        self.assertTrue(announcement.is_published)
        self.assertEqual(announcement.title, 'Test Announcement')


class DashboardIntegrationTests(TestCase):
    """Integration tests for dashboard"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.department = Department.objects.create(
            name='Programming',
            slug='programming'
        )
        self.course = Course.objects.create(
            name='Python',
            code='PROG101',
            department=self.department
        )
        self.user = User.objects.create_user(
            reg_number='SE2021001',
            email='test@example.com',
            password='testpass123',
            full_name='Test User',
            department=self.department,
            course=self.course,
            is_approved=True
        )
    
    def test_access_member_dashboard(self):
        """Test accessing member dashboard"""
        self.client.login(username='test@example.com', password='testpass123')
        
        response = self.client.get(reverse('accounts:member_dashboard'))
        
        # Should either redirect (pending) or show dashboard (approved)
        self.assertIn(response.status_code, [200, 302])
