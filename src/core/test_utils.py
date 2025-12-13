"""
Test cases for core app utilities and helpers
"""
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from core.utils import (
    get_time_remaining,
    is_within_deadline,
    format_time_remaining,
    get_user_status_badge,
)


class UtilityFunctionTests(TestCase):
    """Test utility functions"""
    
    def test_get_time_remaining(self):
        """Test time remaining calculation"""
        future = timezone.now() + timedelta(hours=5)
        remaining = get_time_remaining(future)
        self.assertGreater(remaining, timedelta(hours=4))
    
    def test_is_within_deadline(self):
        """Test deadline check"""
        future = timezone.now() + timedelta(hours=1)
        self.assertTrue(is_within_deadline(future))
        
        past = timezone.now() - timedelta(hours=1)
        self.assertFalse(is_within_deadline(past))
    
    def test_format_time_remaining(self):
        """Test time formatting"""
        future = timezone.now() + timedelta(days=2, hours=5)
        formatted = format_time_remaining(future)
        self.assertIn('day', formatted.lower())


class StatusBadgeTests(TestCase):
    """Test status badge generation"""
    
    def test_user_status_badge_pending(self):
        """Test pending user status badge"""
        badge = get_user_status_badge('pending')
        self.assertIn('badge', badge.lower() if isinstance(badge, str) else str(badge))
    
    def test_user_status_badge_approved(self):
        """Test approved user status badge"""
        badge = get_user_status_badge('approved')
        self.assertIsNotNone(badge)
    
    def test_user_status_badge_active(self):
        """Test active user status badge"""
        badge = get_user_status_badge('active')
        self.assertIsNotNone(badge)


class PaymentStatusTests(TestCase):
    """Test payment status utilities"""
    
    def test_payment_status_pending(self):
        """Test pending payment status"""
        from core.utils import get_payment_status_badge
        badge = get_payment_status_badge('pending')
        self.assertIsNotNone(badge)
    
    def test_payment_status_completed(self):
        """Test completed payment status"""
        from core.utils import get_payment_status_badge
        badge = get_payment_status_badge('completed')
        self.assertIsNotNone(badge)
