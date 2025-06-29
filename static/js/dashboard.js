// Dashboard JavaScript functionality

// Global variables
let currentSection = 'dashboard';

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadDashboard();
    loadCoaches();
    loadUsers();
    loadStorage();
    loadLogs();
    loadReport();
});

// Navigation functions
function showSection(section) {
    // Hide all sections
    document.querySelectorAll('[id$="-section"]').forEach(el => {
        el.style.display = 'none';
    });
    
    // Show selected section
    document.getElementById(section + '-section').style.display = 'block';
    
    // Update navigation
    document.querySelectorAll('.nav-link').forEach(el => {
        el.classList.remove('active');
    });
    event.target.classList.add('active');
    
    currentSection = section;
}

// Dashboard functions
async function loadDashboard() {
    try {
        const [coachesRes, usersRes, storageRes, reportRes] = await Promise.all([
            fetch('/api/coaches'),
            fetch('/api/users'),
            fetch('/api/storage'),
            fetch('/api/report')
        ]);
        
        const coaches = await coachesRes.json();
        const users = await usersRes.json();
        const storage = await storageRes.json();
        const report = await reportRes.json();
        
        // Update stats
        document.getElementById('coaches-count').textContent = coaches.coaches.filter(c => c.status === 'active').length;
        document.getElementById('users-count').textContent = users.users.filter(u => u.status === 'active').length;
        document.getElementById('storage-count').textContent = storage.buckets.length;
        document.getElementById('revenue-today').textContent = `$${report.report.total_revenue.toFixed(2)}`;
        
        // Update recent activity
        updateRecentActivity(report.report.recent_transactions);
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

function updateRecentActivity(transactions) {
    const container = document.getElementById('recent-activity');
    
    if (transactions.length === 0) {
        container.innerHTML = '<p class="text-muted">No recent activity</p>';
        return;
    }
    
    const html = transactions.map(t => `
        <div class="d-flex justify-content-between align-items-center mb-2">
            <div>
                <strong>${t.description || 'Transaction'}</strong>
                <br><small class="text-muted">${t.time || t.date}</small>
            </div>
            <span class="badge bg-success">$${t.amount.toFixed(2)}</span>
        </div>
    `).join('');
    
    container.innerHTML = html;
}

// Coach functions
async function loadCoaches() {
    try {
        const response = await fetch('/api/coaches');
        const data = await response.json();
        
        const container = document.getElementById('coaches-list');
        
        if (data.coaches.length === 0) {
            container.innerHTML = '<p class="text-muted">No coaches found</p>';
            return;
        }
        
        const html = `
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Specialization</th>
                            <th>Rate</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.coaches.map(coach => `
                            <tr>
                                <td>${coach.name}</td>
                                <td>${coach.email}</td>
                                <td>${coach.specialization}</td>
                                <td>$${coach.hourly_rate}</td>
                                <td>
                                    <span class="badge bg-${coach.status === 'active' ? 'success' : 'danger'}">
                                        ${coach.status}
                                    </span>
                                </td>
                                <td>
                                    ${coach.status === 'active' ? 
                                        `<button class="btn btn-sm btn-warning" onclick="blockCoach('${coach.email}')">
                                            <i class="fas fa-ban"></i> Block
                                        </button>` :
                                        `<button class="btn btn-sm btn-success" onclick="unblockCoach('${coach.email}')">
                                            <i class="fas fa-check"></i> Unblock
                                        </button>`
                                    }
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
        
        container.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading coaches:', error);
        document.getElementById('coaches-list').innerHTML = '<p class="text-danger">Error loading coaches</p>';
    }
}

function showCreateCoachModal() {
    const modal = new bootstrap.Modal(document.getElementById('createCoachModal'));
    modal.show();
}

async function createCoach() {
    const form = document.getElementById('createCoachForm');
    const formData = new FormData(form);
    
    const data = {
        email: formData.get('email'),
        name: formData.get('name'),
        specialization: formData.get('specialization'),
        hourly_rate: formData.get('hourly_rate')
    };
    
    try {
        const response = await fetch('/api/coaches', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            bootstrap.Modal.getInstance(document.getElementById('createCoachModal')).hide();
            form.reset();
            loadCoaches();
            loadDashboard();
            showAlert('success', result.message);
        } else {
            showAlert('danger', result.message);
        }
        
    } catch (error) {
        console.error('Error creating coach:', error);
        showAlert('danger', 'Error creating coach');
    }
}

async function blockCoach(email) {
    try {
        const response = await fetch('/api/coaches/block', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        });
        
        const result = await response.json();
        
        if (result.success) {
            loadCoaches();
            showAlert('success', result.message);
        } else {
            showAlert('danger', result.message);
        }
        
    } catch (error) {
        console.error('Error blocking coach:', error);
        showAlert('danger', 'Error blocking coach');
    }
}

async function unblockCoach(email) {
    try {
        const response = await fetch('/api/coaches/unblock', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        });
        
        const result = await response.json();
        
        if (result.success) {
            loadCoaches();
            showAlert('success', result.message);
        } else {
            showAlert('danger', result.message);
        }
        
    } catch (error) {
        console.error('Error unblocking coach:', error);
        showAlert('danger', 'Error unblocking coach');
    }
}

