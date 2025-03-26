// Initialize the page on DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded - Starting initialization");

    // Since we're now using SweetAlert2, no need to load Notie
    // loadNotieLibrary();  <-- Removed

    const filterButton = document.getElementById('filter-button');
    const staffFilter = document.getElementById('staff-filter');
    const userRows = document.querySelectorAll('#table tbody tr');

    // Initialize filters section
    setupFilters(filterButton, staffFilter, userRows);

    // Initialize action buttons and modals
    setupActionButtons();
    initializeModals();
    setupMessageAutoHide();

    // Debug logs for important DOM elements
    console.log("Filter button:", filterButton ? "Found" : "Not found");
    console.log("Staff filter:", staffFilter ? "Found" : "Not found");
    console.log("User rows:", userRows.length);
    console.log("Edit modal:", document.getElementById('edit-modal') ? "Found" : "Not found");
    console.log("Reset password modal:", document.getElementById('reset-password-modal') ? "Found" : "Not found");
    console.log("Initialization complete");
});

// Function to show notifications using SweetAlert2
function showNotification(type, message, duration = 3000) {
    let icon;
    switch (type) {
        case 'success':
            icon = 'success';
            break;
        case 'error':
            icon = 'error';
            break;
        case 'warning':
            icon = 'warning';
            break;
        case 'info':
            icon = 'info';
            break;
        default:
            icon = 'info';
    }
    Swal.fire({
        icon: icon,
        title: message,
        timer: duration,
        showConfirmButton: false,
        position: 'center'
    });
}

// Function to show confirmation dialog using SweetAlert2
function showConfirmation(message, confirmCallback, cancelCallback = null) {
    Swal.fire({
        title: 'Confirmation',
        text: message,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes',
        cancelButtonText: 'No',
        reverseButtons: true,
        allowOutsideClick: true
    }).then((result) => {
        if (result.isConfirmed) {
            confirmCallback();
        } else if (result.dismiss === Swal.DismissReason.cancel) {
            if (cancelCallback) {
                cancelCallback();
            }
        }
    });
}

