"""
API Response utilities and serializers
"""
from rest_framework.response import Response
from rest_framework import status
import json


class APIResponseHelper:
    """Helper for standardized API responses"""
    
    @staticmethod
    def success_response(data=None, message='Success', status_code=status.HTTP_200_OK):
        """Return standardized success response"""
        response_data = {
            'success': True,
            'message': message,
            'data': data
        }
        return Response(response_data, status=status_code)
    
    @staticmethod
    def error_response(error=None, message='Error', status_code=status.HTTP_400_BAD_REQUEST):
        """Return standardized error response"""
        response_data = {
            'success': False,
            'message': message,
            'error': error
        }
        return Response(response_data, status=status_code)
    
    @staticmethod
    def paginated_response(data, count, next_page=None, previous_page=None):
        """Return paginated response"""
        return Response({
            'success': True,
            'count': count,
            'next': next_page,
            'previous': previous_page,
            'results': data
        })
    
    @staticmethod
    def created_response(data, message='Created successfully'):
        """Return created (201) response"""
        return APIResponseHelper.success_response(
            data=data,
            message=message,
            status_code=status.HTTP_201_CREATED
        )
    
    @staticmethod
    def not_found_response(message='Resource not found'):
        """Return not found (404) response"""
        return APIResponseHelper.error_response(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    @staticmethod
    def unauthorized_response(message='Unauthorized'):
        """Return unauthorized (401) response"""
        return APIResponseHelper.error_response(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    @staticmethod
    def forbidden_response(message='Forbidden'):
        """Return forbidden (403) response"""
        return APIResponseHelper.error_response(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN
        )


class APIErrorHandler:
    """Handle and format API errors"""
    
    @staticmethod
    def handle_validation_error(serializer):
        """Handle serializer validation errors"""
        errors = {}
        for field, error_list in serializer.errors.items():
            errors[field] = [str(e) for e in error_list]
        
        return APIResponseHelper.error_response(
            error=errors,
            message='Validation failed',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    @staticmethod
    def handle_not_found(model_name='Resource'):
        """Handle resource not found"""
        return APIResponseHelper.not_found_response(
            message=f'{model_name} not found'
        )
    
    @staticmethod
    def handle_permission_denied():
        """Handle permission denied"""
        return APIResponseHelper.forbidden_response(
            message='You do not have permission to perform this action'
        )


class APIMetadata:
    """API metadata helpers"""
    
    @staticmethod
    def get_api_info():
        """Get API information"""
        return {
            'name': 'MWECAU ICT Club API',
            'version': '1.0.0',
            'description': 'RESTful API for MWECAU ICT Club management system',
            'endpoints': {
                'users': '/api/users/',
                'departments': '/api/departments/',
                'projects': '/api/projects/',
                'events': '/api/events/',
                'announcements': '/api/announcements/',
            }
        }
    
    @staticmethod
    def get_endpoint_documentation(endpoint_name):
        """Get documentation for specific endpoint"""
        docs = {
            'users': {
                'description': 'User management endpoints',
                'methods': ['GET', 'POST', 'PUT', 'DELETE']
            },
            'departments': {
                'description': 'Department management endpoints',
                'methods': ['GET', 'POST']
            },
            'projects': {
                'description': 'Project management endpoints',
                'methods': ['GET', 'POST', 'PUT', 'DELETE']
            },
        }
        return docs.get(endpoint_name)
