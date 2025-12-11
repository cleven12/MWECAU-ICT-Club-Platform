"""
API URL routing configuration for DRF
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.viewsets import (
    DepartmentViewSet, CourseViewSet, CustomUserViewSet,
    ProjectViewSet, EventViewSet, AnnouncementViewSet,
    ContactMessageViewSet, MembershipPaymentViewSet
)

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='api-department')
router.register(r'courses', CourseViewSet, basename='api-course')
router.register(r'users', CustomUserViewSet, basename='api-user')
router.register(r'projects', ProjectViewSet, basename='api-project')
router.register(r'events', EventViewSet, basename='api-event')
router.register(r'announcements', AnnouncementViewSet, basename='api-announcement')
router.register(r'contact-messages', ContactMessageViewSet, basename='api-contact-message')
router.register(r'payments', MembershipPaymentViewSet, basename='api-payment')

# The API URLs are determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]

"""
API Endpoints documentation:

Departments:
  GET    /api/departments/               - List all departments
  GET    /api/departments/{id}/          - Get department details
  POST   /api/departments/               - Create department (admin only)
  PUT    /api/departments/{id}/          - Update department (admin only)
  DELETE /api/departments/{id}/          - Delete department (admin only)

Courses:
  GET    /api/courses/                   - List all courses
  GET    /api/courses/{id}/              - Get course details
  POST   /api/courses/                   - Create course (admin only)
  PUT    /api/courses/{id}/              - Update course (admin only)
  DELETE /api/courses/{id}/              - Delete course (admin only)

Users:
  GET    /api/users/                     - List all users (staff only)
  GET    /api/users/{id}/                - Get user details
  GET    /api/users/profile/             - Get current user profile
  POST   /api/users/                     - Create user (staff only)
  PUT    /api/users/{id}/                - Update user
  DELETE /api/users/{id}/                - Delete user (staff only)
  POST   /api/users/{id}/approve/        - Approve user (admin only)
  POST   /api/users/{id}/reject/         - Reject user (admin only)

Projects:
  GET    /api/projects/                  - List all projects
  GET    /api/projects/{id}/             - Get project details
  GET    /api/projects/featured/         - Get featured projects
  POST   /api/projects/                  - Create project
  PUT    /api/projects/{id}/             - Update project
  DELETE /api/projects/{id}/             - Delete project

Events:
  GET    /api/events/                    - List all events
  GET    /api/events/{id}/               - Get event details
  GET    /api/events/upcoming/           - Get upcoming events
  POST   /api/events/                    - Create event (staff only)
  PUT    /api/events/{id}/               - Update event (staff only)
  DELETE /api/events/{id}/               - Delete event (staff only)

Announcements:
  GET    /api/announcements/             - List published announcements
  GET    /api/announcements/{id}/        - Get announcement details
  GET    /api/announcements/recent/      - Get recent announcements
  GET    /api/announcements/urgent/      - Get urgent announcements
  POST   /api/announcements/             - Create announcement (staff only)
  PUT    /api/announcements/{id}/        - Update announcement (staff only)
  DELETE /api/announcements/{id}/        - Delete announcement (staff only)

Contact Messages:
  GET    /api/contact-messages/          - List contact messages (admin only)
  GET    /api/contact-messages/{id}/     - Get message details (admin only)
  POST   /api/contact-messages/{id}/mark_responded/ - Mark as responded (admin only)

Payments:
  GET    /api/payments/                  - List payments
  GET    /api/payments/{id}/             - Get payment details
  GET    /api/payments/my_payments/      - Get current user's payments
  POST   /api/payments/                  - Create payment
  POST   /api/payments/{id}/confirm_payment/ - Confirm payment (admin only)
"""
