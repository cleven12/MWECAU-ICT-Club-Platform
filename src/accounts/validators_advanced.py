"""
Data validation utilities and helpers
"""
import re
from django.core.exceptions import ValidationError


class DataValidator:
    """Validate various data types"""
    
    @staticmethod
    def is_valid_email(email):
        """Validate email address"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def is_valid_phone(phone):
        """Validate phone number"""
        pattern = r'^[\d\s\-\+\(\)]+$'
        return re.match(pattern, phone) is not None and len(phone) >= 10
    
    @staticmethod
    def is_valid_url(url):
        """Validate URL"""
        pattern = r'^https?:\/\/.+\..+$'
        return re.match(pattern, url) is not None
    
    @staticmethod
    def is_valid_registration_number(reg_number):
        """Validate registration number format"""
        pattern = r'^[A-Z]{2}\d{4}\d{3}$'
        return re.match(pattern, reg_number) is not None
    
    @staticmethod
    def is_strong_password(password):
        """Check if password is strong"""
        if len(password) < 8:
            return False
        
        has_upper = re.search(r'[A-Z]', password)
        has_lower = re.search(r'[a-z]', password)
        has_digit = re.search(r'\d', password)
        has_special = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
        
        return bool(has_upper and has_lower and has_digit and has_special)
    
    @staticmethod
    def validate_file_size(file, max_size_mb=5):
        """Validate file size"""
        if file.size > max_size_mb * 1024 * 1024:
            raise ValidationError(f'File size must not exceed {max_size_mb}MB')
        return True
    
    @staticmethod
    def validate_file_extension(filename, allowed_extensions):
        """Validate file extension"""
        ext = filename.split('.')[-1].lower()
        if ext not in allowed_extensions:
            raise ValidationError(f'File type .{ext} is not allowed')
        return True
    
    @staticmethod
    def validate_image_file(file):
        """Validate image file"""
        from PIL import Image
        
        try:
            Image.open(file)
            return True
        except:
            raise ValidationError('Invalid image file')


class SanitizeHelper:
    """Sanitize user input"""
    
    @staticmethod
    def sanitize_text(text):
        """Remove potentially harmful characters"""
        # Remove common XSS patterns
        dangerous_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'<iframe[^>]*>.*?</iframe>',
        ]
        
        result = text
        for pattern in dangerous_patterns:
            result = re.sub(pattern, '', result, flags=re.IGNORECASE)
        
        return result.strip()
    
    @staticmethod
    def sanitize_url(url):
        """Sanitize URL"""
        # Remove potentially harmful protocols
        dangerous_protocols = ['javascript:', 'data:', 'vbscript:']
        
        for protocol in dangerous_protocols:
            if url.lower().startswith(protocol):
                return ''
        
        return url
    
    @staticmethod
    def sanitize_html(html):
        """Sanitize HTML content"""
        from bleach import clean
        
        allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'a', 'h1', 'h2', 'h3', 'ul', 'ol', 'li']
        allowed_attributes = {'a': ['href', 'title']}
        
        return clean(html, tags=allowed_tags, attributes=allowed_attributes)


class DataNormalizer:
    """Normalize data formats"""
    
    @staticmethod
    def normalize_phone(phone):
        """Normalize phone number format"""
        # Remove spaces, dashes, and parentheses
        normalized = re.sub(r'[\s\-\(\)]', '', phone)
        # Remove + prefix if present
        if normalized.startswith('+'):
            normalized = normalized[1:]
        return normalized
    
    @staticmethod
    def normalize_email(email):
        """Normalize email to lowercase"""
        return email.lower().strip()
    
    @staticmethod
    def normalize_name(name):
        """Normalize name (title case)"""
        return ' '.join(word.capitalize() for word in name.split())
    
    @staticmethod
    def normalize_slug(text):
        """Create URL-safe slug from text"""
        import re
        text = text.lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text.strip('-')
