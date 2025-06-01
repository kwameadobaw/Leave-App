from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('manager-login/', views.manager_login, name='manager_login'),
    path('security-login/', views.security_login, name='security_login'),
    path('logout/', views.logout_view, name='logout'),
    path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('create-leave-request/', views.create_leave_request, name='create_leave_request'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('approve-reject-leave/<int:leave_id>/', views.approve_reject_leave, name='approve_reject_leave'),
    path('security-dashboard/', views.security_dashboard, name='security_dashboard'),
    path('download-leave-pdf/<int:leave_id>/', views.download_leave_pdf, name='download_leave_pdf'),
    path('log-employee-movement/<int:leave_id>/', views.log_employee_movement, name='log_employee_movement'),
]