// User functions
async function loadUsers() {
    try {
        const response = await fetch('/api/users');
        const data = await response.json();
        
        const container = document.getElementById('users-list');
        
        if (data.users.length === 0) {
            container.innerHTML = '<p class="text-muted">No users found</p>';
            return;
        }
        
        const html = `
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Role</th>
                            <th>Status</th>
                            <th>Created</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.users.map(user => `
                            <tr>
                                <td>${user.name}</td>
                                <td>${user.email}</td>
                                <td>
                                    <span class="badge bg-info">${user.role}</span>
                                </td>
                                <td>
                                    <span class="badge bg-${user.status === 'active' ? 'success' : 'danger'}">
                                        ${user.status}
                                    </span>
                                </td>
                                <td>${new Date(user.created_at).toLocaleDateString()}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
        
        container.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading users:', error);
        document.getElementById('users-list').innerHTML = '<p class="text-danger">Error loading users</p>';
    }
}

function showCreateUserModal() {
    const modal = new bootstrap.Modal(document.getElementById('createUserModal'));
    modal.show();
}

async function createUser() {
    const form = document.getElementById('createUserForm');
    const formData = new FormData(form);
    
    const data = {
        email: formData.get('email'),
        name: formData.get('name'),
        role: formData.get('role')
    };
    
    try {
        const response = await fetch('/api/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            bootstrap.Modal.getInstance(document.getElementById('createUserModal')).hide();
            form.reset();
            loadUsers();
            loadDashboard();
            showAlert('success', result.message);
        } else {
            showAlert('danger', result.message);
        }
        
    } catch (error) {
        console.error('Error creating user:', error);
        showAlert('danger', 'Error creating user');
    }
}

// Storage functions
async function loadStorage() {
    try {
        const response = await fetch('/api/storage');
        const data = await response.json();
        
        const container = document.getElementById('storage-list');
        
        if (data.buckets.length === 0) {
            container.innerHTML = '<p class="text-muted">No storage buckets found</p>';
            return;
        }
        
        const html = `
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Purpose</th>
                            <th>Size</th>
                            <th>Used</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.buckets.map(bucket => `
                            <tr>
                                <td>${bucket.name}</td>
                                <td>${bucket.purpose}</td>
                                <td>${bucket.size_gb}GB</td>
                                <td>${bucket.used_gb}GB</td>
                                <td>
                                    <span class="badge bg-${bucket.status === 'active' ? 'success' : 'danger'}">
                                        ${bucket.status}
                                    </span>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
        
        container.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading storage:', error);
        document.getElementById('storage-list').innerHTML = '<p class="text-danger">Error loading storage</p>';
    }
}

function showCreateStorageModal() {
    const modal = new bootstrap.Modal(document.getElementById('createStorageModal'));
    modal.show();
}

async function createStorage() {
    const form = document.getElementById('createStorageForm');
    const formData = new FormData(form);
    
    const data = {
        name: formData.get('name'),
        purpose: formData.get('purpose'),
        size_gb: formData.get('size_gb')
    };
    
    try {
        const response = await fetch('/api/storage', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            bootstrap.Modal.getInstance(document.getElementById('createStorageModal')).hide();
            form.reset();
            loadStorage();
            loadDashboard();
            showAlert('success', result.message);
        } else {
            showAlert('danger', result.message);
        }
        
    } catch (error) {
        console.error('Error creating storage bucket:', error);
        showAlert('danger', 'Error creating storage bucket');
    }
}

// Logs functions
async function loadLogs() {
    try {
        const days = document.getElementById('logs-days').value;
        const response = await fetch(`/api/logs?days=${days}`);
        const data = await response.json();
        
        const container = document.getElementById('logs-content');
        
        if (data.logs.length === 0) {
            container.innerHTML = '<p class="text-muted">No logs found</p>';
            return;
        }
        
        const html = data.logs.map(log => `
            <div class="mb-3">
                <h6>${log.date}</h6>
                <pre class="bg-light p-3 rounded" style="max-height: 200px; overflow-y: auto;">${log.content}</pre>
            </div>
        `).join('');
        
        container.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading logs:', error);
        document.getElementById('logs-content').innerHTML = '<p class="text-danger">Error loading logs</p>';
    }
}

// Report functions
async function loadReport() {
    try {
        const date = document.getElementById('report-date').value || new Date().toISOString().split('T')[0];
        const response = await fetch(`/api/report?date=${date}`);
        const data = await response.json();
        
        const container = document.getElementById('report-content');
        const report = data.report;
        
        const html = `
            <div class="row">
                <div class="col-md-6">
                    <h6>Summary</h6>
                    <ul class="list-unstyled">
                        <li><strong>Active Coaches:</strong> ${report.active_coaches}</li>
                        <li><strong>Active Users:</strong> ${report.active_users}</li>
                        <li><strong>Total Sessions:</strong> ${report.total_sessions}</li>
                        <li><strong>Total Revenue:</strong> $${report.total_revenue.toFixed(2)}</li>
                    </ul>
                </div>
                <div class="col-md-6">
                    <h6>Recent Transactions</h6>
                    ${report.recent_transactions.length > 0 ? 
                        report.recent_transactions.map(t => `
                            <div class="d-flex justify-content-between mb-1">
                                <small>${t.description || 'Transaction'}</small>
                                <small class="text-success">$${t.amount.toFixed(2)}</small>
                            </div>
                        `).join('') :
                        '<p class="text-muted">No transactions</p>'
                    }
                </div>
            </div>
        `;
        
        container.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading report:', error);
        document.getElementById('report-content').innerHTML = '<p class="text-danger">Error loading report</p>';
    }
}

// Utility functions
function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.querySelector('.main-content').insertBefore(alertDiv, document.querySelector('.main-content').firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Event listeners
document.getElementById('logs-days').addEventListener('change', loadLogs);
document.getElementById('report-date').addEventListener('change', loadReport); 