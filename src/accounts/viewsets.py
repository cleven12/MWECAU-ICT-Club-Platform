"""
Django REST Framework viewsets for API endpoints
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from accounts.models import CustomUser, Department, Course
from core.models import Project, Event, Announcement, ContactMessage
from membership.models import MembershipPayment
from accounts.serializers import (
    CustomUserSerializer, DepartmentSerializer, CourseSerializer,
    ProjectSerializer, EventSerializer, AnnouncementSerializer,
    ContactMessageSerializer, MembershipPaymentSerializer
)


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Department model"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Course model"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department']
    search_fields = ['name', 'code']


class CustomUserViewSet(viewsets.ModelViewSet):
    """ViewSet for CustomUser model"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'is_approved', 'is_active']
    search_fields = ['full_name', 'reg_number', 'email']
    ordering_fields = ['registered_at', 'full_name']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=user.id)
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        """Approve user membership"""
        user = self.get_object()
        user.is_approved = True
        user.save()
        return Response({'status': 'user approved'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        """Reject user membership"""
        user = self.get_object()
        user.is_approved = False
        user.save()
        return Response({'status': 'user rejected'})


class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet for Project model"""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'featured']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and self.request.user.is_department_leader:
            return queryset.filter(department=self.request.user.department)
        return queryset
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured projects"""
        featured_projects = Project.objects.filter(featured=True)
        serializer = self.get_serializer(featured_projects, many=True)
        return Response(serializer.data)


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Event model"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['event_date', 'created_at']
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming events"""
        from core.managers import EventQuerySet
        qs = EventQuerySet(Event, using=Event.objects.db)
        upcoming = qs.upcoming()
        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)


class AnnouncementViewSet(viewsets.ModelViewSet):
    """ViewSet for Announcement model"""
    queryset = Announcement.objects.filter(is_published=True)
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['announcement_type', 'department']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at']
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent announcements"""
        recent_announcements = Announcement.objects.filter(is_published=True).order_by('-created_at')[:10]
        serializer = self.get_serializer(recent_announcements, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def urgent(self, request):
        """Get urgent announcements"""
        urgent_announcements = Announcement.objects.filter(
            is_published=True,
            announcement_type='urgent'
        ).order_by('-created_at')
        serializer = self.get_serializer(urgent_announcements, many=True)
        return Response(serializer.data)


class ContactMessageViewSet(viewsets.ModelViewSet):
    """ViewSet for ContactMessage model"""
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'subject']
    ordering_fields = ['created_at']
    
    @action(detail=True, methods=['post'])
    def mark_responded(self, request, pk=None):
        """Mark contact message as responded"""
        message = self.get_object()
        message.is_responded = True
        message.save()
        return Response({'status': 'marked as responded'})


class MembershipPaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for MembershipPayment model"""
    queryset = MembershipPayment.objects.all()
    serializer_class = MembershipPaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'provider']
    ordering_fields = ['created_at', 'amount']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return MembershipPayment.objects.all()
        return MembershipPayment.objects.filter(user=user)
    
    @action(detail=False, methods=['get'])
    def my_payments(self, request):
        """Get current user's payments"""
        payments = MembershipPayment.objects.filter(user=request.user).order_by('-created_at')
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def confirm_payment(self, request, pk=None):
        """Confirm payment by admin"""
        payment = self.get_object()
        payment.status = 'success'
        payment.save()
        return Response({'status': 'payment confirmed'})
