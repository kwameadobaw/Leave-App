from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class RoleBasedAccessMiddleware:
    """Middleware to enforce role-based access control"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Process request before view is called
        if request.user.is_authenticated:
            # Get current path
            path = request.path_info
            
            # Skip middleware for static files, admin, and authentication views
            if path.startswith('/static/') or path.startswith('/media/') or \
               path.startswith('/admin/') or path == reverse('logout'):
                return self.get_response(request)
            
            try:
                user_type = request.user.userprofile.user_type
                
                # Employee access restrictions
                if user_type == 'employee':
                    if path.startswith('/manager/') or path.startswith('/security/'):
                        messages.error(request, 'Access denied. You do not have permission to view this page.')
                        return redirect('employee_dashboard')
                
                # Manager access restrictions
                elif user_type == 'manager':
                    if path.startswith('/security/'):
                        messages.error(request, 'Access denied. You do not have permission to view this page.')
                        return redirect('manager_dashboard')
                    
                # Security access restrictions
                elif user_type == 'security':
                    if path.startswith('/manager/'):
                        messages.error(request, 'Access denied. You do not have permission to view this page.')
                        return redirect('security_dashboard')
                        
            except AttributeError:
                # Handle case where user doesn't have a profile
                pass
        
        # Process response after view is called
        response = self.get_response(request)
        return response