// Utilities
const showToast = (message, type = 'success') => {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i> <span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
};

const openModal = (id) => document.getElementById(id).classList.add('active');
const closeModal = (id) => document.getElementById(id).classList.remove('active');

const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

const fetchAPI = async (url, method='POST', body=null) => {
    const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
        body: body ? JSON.stringify(body) : null
    });
    return res.json();
};

const logout = () => {
    window.location.href = '/logout/';
};

const toggleTheme = () => {
    const body = document.body;
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    document.getElementById('theme-icon').className = newTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
};

// Navigation
const switchSection = (sectionId, element) => {
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
    if(element) element.classList.add('active');
    document.querySelectorAll('.section').forEach(el => el.classList.remove('active'));
    document.getElementById(`sec-${sectionId}`).classList.add('active');
};

const initDashboard = async () => {
    if (localStorage.getItem('theme') === 'dark') {
        document.body.setAttribute('data-theme', 'dark');
        document.getElementById('theme-icon').className = 'fas fa-sun';
    }

    const navItems = [
        { id: 'dashboard', icon: 'fas fa-home', label: 'Dashboard' },
        { id: 'rooms', icon: 'fas fa-bed', label: 'Rooms' },
        { id: 'students', icon: 'fas fa-users', label: 'Students' },
        { id: 'fees', icon: 'fas fa-money-bill-wave', label: 'Fees' },
        { id: 'complaints', icon: 'fas fa-exclamation-triangle', label: 'Complaints' },
        { id: 'attendance', icon: 'fas fa-calendar-check', label: 'Attendance' },
        { id: 'reports', icon: 'fas fa-chart-bar', label: 'Reports' },
        { id: 'notices', icon: 'fas fa-clipboard-list', label: 'Notice Board' }
    ];

    const navContainer = document.getElementById('sidebar-nav');
    if(navContainer) {
        navItems.forEach((item, index) => {
            const div = document.createElement('div');
            div.className = `nav-item ${index === 0 ? 'active' : ''}`;
            div.innerHTML = `<i class="${item.icon}"></i> <span>${item.label}</span>`;
            div.onclick = () => switchSection(item.id, div);
            navContainer.appendChild(div);
        });
    }

    const role = document.querySelector('.dashboard-layout').getAttribute('data-role');
    if (role === 'student') {

    document.querySelectorAll('.admin-only').forEach(el => {
        el.style.display = 'none';
    });

    // studentinu delete buttons hide
    document.querySelectorAll('.btn-danger').forEach(el => {
        el.style.display = 'none';
    });

} else {

    document.querySelectorAll('.student-only').forEach(el => {
        el.style.display = 'none';
    });

}

    // Global Search Filter
    const searchInput = document.getElementById('global-search');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            const activeSection = document.querySelector('.section.active');
            if (activeSection) {
                const rows = activeSection.querySelectorAll('tbody tr');
                rows.forEach(row => {
                    const text = row.innerText.toLowerCase();
                    row.style.display = text.includes(query) ? '' : 'none';
                });
            }
        });
    }

    await loadData();
};

