"""
Testing utilities and fixtures
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from accounts.models import Department, Course

User = get_user_model()


class BaseTestCase(TestCase):
    """Base test case with common setup"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = Client()
        self.create_test_departments()
        self.create_test_courses()
        self.create_test_users()
    
    def create_test_departments(self):
        """Create test departments"""
        self.dept_programming = Department.objects.create(
            name='Programming',
            slug='programming',
            description='Programming Department'
        )
        self.dept_cybersecurity = Department.objects.create(
            name='Cybersecurity',
            slug='cybersecurity',
            description='Cybersecurity Department'
        )
    
    def create_test_courses(self):
        """Create test courses"""
        self.course_python = Course.objects.create(
            name='Python Programming',
            code='PROG101',
            department=self.dept_programming
        )
        self.course_web = Course.objects.create(
            name='Web Development',
            code='PROG102',
            department=self.dept_programming
        )
    
    def create_test_users(self):
        """Create test users"""
        self.user_student = User.objects.create_user(
            reg_number='SE2021001',
            email='student@example.com',
            password='testpass123',
            full_name='John Student',
            department=self.dept_programming,
            course=self.course_python,
            is_approved=True
        )
        
        self.user_pending = User.objects.create_user(
            reg_number='SE2021002',
            email='pending@example.com',
            password='testpass123',
            full_name='Jane Pending',
            department=self.dept_programming,
            course=self.course_python,
            is_approved=False
        )
        
        self.user_leader = User.objects.create_user(
            reg_number='SE2021003',
            email='leader@example.com',
            password='testpass123',
            full_name='Bob Leader',
            department=self.dept_programming,
            course=self.course_python,
            is_approved=True,
            is_department_leader=True
        )
        
        self.user_admin = User.objects.create_superuser(
            reg_number='SE2021004',
            email='admin@example.com',
            password='testpass123',
            full_name='Admin User',
            department=self.dept_programming,
            course=self.course_python
        )


class ViewTestMixin:
    """Mixin for view testing"""
    
    def login(self, user=None):
        """Login user"""
        if user is None:
            user = self.user_student
        
        self.client.login(
            username=user.reg_number,
            email=user.email,
            password='testpass123'
        )
    
    def assert_redirect(self, response, expected_url):
        """Assert redirect to expected URL"""
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_url)
    
    def assert_template_used(self, response, template_name):
        """Assert template was used"""
        self.assertTemplateUsed(response, template_name)
    
    def assert_context_contains(self, response, *keys):
        """Assert response context contains keys"""
        for key in keys:
            self.assertIn(key, response.context)


class APITestMixin:
    """Mixin for API testing"""
    
    def get_auth_headers(self, user=None):
        """Get authorization headers for API"""
        from rest_framework.authtoken.models import Token
        
        if user is None:
            user = self.user_student
        
        token, _ = Token.objects.get_or_create(user=user)
        return {
            'HTTP_AUTHORIZATION': f'Bearer {token.key}'
        }
    
    def assert_json_response(self, response, status_code=200):
        """Assert response is JSON with expected status"""
        self.assertEqual(response.status_code, status_code)
        self.assertEqual(response['Content-Type'], 'application/json')
    
    def assert_json_contains(self, response, *keys):
        """Assert JSON response contains keys"""
        data = response.json()
        for key in keys:
            self.assertIn(key, data)


class FormTestMixin:
    """Mixin for form testing"""
    
    def assert_form_error(self, form, field, message):
        """Assert form has error for field"""
        self.assertIn(field, form.errors)
        self.assertIn(message, str(form.errors[field]))
    
    def assert_form_valid(self, form):
        """Assert form is valid"""
        self.assertTrue(form.is_valid(), msg=str(form.errors))
    
    def assert_form_invalid(self, form):
        """Assert form is invalid"""
        self.assertFalse(form.is_valid())


class FactoryMixin:
    """Mixin for factory methods"""
    
    def create_project(self, **kwargs):
        """Create a test project"""
        from core.models import Project
        
        defaults = {
            'title': 'Test Project',
            'description': 'Test Description',
            'slug': 'test-project',
            'department': self.dept_programming,
            'created_by': self.user_student,
        }
        defaults.update(kwargs)
        
        return Project.objects.create(**defaults)
    
    def create_event(self, **kwargs):
        """Create a test event"""
        from core.models import Event
        from django.utils import timezone
        
        defaults = {
            'title': 'Test Event',
            'description': 'Test Description',
            'event_date': timezone.now() + timezone.timedelta(days=1),
            'location': 'Test Location',
            'department': self.dept_programming,
        }
        defaults.update(kwargs)
        
        return Event.objects.create(**defaults)
    
    def create_announcement(self, **kwargs):
        """Create a test announcement"""
        from core.models import Announcement
        
        defaults = {
            'title': 'Test Announcement',
            'content': 'Test Content',
            'announcement_type': 'general',
            'department': self.dept_programming,
            'is_published': True,
        }
        defaults.update(kwargs)
        
        return Announcement.objects.create(**defaults)