// Setup filters section
function setupFilters(filterButton, staffFilter, userRows) {
    const filterOptions = document.querySelector('.filter-options');

    // Create and style the filter popup
    const createFilterPopup = () => {
        if (document.getElementById('filter-popup')) {
            return document.getElementById('filter-popup');
        }

        const popup = document.createElement('div');
        popup.id = 'filter-popup';
        popup.style.position = 'absolute';
        popup.style.top = '70px';
        popup.style.right = '20px';
        popup.style.backgroundColor = '#fff';
        popup.style.padding = '15px';
        popup.style.borderRadius = '10px';
        popup.style.boxShadow = '0 5px 15px rgba(0,0,0,0.2)';
        popup.style.zIndex = '100';
        popup.style.width = '300px';
        popup.style.display = 'none';

        const heading = document.createElement('h3');
        heading.textContent = 'Filter Users';
        heading.style.marginBottom = '15px';
        heading.style.borderBottom = '1px solid #eee';
        heading.style.paddingBottom = '10px';

        const staffFilterClone = staffFilter ? staffFilter.cloneNode(true) : document.createElement('select');
        staffFilterClone.id = 'staff-filter-popup';
        staffFilterClone.style.width = '100%';
        staffFilterClone.style.padding = '10px';
        staffFilterClone.style.marginBottom = '15px';
        staffFilterClone.style.borderRadius = '5px';
        staffFilterClone.style.border = '1px solid #ddd';

        if (!staffFilter) {
            const options = [
                { value: 'all', text: 'All Users' },
                { value: 'staff', text: 'Staff Only' },
                { value: 'regular', text: 'Regular Users Only' }
            ];
            options.forEach(opt => {
                const option = document.createElement('option');
                option.value = opt.value;
                option.textContent = opt.text;
                staffFilterClone.appendChild(option);
            });
        }

        const buttonsContainer = document.createElement('div');
        buttonsContainer.style.display = 'flex';
        buttonsContainer.style.justifyContent = 'space-between';

        const applyButton = document.createElement('button');
        applyButton.textContent = 'Apply Filters';
        applyButton.style.backgroundColor = '#5a8f9c';
        applyButton.style.color = 'white';
        applyButton.style.border = 'none';
        applyButton.style.padding = '10px 15px';
        applyButton.style.borderRadius = '5px';
        applyButton.style.cursor = 'pointer';

        const resetButton = document.createElement('button');
        resetButton.textContent = 'Reset';
        resetButton.style.backgroundColor = '#ccc';
        resetButton.style.color = 'white';
        resetButton.style.border = 'none';
        resetButton.style.padding = '10px 15px';
        resetButton.style.borderRadius = '5px';
        resetButton.style.cursor = 'pointer';

        const closeButton = document.createElement('button');
        closeButton.textContent = '✕';
        closeButton.style.position = 'absolute';
        closeButton.style.top = '10px';
        closeButton.style.right = '10px';
        closeButton.style.backgroundColor = 'transparent';
        closeButton.style.border = 'none';
        closeButton.style.fontSize = '18px';
        closeButton.style.cursor = 'pointer';

        buttonsContainer.appendChild(resetButton);
        buttonsContainer.appendChild(applyButton);

        popup.appendChild(heading);
        popup.appendChild(closeButton);
        popup.appendChild(staffFilterClone);
        popup.appendChild(buttonsContainer);

        document.querySelector('.header').appendChild(popup);

        closeButton.addEventListener('click', () => {
            popup.style.display = 'none';
        });

        applyButton.addEventListener('click', () => {
            const staffFilterValue = staffFilterClone.value;
            userRows.forEach(row => {
                applyStaffFilter(row, staffFilterValue);
            });
            if (staffFilter) {
                staffFilter.value = staffFilterValue;
            }
            popup.style.display = 'none';
            showNotification('success', 'Filters applied successfully', 2000);
        });

        resetButton.addEventListener('click', () => {
            staffFilterClone.value = 'all';
            userRows.forEach(row => {
                row.style.display = '';
            });
            if (staffFilter) {
                staffFilter.value = 'all';
            }
            showNotification('info', 'Filters reset', 2000);
        });

        return popup;
    };

    if (filterButton) {
        filterButton.addEventListener('click', function() {
            const popup = createFilterPopup();
            if (popup.style.display === 'none') {
                popup.style.display = 'block';
                popup.style.opacity = '0';
                popup.style.transform = 'translateY(-10px)';
                setTimeout(() => {
                    popup.style.opacity = '1';
                    popup.style.transform = 'translateY(0)';
                    popup.style.transition = 'all 0.3s ease';
                }, 10);
            } else {
                popup.style.display = 'none';
            }
        });
    }

    const style = document.createElement('style');
    style.textContent = `
        #filter-popup {
            animation: fadeIn 0.3s ease;
            transition: all 0.3s ease;
        }
        
        #filter-popup button:hover {
            opacity: 0.9;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    `;
    document.head.appendChild(style);
}

// Apply staff filter to a table row
function applyStaffFilter(row, staffFilter) {
    if (!row) return;
    const isStaff = row.getAttribute('data-is-staff') === 'true';
    if (staffFilter === 'all') {
        row.style.display = '';
    } else {
        const showRow = (staffFilter === 'staff' && isStaff) || (staffFilter === 'regular' && !isStaff);
        row.style.display = showRow ? '' : 'none';
    }
}

