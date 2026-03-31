/**
 * StockFlow Luxury Minimalism Core UI Logic
 */

// UI State Management
const UIState = {
    darkMode: localStorage.getItem('theme') !== 'light',
    sidebarOpen: window.innerWidth > 1024,
    searchOpen: false,
    modalOpen: false
};

// Initialize UI
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initToasts();
    initKeyboardShortcuts();
    
    // Auto-hide mobile sidebar
    if (window.innerWidth < 1024) toggleSidebar(false);
});

// Theme Management
function initTheme() {
    const toggleBtn = document.getElementById('theme-toggle');
    const sunIcon = document.getElementById('sun-icon');
    const moonIcon = document.getElementById('moon-icon');
    const body = document.getElementById('main-body');

    const autoFillDemo = () => {
        const e = document.getElementById('email');
        const p = document.getElementById('password');
        if (e && p) {
            e.value = "tony@stark.com";
            p.value = "iamironman";
            showToast("Tony Stark credentials synchronized.", "success");
        }
    };

    const updateThemeUI = (isDark) => {
        if (isDark) {
            document.documentElement.classList.remove('light-mode');
            body.classList.remove('light-mode');
            sunIcon?.classList.remove('hidden');
            moonIcon?.classList.add('hidden');
        } else {
            document.documentElement.classList.add('light-mode');
            body.classList.add('light-mode');
            sunIcon?.classList.add('hidden');
            moonIcon?.classList.remove('hidden');
        }
    };

    updateThemeUI(UIState.darkMode);

    toggleBtn?.addEventListener('click', () => {
        UIState.darkMode = !UIState.darkMode;
        localStorage.setItem('theme', UIState.darkMode ? 'dark' : 'light');
        updateThemeUI(UIState.darkMode);
    });
}

// Toast Notification System
function showToast(message, type = 'info', duration = 4000) {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast-item glass-card backdrop-blur-xl border border-white/10 rounded-2xl p-4 flex items-start gap-4 animate-slide opacity-0 max-w-sm pointer-events-auto shadow-2xl`;
    
    let icon = 'info';
    let iconColor = 'text-primary';
    if (type === 'success') { icon = 'check-circle'; iconColor = 'text-accent'; }
    if (type === 'error') { icon = 'alert-circle'; iconColor = 'text-danger'; }
    if (type === 'warning') { icon = 'alert-triangle'; iconColor = 'text-warning'; }

    toast.innerHTML = `
        <div class="${iconColor}">
            <i data-lucide="${icon}" class="w-5 h-5"></i>
        </div>
        <div class="flex-1">
            <h4 class="text-xs font-display font-bold uppercase tracking-widest text-primary/40 mb-1">System Alert</h4>
            <p class="text-[0.78rem] font-medium leading-relaxed">${message}</p>
        </div>
        <button class="text-white/20 hover:text-white transition-colors" onclick="this.parentElement.remove()">
            <i data-lucide="x" class="w-4 h-4"></i>
        </button>
    `;

    container.appendChild(toast);
    lucide.createIcons();
    
    // Animate in
    setTimeout(() => toast.style.opacity = '1', 10);

    // Auto remove
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(20px)';
        setTimeout(() => toast.remove(), 400);
    }, duration);
}

function initToasts() {
    // Process server-side flashes passed via base.html
    if (typeof flashes !== 'undefined' && Array.isArray(flashes)) {
        flashes.forEach((f, i) => {
            const [category, message] = Array.isArray(f) ? f : [null, f];
            if (message) {
                setTimeout(() => showToast(message, category === 'message' ? 'success' : category), i * 500);
            }
        });
    }
}

// Sidebar Management
function toggleSidebar(force) {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    if (!sidebar) return;

    const isOpen = typeof force === 'boolean' ? force : sidebar.classList.contains('-translate-x-full');
    
    if (isOpen) {
        sidebar.classList.remove('-translate-x-full');
        overlay?.classList.remove('hidden');
    } else {
        sidebar.classList.add('-translate-x-full');
        overlay?.classList.add('hidden');
    }
    UIState.sidebarOpen = isOpen;
}

// Modal System
function openModal(contentHtml) {
    const modal = document.getElementById('global-modal');
    const modalBody = document.getElementById('modal-body');
    const overlay = modal.querySelector('.modal-overlay');
    const content = modal.querySelector('.modal-content');

    modalBody.innerHTML = contentHtml;
    modal.classList.remove('hidden');
    
    setTimeout(() => {
        overlay.style.opacity = '1';
        content.style.opacity = '1';
        content.style.transform = 'scale(1)';
    }, 10);
    
    UIState.modalOpen = true;
    lucide.createIcons();
}

function closeModal() {
    const modal = document.getElementById('global-modal');
    const overlay = modal.querySelector('.modal-overlay');
    const content = modal.querySelector('.modal-content');

    overlay.style.opacity = '0';
    content.style.opacity = '0';
    content.style.transform = 'scale(0.9)';
    
    setTimeout(() => {
        modal.classList.add('hidden');
    }, 300);
    UIState.modalOpen = false;
}

// Keyboard Shortcuts
function initKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Cmd/Ctrl + K = Search
        if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
            e.preventDefault();
            openGlobalSearch();
        }

        // Cmd/Ctrl + N = Add New product
        if ((e.metaKey || e.ctrlKey) && e.key === 'n') {
            e.preventDefault();
            window.location.href = '/products/new';
        }

        // Esc = Close Modal
        if (e.key === 'Escape' && UIState.modalOpen) {
            closeModal();
        }
    });
}

function openGlobalSearch() {
    showToast("Opening search matrix...", "info");
    // To be implemented in search.js or similar
}

// Ajax Helper with loading state
async function apiRequest(url, method = 'GET', data = null, options = {}) {
    const { showLoading = true, loadingMessage = 'Processing...' } = options;
    
    // Show loading overlay if enabled
    if (showLoading) {
        showLoadingOverlay(loadingMessage);
    }
    
    try {
        const fetchOptions = {
            method,
            headers: { 'Content-Type': 'application/json' }
        };
        if (data) fetchOptions.body = JSON.stringify(data);
        
        const response = await fetch(url, fetchOptions);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        return result;
    } catch (error) {
        showToast(`Request failed: ${error.message}`, 'error');
        return null;
    } finally {
        // Hide loading overlay
        if (showLoading) {
            hideLoadingOverlay();
        }
    }
}

// Loading Overlay Functions
function showLoadingOverlay(message = 'Processing...') {
    let overlay = document.getElementById('loading-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div class="flex flex-col items-center gap-4">
                <div class="spinner"></div>
                <p class="text-sm text-text-secondary" id="loading-message">${message}</p>
            </div>
        `;
        document.body.appendChild(overlay);
    } else {
        const msgEl = document.getElementById('loading-message');
        if (msgEl) msgEl.textContent = message;
    }
    
    // Trigger reflow
    overlay.offsetHeight;
    overlay.classList.add('active');
}

function hideLoadingOverlay() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.classList.remove('active');
        setTimeout(() => overlay.remove(), 300);
    }
}
