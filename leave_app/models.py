from django.db import models
from django.contrib.auth.models import User

class LeaveRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_requests')
    start_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_date = models.DateField()
    end_time = models.TimeField(null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Security logging fields
    departure_time = models.DateTimeField(null=True, blank=True)
    return_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.employee.username}'s leave request from {self.start_date} to {self.end_date}"
    
    class Meta:
        ordering = ['-created_at']

class UserProfile(models.Model):
    USER_TYPES = (
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('security', 'Security'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='employee')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"