// Setup action buttons (edit, toggle status, delete, etc.)
function setupActionButtons() {
    console.log("Setting up action buttons");

    debugElement('edit-button', 'Edit button:');
    debugElement('reset-password-button', 'Reset password button:');
    debugElement('toggle-status-button', 'Toggle status button:');
    debugElement('delete-button', 'Delete button:');

    const editButton = document.getElementById('edit-button');
    if (editButton) {
        editButton.addEventListener('click', function() {
            console.log("Edit button clicked");
            const userId = new URLSearchParams(window.location.search).get('user_id');
            console.log("User ID:", userId);

            if (userId) {
                try {
                    const modal = document.getElementById('edit-modal');
                    console.log("Edit modal:", modal ? "Found" : "Not found");

                    if (modal) {
                        const userIdInput = modal.querySelector('input[name="user_id"]');
                        if (userIdInput) userIdInput.value = userId;

                        const detailsElement = document.getElementById('general_details');
                        console.log("General details element:", detailsElement ? "Found" : "Not found");

                        if (detailsElement) {
                            const paragraphs = detailsElement.querySelectorAll('p');
                            console.log("Number of paragraphs found:", paragraphs.length);

                            let username = "", email = "", isStaff = false;
                            paragraphs.forEach((p, index) => {
                                const text = p.textContent || "";
                                console.log(`Paragraph ${index} text:`, text);
                                if (text.includes("Name:")) {
                                    username = text.split(': ')[1] || "";
                                } else if (text.includes("Email:")) {
                                    email = text.split(': ')[1] || "";
                                } else if (text.includes("Staff Status:")) {
                                    isStaff = text.includes('Yes');
                                }
                            });

                            console.log("Extracted - Username:", username);
                            console.log("Extracted - Email:", email);
                            console.log("Extracted - Is Staff:", isStaff);

                            const usernameInput = modal.querySelector('#username');
                            const emailInput = modal.querySelector('#email');
                            const staffSelect = modal.querySelector('#is_staff');

                            if (usernameInput) usernameInput.value = username;
                            if (emailInput) emailInput.value = email;
                            if (staffSelect) staffSelect.value = isStaff ? 'true' : 'false';
                        } else {
                            console.error("Could not find general_details element");
                        }
                        modal.style.display = 'block';
                    } else {
                        console.error("Edit modal not found in DOM");
                        showNotification('error', 'Could not find the edit form. Please contact support.');
                    }
                } catch (error) {
                    console.error("Error setting up edit modal:", error);
                    showNotification('error', 'An error occurred. Please try again or contact support.');
                }
            } else {
                showNotification('warning', 'Please select a user first');
            }
        });
    } else {
        console.error("Edit button not found in DOM");
    }

    const toggleStatusButton = document.getElementById('toggle-status-button');
    if (toggleStatusButton) {
        toggleStatusButton.addEventListener('click', function() {
            console.log("Toggle status button clicked");
            const userId = new URLSearchParams(window.location.search).get('user_id');

            if (userId) {
                const statusElement = document.querySelector('#status');
                const isActive = statusElement && statusElement.textContent.includes('Active');
                const action = isActive ? 'disable' : 'enable';

                showConfirmation(
                    `Are you sure you want to ${action} this account?`,
                    function() {
                        const form = document.getElementById('disable-form');
                        if (form) {
                            const userIdInput = form.querySelector('input[name="user_id"]');
                            if (userIdInput) userIdInput.value = userId;
                            form.submit();
                        } else {
                            console.error("Disable form not found");
                            showNotification('error', 'Could not find the form. Please contact support.');
                        }
                    }
                );
            } else {
                showNotification('warning', 'Please select a user first');
            }
        });
    }

    const deleteButton = document.getElementById('delete-button');
    if (deleteButton) {
        deleteButton.addEventListener('click', function() {
            console.log("Delete button clicked");
            const userId = new URLSearchParams(window.location.search).get('user_id');

            if (userId) {
                showConfirmation(
                    'Are you sure you want to delete this account? This action cannot be undone.',
                    function() {
                        const form = document.getElementById('delete-form');
                        if (form) {
                            const userIdInput = form.querySelector('input[name="user_id"]');
                            if (userIdInput) userIdInput.value = userId;
                            form.submit();
                        } else {
                            console.error("Delete form not found");
                            showNotification('error', 'Could not find the form. Please contact support.');
                        }
                    }
                );
            } else {
                showNotification('warning', 'Please select a user first');
            }
        });
    }

    console.log("Action buttons setup complete");
}

// Helper function for debugging DOM elements
function debugElement(id, message) {
    const element = document.getElementById(id);
    console.log(message, element ? "Found" : "Not found");
    return element;
}

// Initialize modal behaviors
function initializeModals() {
    console.log("Initializing modals");

    const closeButtons = document.querySelectorAll('.modal .close');
    console.log("Close buttons found:", closeButtons.length);

    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const modal = this.closest('.modal');
            if (modal) modal.style.display = 'none';
        });
    });

    window.addEventListener('click', function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    });

    const resetPasswordForm = document.querySelector('#reset-password-modal form');
    if (resetPasswordForm) {
        resetPasswordForm.addEventListener('submit', function(event) {
            const newPassword = document.getElementById('new_password')?.value || '';
            const confirmPassword = document.getElementById('confirm_password')?.value || '';

            if (newPassword !== confirmPassword) {
                event.preventDefault();
                showNotification('error', "Passwords don't match. Please try again.");
                return false;
            }

            if (newPassword.length < 8) {
                event.preventDefault();
                showNotification('error', "Password must be at least 8 characters long.");
                return false;
            }

            return true;
        });
    } else {
        console.log("Reset password form not found");
    }

    console.log("Modals initialization complete");
}

// Automatically hide messages after a few seconds
function setupMessageAutoHide() {
    const messages = document.querySelectorAll('.message');
    console.log("Status messages found:", messages.length);

    if (messages.length > 0) {
        setTimeout(() => {
            messages.forEach(message => {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.style.display = 'none';
                }, 500);
            });
        }, 5000);
    }

    console.log("Message auto-hide setup complete");
}
