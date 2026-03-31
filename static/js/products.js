/**
 * StockFlow Asset Registry Logic (AJAX Quick Adjust)
 */

document.addEventListener('DOMContentLoaded', () => {
    initQuickAdjust();
    initSearch();
    initBulkActions();
});

function initQuickAdjust() {
    document.querySelectorAll('.adjust-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const id = btn.getAttribute('data-id');
            const delta = parseInt(btn.getAttribute('data-delta'));
            const quantityEl = document.getElementById(`qty-${id}`);
            
            // UI Optimistic Update
            let currentQty = parseInt(quantityEl.innerText);
            let nextQty = currentQty + delta;
            if (nextQty < 0) return showToast("Cannot reduce below zero.", "warning");
            
            quantityEl.innerText = nextQty;
            quantityEl.classList.add('text-primary', 'scale-110');
            
            const result = await apiRequest(`/products/${id}/adjust`, 'POST', { delta });
            
            if (result && result.success) {
                showToast(`${result.name} updated: ${result.new_quantity}`, 'success');
                // Update status badge if threshold crossed
                updateStatusBadge(id, result.new_quantity, result.threshold);
            } else {
                // Revert on failure
                quantityEl.innerText = currentQty;
                showToast("Update failed. Reverting...", "error");
            }
            
            setTimeout(() => quantityEl.classList.remove('text-primary', 'scale-110'), 500);
        });
    });
}

function updateStatusBadge(id, qty, threshold) {
    const badge = document.getElementById(`badge-${id}`);
    if (!badge) return;

    if (qty <= 0) {
        badge.className = 'badge badge-danger';
        badge.innerText = 'Out of Stock';
    } else if (qty <= threshold) {
        badge.className = 'badge badge-warning';
        badge.innerText = 'Low Stock';
    } else {
        badge.className = 'badge badge-success';
        badge.innerText = 'Nominal';
    }
}

function initSearch() {
    const searchInput = document.getElementById('asset-search');
    const tableRows = document.querySelectorAll('tbody tr');

    searchInput?.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        
        tableRows.forEach(row => {
            const text = row.innerText.toLowerCase();
            row.style.display = text.includes(query) ? '' : 'none';
        });
    });
}

function initBulkActions() {
    const mainCheck = document.getElementById('select-all-assets');
    const rowChecks = document.querySelectorAll('.asset-checkbox');
    const bulkBar = document.getElementById('bulk-actions-bar');
    const countDisplay = document.getElementById('selected-count');

    mainCheck?.addEventListener('change', (e) => {
        rowChecks.forEach(c => c.checked = e.target.checked);
        updateBulkBar();
    });

    rowChecks.forEach(c => c.addEventListener('change', updateBulkBar));

    function updateBulkBar() {
        const selected = Array.from(rowChecks).filter(c => c.checked);
        if (selected.length > 0) {
            bulkBar.classList.remove('translate-y-20', 'opacity-0');
            countDisplay.innerText = selected.length;
        } else {
            bulkBar.classList.add('translate-y-20', 'opacity-0');
        }
    }
}

function deleteProduct(productId) {
    const modalContent = `
        <div class="text-center">
            <div class="w-16 h-16 rounded-full bg-danger/10 flex items-center justify-center mx-auto mb-4">
                <i data-lucide="alert-triangle" class="w-8 h-8 text-danger"></i>
            </div>
            <h3 class="text-xl font-display font-bold text-white mb-2">Confirm Deletion</h3>
            <p class="text-sm text-text-secondary mb-6">This action will permanently remove the asset. This cannot be undone.</p>
            <div class="flex gap-3 justify-center">
                <button onclick="closeModal()" class="btn bg-white/5 border border-white/10 text-white hover:bg-white/10 px-4 py-2 rounded-lg">
                    Cancel
                </button>
                <button onclick="confirmDelete('${productId}')" class="btn btn-danger px-4 py-2 rounded-lg">
                    Delete Asset
                </button>
            </div>
        </div>
    `;
    openModal(modalContent);
    lucide.createIcons();
}

async function confirmDelete(productId) {
    closeModal();
    try {
        const response = await fetch(`/products/${productId}/delete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });
        
        if (response.ok) {
            showToast('Asset successfully removed from registry', 'success');
            const btn = document.querySelector(`button[onclick="deleteProduct('${productId}')"]`);
            if (btn) {
                const row = btn.closest('tr');
                row.style.opacity = '0';
                setTimeout(() => row.remove(), 300);
            }
        } else {
            showToast('Failed to delete asset', 'error');
        }
    } catch (error) {
        showToast('Network error. Please try again.', 'error');
    }
}
