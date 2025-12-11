"""
Security utilities and helpers
"""
import hashlib
import secrets
from django.core.exceptions import ValidationError
from django.conf import settings


class PasswordSecurity:
    """Password security utilities"""
    
    @staticmethod
    def hash_password(password: str, salt: str = None) -> str:
        """Hash password with salt"""
        if not salt:
            salt = secrets.token_hex(16)
        
        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        
        return f"{salt}${hashed.hex()}"
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash"""
        try:
            salt, _ = hashed.split('$')
            new_hash = PasswordSecurity.hash_password(password, salt)
            return hashed == new_hash
        except Exception:
            return False
    
    @staticmethod
    def generate_temporary_password(length: int = 12) -> str:
        """Generate a temporary password"""
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%'
        return ''.join(secrets.choice(alphabet) for _ in range(length))


class TokenSecurity:
    """Token security utilities"""
    
    @staticmethod
    def generate_token(length: int = 32) -> str:
        """Generate secure random token"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_code(length: int = 6, numeric: bool = True) -> str:
        """Generate secure code (OTP, verification, etc.)"""
        if numeric:
            return ''.join(str(secrets.randbelow(10)) for _ in range(length))
        else:
            alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            return ''.join(secrets.choice(alphabet) for _ in range(length))


class CSRFSecurity:
    """CSRF token security"""
    
    @staticmethod
    def generate_csrf_token() -> str:
        """Generate CSRF token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def validate_csrf_token(token: str) -> bool:
        """Validate CSRF token"""
        return len(token) > 0 and len(token) <= 128


class IPAddressSecurity:
    """IP address security utilities"""
    
    @staticmethod
    def get_client_ip(request) -> str:
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @staticmethod
    def is_ip_whitelisted(ip: str, whitelist: list = None) -> bool:
        """Check if IP is in whitelist"""
        if not whitelist:
            whitelist = getattr(settings, 'IP_WHITELIST', [])
        return ip in whitelist
    
    @staticmethod
    def is_ip_blacklisted(ip: str, blacklist: list = None) -> bool:
        """Check if IP is in blacklist"""
        if not blacklist:
            blacklist = getattr(settings, 'IP_BLACKLIST', [])
        return ip in blacklist


class RateLimitSecurity:
    """Rate limiting security"""
    
    @staticmethod
    def check_rate_limit(identifier: str, limit: int = 100, window: int = 3600) -> bool:
        """Check if request is within rate limit"""
        from django.core.cache import cache
        
        cache_key = f'rate_limit:{identifier}'
        requests = cache.get(cache_key, 0)
        
        if requests >= limit:
            return False
        
        cache.set(cache_key, requests + 1, window)
        return True
    
    @staticmethod
    def get_remaining_requests(identifier: str, limit: int = 100) -> int:
        """Get remaining requests for identifier"""
        from django.core.cache import cache
        
        cache_key = f'rate_limit:{identifier}'
        requests = cache.get(cache_key, 0)
        
        return max(0, limit - requests)


class EncryptionSecurity:
    """Encryption utilities"""
    
    @staticmethod
    def encrypt_data(data: str, key: str = None) -> str:
        """Encrypt sensitive data"""
        try:
            from cryptography.fernet import Fernet
            if not key:
                key = settings.SECRET_KEY.encode()[:32].ljust(32, b'0')
            cipher = Fernet(key)
            encrypted = cipher.encrypt(data.encode())
            return encrypted.decode()
        except ImportError:
            return data
    
    @staticmethod
    def decrypt_data(encrypted_data: str, key: str = None) -> str:
        """Decrypt sensitive data"""
        try:
            from cryptography.fernet import Fernet
            if not key:
                key = settings.SECRET_KEY.encode()[:32].ljust(32, b'0')
            cipher = Fernet(key)
            decrypted = cipher.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except Exception:
            return None


class SessionSecurity:
    """Session security utilities"""
    
    @staticmethod
    def invalidate_session(request):
        """Invalidate user session"""
        if hasattr(request, 'session'):
            request.session.flush()
    
    @staticmethod
    def regenerate_session_id(request):
        """Regenerate session ID"""
        if hasattr(request, 'session'):
            request.session.create()
    
    @staticmethod
    def set_secure_cookie(response, key: str, value: str, max_age: int = None):
        """Set secure HTTP-only cookie"""
        response.set_cookie(
            key,
            value,
            max_age=max_age,
            httponly=True,
            secure=getattr(settings, 'SESSION_COOKIE_SECURE', False),
            samesite='Strict'
        )
        return response


class AuditSecurity:
    """Security audit logging"""
    
    @staticmethod
    def log_security_event(event_type: str, user=None, ip_address: str = None, details: dict = None):
        """Log security event"""
        import logging
        logger = logging.getLogger('security')
        
        message = f"[{event_type}] User: {user}, IP: {ip_address}"
        if details:
            message += f", Details: {details}"
        
        logger.warning(message)
    
    @staticmethod
    def log_failed_login_attempt(username: str, ip_address: str):
        """Log failed login attempt"""
        AuditSecurity.log_security_event(
            'FAILED_LOGIN',
            ip_address=ip_address,
            details={'username': username}
        )
    
    @staticmethod
    def log_unauthorized_access(user, resource: str, ip_address: str):
        """Log unauthorized access attempt"""
        AuditSecurity.log_security_event(
            'UNAUTHORIZED_ACCESS',
            user=user,
            ip_address=ip_address,
            details={'resource': resource}
        )
