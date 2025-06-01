from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import LeaveRequest, UserProfile

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        required=True
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        required=True
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        required=True
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        required=True,
        help_text="<ul class='text-muted small'>"
                  "<li>Your password can't be too similar to your other personal information.</li>"
                  "<li>Your password must contain at least 8 characters.</li>"
                  "<li>Your password can't be a commonly used password.</li>"
                  "<li>Your password can't be entirely numeric.</li></ul>"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        required=True
    )
    profile_image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        required=False
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'phone_number']
        widgets = {
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'start_time', 'end_date', 'end_time', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class LeaveApprovalForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class SecurityLogForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['departure_time', 'return_time']
        widgets = {
            'departure_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'return_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }