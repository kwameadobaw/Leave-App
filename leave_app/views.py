from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import LeaveRequest, UserProfile
from .forms import UserLoginForm, LeaveRequestForm, LeaveApprovalForm, UserRegistrationForm, UserUpdateForm, UserProfileUpdateForm, SecurityLogForm
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import io

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Set user's first and last name
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            
            # Update user profile (created by signal) instead of creating a new one
            profile_image = form.cleaned_data.get('profile_image')
            phone_number = form.cleaned_data.get('phone_number')
            
            # Get the profile that was created by the signal
            profile = UserProfile.objects.get(user=user)
            profile.profile_image = profile_image
            profile.phone_number = phone_number
            profile.save()
            
            messages.success(request, f'Account created for {user.username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'leave_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Use get_or_create to avoid IntegrityError
                profile, created = UserProfile.objects.get_or_create(user=user, defaults={'user_type': 'employee'})
                if profile.user_type == 'manager':
                    return redirect('manager_dashboard')
                elif profile.user_type == 'security':
                    return redirect('security_dashboard')
                else:
                    return redirect('employee_dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'leave_app/login.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    
    return render(request, 'leave_app/profile.html', context)

def manager_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if password == 'Manager123':
            # Find or create a manager user
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(username=username, password='Manager123')
                UserProfile.objects.create(user=user, user_type='manager')
            else:
                # Ensure the user has a manager profile
                # Use get_or_create to avoid IntegrityError
                profile, created = UserProfile.objects.get_or_create(user=user)
                profile.user_type = 'manager'
                profile.save()
            
            # Log the user in
            user = authenticate(username=username, password='Manager123')
            login(request, user)
            return redirect('manager_dashboard')
        else:
            messages.error(request, "Invalid manager password.")
    
    return render(request, 'leave_app/manager_login.html')

def security_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if password == 'Security123':
            # Find or create a security user
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(username=username, password='Security123')
                UserProfile.objects.create(user=user, user_type='security')
            else:
                # Ensure the user has a security profile
                # Use get_or_create to avoid IntegrityError
                profile, created = UserProfile.objects.get_or_create(user=user)
                profile.user_type = 'security'
                profile.save()
            
            # Log the user in
            user = authenticate(username=username, password='Security123')
            login(request, user)
            return redirect('security_dashboard')
        else:
            messages.error(request, "Invalid security password.")
    
    return render(request, 'leave_app/security_login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def employee_dashboard(request):
    # Check if user is an employee
    try:
        profile = request.user.profile
        if profile.user_type != 'employee':
            return redirect('login')
    except UserProfile.DoesNotExist:
        # Create employee profile if it doesn't exist
        UserProfile.objects.create(user=request.user, user_type='employee')
    
    # Get all leave requests for the current user
    leave_requests = LeaveRequest.objects.filter(employee=request.user).order_by('-created_at')
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(leave_requests, 5)  # Show 5 leave requests per page
    
    try:
        leave_requests = paginator.page(page)
    except PageNotAnInteger:
        leave_requests = paginator.page(1)
    except EmptyPage:
        leave_requests = paginator.page(paginator.num_pages)
    
    return render(request, 'leave_app/employee_dashboard.html', {
        'leave_requests': leave_requests
    })

@login_required
def create_leave_request(request):
    # Check if user is an employee
    try:
        profile = request.user.profile
        if profile.user_type != 'employee':
            return redirect('login')
    except UserProfile.DoesNotExist:
        # Create employee profile if it doesn't exist
        UserProfile.objects.create(user=request.user, user_type='employee')
    
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = request.user
            leave_request.save()
            messages.success(request, "Leave request submitted successfully!")
            return redirect('employee_dashboard')
    else:
        form = LeaveRequestForm()
    
    return render(request, 'leave_app/create_leave_request.html', {'form': form})

@login_required
def manager_dashboard(request):
    # Check if user is a manager
    try:
        profile = request.user.profile
        if profile.user_type != 'manager':
            return redirect('login')
    except UserProfile.DoesNotExist:
        return redirect('login')
    
    # Get pending, approved, and rejected leave requests
    pending_requests = LeaveRequest.objects.filter(status='pending').order_by('-created_at')
    approved_requests = LeaveRequest.objects.filter(status='approved').order_by('-created_at')
    rejected_requests = LeaveRequest.objects.filter(status='rejected').order_by('-created_at')
    
    return render(request, 'leave_app/manager_dashboard.html', {
        'leave_requests': pending_requests,  # Keep original name for backward compatibility
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'rejected_requests': rejected_requests
    })

@login_required
def approve_reject_leave(request, leave_id):
    # Check if user is a manager
    try:
        profile = request.user.profile
        if profile.user_type != 'manager':
            return redirect('login')
    except UserProfile.DoesNotExist:
        return redirect('login')
    
    leave_request = get_object_or_404(LeaveRequest, id=leave_id)
    
    if request.method == 'POST':
        form = LeaveApprovalForm(request.POST, instance=leave_request)
        if form.is_valid():
            form.save()
            messages.success(request, f"Leave request {leave_request.status} successfully!")
            return redirect('manager_dashboard')
    else:
        form = LeaveApprovalForm(instance=leave_request)
    
    return render(request, 'leave_app/approve_reject_leave.html', {
        'form': form,
        'leave_request': leave_request
    })

@login_required
def security_dashboard(request):
    # Check if user is security personnel
    try:
        profile = request.user.profile
        if profile.user_type != 'security':
            return redirect('login')
    except UserProfile.DoesNotExist:
        return redirect('login')
    
    # Get approved leave requests
    approved_requests = LeaveRequest.objects.filter(status='approved').order_by('-created_at')
    
    # Get rejected leave requests
    rejected_requests = LeaveRequest.objects.filter(status='rejected').order_by('-created_at')
    
    return render(request, 'leave_app/security_dashboard.html', {
        'approved_requests': approved_requests,
        'rejected_requests': rejected_requests
    })

@login_required
def log_employee_movement(request, leave_id):
    # Check if user is security personnel
    try:
        profile = request.user.profile
        if profile.user_type != 'security':
            return redirect('login')
    except UserProfile.DoesNotExist:
        return redirect('login')
    
    leave_request = get_object_or_404(LeaveRequest, id=leave_id, status='approved')
    
    if request.method == 'POST':
        form = SecurityLogForm(request.POST, instance=leave_request)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee movement logged successfully!")
            return redirect('security_dashboard')
    else:
        form = SecurityLogForm(instance=leave_request)
    
    return render(request, 'leave_app/log_employee_movement.html', {
        'form': form,
        'leave_request': leave_request
    })

@login_required
def download_leave_pdf(request, leave_id):
    # Check if user is the employee who owns the leave request
    leave_request = get_object_or_404(LeaveRequest, id=leave_id)
    
    # Allow access to the employee who owns the request, managers, and security personnel
    if (leave_request.employee != request.user and 
        request.user.profile.user_type != 'manager' and 
        request.user.profile.user_type != 'security'):
        messages.error(request, "You don't have permission to view this leave request.")
        return redirect('employee_dashboard')
    
    # Allow viewing both approved and rejected leave requests
    if leave_request.status not in ['approved', 'rejected']:
        messages.error(request, "Only approved or rejected leave requests can be viewed.")
        return redirect('employee_dashboard')
    
    # Determine which dashboard to redirect back to based on user type
    redirect_url = 'employee_dashboard'
    if request.user.profile.user_type == 'manager':
        redirect_url = 'manager_dashboard'
    elif request.user.profile.user_type == 'security':
        redirect_url = 'security_dashboard'
    
    # Render the template with print functionality
    return render(request, 'leave_app/view_leave_pdf.html', {
        'leave_request': leave_request,
        'user': request.user,
        'redirect_url': redirect_url
    })
