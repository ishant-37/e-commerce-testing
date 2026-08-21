/**
 * E-Commerce QA Project — Main JavaScript
 * Handles client-side interactions: cart, alerts, navigation.
 */

// ============================================================
// Alert / Notification System
// ============================================================

/**
 * Display a flash alert message at the top of the page.
 * @param {string} message - The message to display.
 * @param {string} type - 'success', 'error', or 'info'.
 */
function showAlert(message, type = 'info') {
    const container = document.getElementById('alert-container');
    const alert = document.createElement('div');
    alert.className = `flash flash-${type}`;
    alert.textContent = message;
    container.innerHTML = '';
    container.appendChild(alert);

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 300);
    }, 5000);
}

/**
 * Show a validation error message for a specific form field.
 * @param {string} fieldId - The ID of the input field.
 * @param {string} message - The error message.
 */
function showFieldError(fieldId, message) {
    const errorEl = document.getElementById(fieldId + '-error');
    if (errorEl) {
        errorEl.textContent = message;
    }
    const inputEl = document.getElementById(fieldId);
    if (inputEl) {
        inputEl.style.borderColor = '#dc2626';
    }
}

/**
 * Clear all form field validation errors.
 */
function clearErrors() {
    document.querySelectorAll('.form-error').forEach(el => el.textContent = '');
    document.querySelectorAll('.form-input').forEach(el => el.style.borderColor = '');
}

// ============================================================
// Navigation
// ============================================================

/**
 * Toggle mobile navigation menu.
 */
function toggleMobileMenu() {
    const mobile = document.getElementById('nav-mobile');
    mobile.classList.toggle('active');
}

// ============================================================
// Logout
// ============================================================

/**
 * Log out the current user via API call.
 */
async function logout() {
    try {
        const response = await fetch('/api/logout', { method: 'POST' });
        if (response.ok) {
            window.location.href = '/login';
        }
    } catch (error) {
        showAlert('Logout failed. Please try again.', 'error');
    }
}

// ============================================================
// Cart Operations
// ============================================================

/**
 * Add a product to the cart.
 * @param {number} productId - The product ID to add.
 * @param {number} quantity - Quantity to add (default 1).
 */
async function addToCart(productId, quantity = 1) {
    try {
        const response = await fetch('/api/cart', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ product_id: productId, quantity: quantity })
        });

        const data = await response.json();

        if (response.ok) {
            showAlert('Product added to cart!', 'success');
        } else if (response.status === 401) {
            window.location.href = '/login';
        } else {
            showAlert(data.error || 'Failed to add to cart', 'error');
        }
    } catch (error) {
        showAlert('Network error. Please try again.', 'error');
    }
}

/**
 * Update the quantity of a cart item.
 * @param {number} itemId - The cart item ID.
 * @param {number} newQuantity - The new quantity.
 */
async function updateCartItem(itemId, newQuantity) {
    if (newQuantity < 1) {
        removeCartItem(itemId);
        return;
    }

    try {
        const response = await fetch(`/api/cart/${itemId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ quantity: newQuantity })
        });

        if (response.ok) {
            // Reload page to reflect updated quantities and totals
            window.location.reload();
        } else {
            const data = await response.json();
            showAlert(data.error || 'Failed to update cart', 'error');
        }
    } catch (error) {
        showAlert('Network error. Please try again.', 'error');
    }
}

/**
 * Remove an item from the cart.
 * @param {number} itemId - The cart item ID to remove.
 */
async function removeCartItem(itemId) {
    try {
        const response = await fetch(`/api/cart/${itemId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            window.location.reload();
        } else {
            const data = await response.json();
            showAlert(data.error || 'Failed to remove item', 'error');
        }
    } catch (error) {
        showAlert('Network error. Please try again.', 'error');
    }
}
