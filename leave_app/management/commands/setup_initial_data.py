from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from leave_app.models import UserProfile, LeaveRequest
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Sets up initial data for the leave management system'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Setting up initial data...'))
        
        # Create user groups
        employee_group, created = Group.objects.get_or_create(name='Employee')
        manager_group, created = Group.objects.get_or_create(name='Manager')
        security_group, created = Group.objects.get_or_create(name='Security')
        
        self.stdout.write(self.style.SUCCESS('Created user groups'))
        
        # Create sample users
        # Admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            UserProfile.objects.create(user=admin_user, user_type='admin')
        
        # Employee users
        employee_users = []
        for i in range(1, 6):
            username = f'employee{i}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'first_name': f'Employee{i}',
                    'last_name': 'User'
                }
            )
            if created:
                user.set_password('employee123')
                user.save()
                user.groups.add(employee_group)
                UserProfile.objects.create(user=user, user_type='employee')
                employee_users.append(user)
        
        # Manager users
        manager_users = []
        for i in range(1, 3):
            username = f'manager{i}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'first_name': f'Manager{i}',
                    'last_name': 'User'
                }
            )
            if created:
                user.set_password('manager123')
                user.save()
                user.groups.add(manager_group)
                UserProfile.objects.create(user=user, user_type='manager')
                manager_users.append(user)
        
        # Security users
        security_users = []
        for i in range(1, 3):
            username = f'security{i}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'first_name': f'Security{i}',
                    'last_name': 'User'
                }
            )
            if created:
                user.set_password('security123')
                user.save()
                user.groups.add(security_group)
                UserProfile.objects.create(user=user, user_type='security')
                security_users.append(user)
        
        self.stdout.write(self.style.SUCCESS('Created sample users'))
        
        # Create sample leave requests
        if employee_users and not LeaveRequest.objects.exists():
            statuses = ['pending', 'approved', 'rejected']
            reasons = [
                'Personal leave',
                'Medical appointment',
                'Family emergency',
                'Vacation',
                'Home repairs',
                'Professional development',
                'Religious holiday'
            ]
            
            today = datetime.now().date()
            
            for employee in employee_users:
                # Create 3-5 leave requests per employee
                for _ in range(random.randint(3, 5)):
                    status = random.choice(statuses)
                    start_date = today + timedelta(days=random.randint(1, 30))
                    end_date = start_date + timedelta(days=random.randint(1, 5))
                    reason = random.choice(reasons)
                    
                    LeaveRequest.objects.create(
                        employee=employee,
                        start_date=start_date,
                        end_date=end_date,
                        reason=reason,
                        status=status
                    )
            
            self.stdout.write(self.style.SUCCESS('Created sample leave requests'))
        
        self.stdout.write(self.style.SUCCESS('Initial data setup complete!'))