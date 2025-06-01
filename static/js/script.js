// Leave Management System - Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to main content
    const mainContent = document.querySelector('.col-md-9');
    if (mainContent) {
        mainContent.classList.add('fade-in');
    }

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Date validation for leave request form
    const startDateInput = document.getElementById('id_start_date');
    const endDateInput = document.getElementById('id_end_date');

    if (startDateInput && endDateInput) {
        // Set minimum date to today
        const today = new Date().toISOString().split('T')[0];
        startDateInput.setAttribute('min', today);
        
        // Update end date minimum when start date changes
        startDateInput.addEventListener('change', function() {
            endDateInput.setAttribute('min', this.value);
            
            // If end date is before start date, update it
            if (endDateInput.value && endDateInput.value < this.value) {
                endDateInput.value = this.value;
            }
        });
    }

    // Mobile sidebar toggle
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
    }

    // Status badge animations
    const statusBadges = document.querySelectorAll('.badge');
    statusBadges.forEach(badge => {
        badge.addEventListener('mouseover', function() {
            this.style.transform = 'scale(1.1)';
        });
        badge.addEventListener('mouseout', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // Table row hover effect
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseover', function() {
            this.style.transition = 'background-color 0.3s ease';
        });
    });
});