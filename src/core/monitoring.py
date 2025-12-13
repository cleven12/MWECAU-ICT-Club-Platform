"""
Application monitoring and health check utilities
"""
import logging
from django.db import connection
from django.core.cache import cache
from django.utils import timezone
import time

logger = logging.getLogger(__name__)


class HealthCheck:
    """Application health checks"""
    
    @staticmethod
    def check_database():
        """Check database connectivity"""
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
            return {
                'status': 'healthy',
                'message': 'Database connection successful'
            }
        except Exception as e:
            logger.error(f'Database health check failed: {str(e)}')
            return {
                'status': 'unhealthy',
                'message': f'Database error: {str(e)}'
            }
    
    @staticmethod
    def check_cache():
        """Check cache connectivity"""
        try:
            cache.set('health_check', 'ok', 60)
            value = cache.get('health_check')
            
            if value == 'ok':
                return {
                    'status': 'healthy',
                    'message': 'Cache connection successful'
                }
            else:
                return {
                    'status': 'unhealthy',
                    'message': 'Cache set/get failed'
                }
        except Exception as e:
            logger.error(f'Cache health check failed: {str(e)}')
            return {
                'status': 'unhealthy',
                'message': f'Cache error: {str(e)}'
            }
    
    @staticmethod
    def check_static_files():
        """Check if static files directory is accessible"""
        from django.conf import settings
        import os
        
        static_root = settings.STATIC_ROOT
        
        if os.path.exists(static_root):
            return {
                'status': 'healthy',
                'message': 'Static files directory accessible'
            }
        else:
            return {
                'status': 'unhealthy',
                'message': 'Static files directory not found'
            }
    
    @staticmethod
    def check_media_files():
        """Check if media directory is accessible"""
        from django.conf import settings
        import os
        
        media_root = settings.MEDIA_ROOT
        
        if os.path.exists(media_root):
            return {
                'status': 'healthy',
                'message': 'Media directory accessible'
            }
        else:
            return {
                'status': 'unhealthy',
                'message': 'Media directory not found'
            }
    
    @staticmethod
    def get_full_health_status():
        """Get complete health status"""
        return {
            'timestamp': timezone.now().isoformat(),
            'database': HealthCheck.check_database(),
            'cache': HealthCheck.check_cache(),
            'static_files': HealthCheck.check_static_files(),
            'media_files': HealthCheck.check_media_files(),
        }


class PerformanceMonitor:
    """Monitor application performance"""
    
    @staticmethod
    def measure_execution_time(func):
        """Measure function execution time"""
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start
            
            logger.info(f'{func.__name__} took {duration:.3f}s')
            return result
        
        return wrapper
    
    @staticmethod
    def get_database_stats():
        """Get database query statistics"""
        from django.conf import settings
        
        if settings.DEBUG:
            return {
                'queries': len(connection.queries),
                'total_time': sum(float(q.get('time', 0)) for q in connection.queries),
            }
        return None


class ResourceMonitor:
    """Monitor system resources"""
    
    @staticmethod
    def get_memory_usage():
        """Get memory usage"""
        import psutil
        
        try:
            process = psutil.Process()
            memory = process.memory_info()
            return {
                'rss': memory.rss / 1024 / 1024,  # MB
                'vms': memory.vms / 1024 / 1024,  # MB
            }
        except:
            return None
    
    @staticmethod
    def get_cpu_usage():
        """Get CPU usage"""
        import psutil
        
        try:
            return {
                'percent': psutil.cpu_percent(interval=1),
            }
        except:
            return None
    
    @staticmethod
    def get_disk_usage():
        """Get disk usage"""
        import psutil
        from django.conf import settings
        
        try:
            disk = psutil.disk_usage(settings.BASE_DIR)
            return {
                'total': disk.total / 1024 / 1024 / 1024,  # GB
                'used': disk.used / 1024 / 1024 / 1024,    # GB
                'free': disk.free / 1024 / 1024 / 1024,    # GB
                'percent': disk.percent,
            }
        except:
            return None