const loadData = async () => {
    const res = await fetch('/api/data/');
    const data = await res.json();
    
    // Render Rooms
    document.getElementById('rooms-table-body').innerHTML = data.rooms.map(r => `
        <tr>
            <td>${r.room_no}</td>
            <td>${r.room_type}</td>
            <td>${r.capacity}</td>
            <td>${r.occupied}</td>
            <td><span class="badge ${r.status === 'Full' ? 'danger' : 'success'}">${r.status}</span></td>
            <td>
                <button class="btn btn-small btn-danger" onclick="deleteRoom('${r.room_no}')"><i class="fas fa-trash"></i></button>
            </td>
        </tr>
    `).join('');

    // Render Students
    document.getElementById('students-table-body').innerHTML = data.students.map(s => `
        <tr>
            <td>${s.name}</td>
            <td>${s.email}</td>
            <td>${s.phone || 'N/A'}</td>
            <td>${s.room_no || 'Unallocated'}</td>
            <td>
                <button class="btn btn-small btn-danger" onclick="deleteStudent(${s.id})"><i class="fas fa-trash"></i></button>
            </td>
        </tr>
    `).join('');

    // Render Fees
    document.getElementById('fees-table-body').innerHTML = data.fees.map(f => `
        <tr>
            <td>${f.student_name}</td>
            <td>${f.amount}</td>
            <td>${f.month}</td>
            <td><span class="badge ${f.status === 'Paid' ? 'success' : 'warning'}">${f.status}</span></td>
            <td>${f.date_paid || '-'}</td>
        </tr>
    `).join('');

    // Render Complaints
    document.getElementById('complaints-table-body').innerHTML = data.complaints.map(c => `
        <tr>
            <td>${c.id}</td>
            <td>${c.student_name}</td>
            <td>${c.category}</td>
            <td>${c.description}</td>
            <td><span class="badge ${c.status === 'Pending' ? 'warning' : 'success'}">${c.status}</span></td>
            <td>
                ${c.status === 'Pending' ? `<button class="btn btn-small" onclick="resolveComplaint('${c.id}')">Resolve</button>` : 'Resolved'}
            </td>
        </tr>
    `).join('');

    // Render Attendance
    const attBody = document.getElementById('attendance-table-body');
    if (attBody) {
        attBody.innerHTML = data.attendance.map(a => `
            <tr>
                <td>${a.student_name}</td>
                <td>${a.date}</td>
                <td><span class="badge ${a.status === 'Present' ? 'success' : 'danger'}">${a.status}</span></td>
            </tr>
        `).join('');
    }

    // Render Notices
    const noticesGrid = document.getElementById('notices-grid');
    const dbNotices = document.getElementById('dashboard-notices');
    const noticesHtml = data.notices.map(n => `
        <div class="notice-card">
            <div class="notice-date">${new Date(n.date_posted).toLocaleDateString()}</div>
            <div class="notice-title">${n.title}</div>
            <div class="notice-content">${n.content}</div>
        </div>
    `).join('');
    if (noticesGrid) noticesGrid.innerHTML = noticesHtml || '<p>No notices available.</p>';
    if (dbNotices) dbNotices.innerHTML = noticesHtml || '<p>No notices available.</p>';
};

// CRUD Actions
const submitRoom = async () => {
    const no = document.getElementById('r-no').value;
    const type = document.getElementById('r-type').value;
    if(!no) return;
    
    await fetchAPI('/api/add_room/', 'POST', { no, type });
    closeModal('add-room-modal');
    showToast('Room added successfully');
    window.location.reload(); // To update dashboard stats natively
};

const deleteRoom = async (no) => {
    if(confirm('Are you sure you want to delete this room?')) {
        await fetchAPI(`/api/delete_room/${no}/`);
        showToast('Room deleted');
        window.location.reload();
    }
};

const deleteStudent = async (id) => {
    if(confirm('Are you sure you want to delete this student?')) {
        await fetchAPI(`/api/delete_student/${id}/`);
        showToast('Student deleted');
        window.location.reload();
    }
}

const submitComplaint = async () => {
    const category = document.getElementById('c-category').value;
    const desc = document.getElementById('c-desc').value;
    if(!desc) return;
    
    await fetchAPI('/api/add_complaint/', 'POST', { category, desc });
    closeModal('add-complaint-modal');
    showToast('Complaint submitted successfully');
    window.location.reload();
};

const resolveComplaint = async (id) => {
    await fetchAPI(`/api/resolve_complaint/${id}/`);
    showToast('Complaint resolved');
    window.location.reload();
};

const payFee = async () => {
    await fetchAPI('/api/pay_fee/');
    showToast('Fee payment recorded');
    window.location.reload();
};

const submitNotice = async () => {
    const title = document.getElementById('n-title').value;
    const content = document.getElementById('n-content').value;
    if(!title || !content) return;
    
    await fetchAPI('/api/add_notice/', 'POST', { title, content });
    closeModal('add-notice-modal');
    showToast('Notice published successfully');
    window.location.reload();
};
const submitStudent = async () => {

    const name = document.getElementById('s-name').value;
    const email = document.getElementById('s-email').value;
    const phone = document.getElementById('s-phone').value;

    await fetchAPI('/api/add_student/', 'POST', {
        name,
        email,
        phone
    });

    closeModal('add-student-modal');

    showToast('Student added');

    window.location.reload();
};


const submitFee = async () => {

    const student_id = document.getElementById('f-student-id').value;
    const amount = document.getElementById('f-amount').value;
    const month = document.getElementById('f-month').value;

    await fetchAPI('/api/add_fee/', 'POST', {
        student_id,
        amount,
        month
    });

    closeModal('add-fee-modal');

    showToast('Fee added');

    window.location.reload();
};


const submitAttendance = async () => {

    const student_id = document.getElementById('a-student-id').value;
    const status = document.getElementById('a-status').value;

    await fetchAPI('/api/mark_attendance/', 'POST', {
        student_id,
        status
    });

    closeModal('attendance-modal');

    showToast('Attendance marked');

    window.location.reload();
};
document.addEventListener('DOMContentLoaded', () => {

    const dashboard = document.querySelector('.dashboard-layout');

    if (dashboard) {

        initDashboard();

    }

});
