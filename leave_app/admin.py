from django.contrib import admin
from .models import LeaveRequest, UserProfile

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('employee__username', 'reason')
    date_hierarchy = 'created_at'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_full_name', 'get_email', 'phone_number', 'user_type')
    list_filter = ('user_type',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'phone_number')
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
