/**
 * JARVIS AI Assistant — Reminders Module
 * Handles AJAX-based reminder CRUD operations.
 */
document.addEventListener('DOMContentLoaded', () => {
    const reminderList = document.getElementById('reminderList');
    const addReminderBtn = document.getElementById('addReminderBtn');
    const modalOverlay = document.getElementById('reminderModal');
    const modalForm = document.getElementById('reminderForm');
    const cancelModalBtn = document.getElementById('cancelModal');

    if (!reminderList) return;

    // Get CSRF token from meta tags
    const csrfToken = document.querySelector('meta[name="_csrf"]')?.getAttribute('content');
    const csrfHeader = document.querySelector('meta[name="_csrf_header"]')?.getAttribute('content');

    // Event Listeners
    if (addReminderBtn) {
        addReminderBtn.addEventListener('click', () => openModal());
    }

    if (cancelModalBtn) {
        cancelModalBtn.addEventListener('click', () => closeModal());
    }

    if (modalOverlay) {
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) closeModal();
        });
    }

    if (modalForm) {
        modalForm.addEventListener('submit', handleCreateReminder);
    }

    /**
     * Open the create reminder modal.
     */
    function openModal() {
        if (modalOverlay) {
            modalOverlay.classList.add('active');
            const titleInput = document.getElementById('reminderTitle');
            if (titleInput) titleInput.focus();
        }
    }

    /**
     * Close the modal.
     */
    function closeModal() {
        if (modalOverlay) {
            modalOverlay.classList.remove('active');
        }
        if (modalForm) {
            modalForm.reset();
        }
    }

    /**
     * Handle creating a new reminder.
     */
    async function handleCreateReminder(e) {
        e.preventDefault();

        const title = document.getElementById('reminderTitle').value.trim();
        const reminderTime = document.getElementById('reminderTime').value;

        if (!title || !reminderTime) {
            alert('Please fill in all fields.');
            return;
        }

        try {
            const headers = {
                'Content-Type': 'application/json'
            };
            if (csrfToken && csrfHeader) {
                headers[csrfHeader] = csrfToken;
            }

            const response = await fetch('/api/reminders', {
                method: 'POST',
                headers: headers,
                body: JSON.stringify({
                    title: title,
                    reminderTime: reminderTime + ':00'
                })
            });

            if (!response.ok) throw new Error('Failed to create reminder');

            const data = await response.json();
            addReminderCard(data);
            closeModal();

        } catch (error) {
            console.error('Create reminder error:', error);
            alert('Failed to create reminder. Please try again.');
        }
    }

    /**
     * Add a reminder card to the DOM.
     */
    function addReminderCard(reminder) {
        // Remove empty state if present
        const emptyState = reminderList.querySelector('.empty-state');
        if (emptyState) emptyState.remove();

        const card = document.createElement('div');
        card.className = `reminder-card ${reminder.status ? reminder.status.toLowerCase() : 'pending'}`;
        card.dataset.id = reminder.id;

        const statusClass = (reminder.status || 'PENDING').toLowerCase();
        const formattedTime = formatDateTime(reminder.reminderTime);

        card.innerHTML = `
            <div class="reminder-status-dot ${statusClass}"></div>
            <div class="reminder-info">
                <div class="reminder-title">${escapeHtml(reminder.title)}</div>
                <div class="reminder-time">🕐 ${formattedTime}</div>
            </div>
            <span class="badge ${statusClass}">${statusClass}</span>
            <div class="reminder-actions">
                <button class="btn-complete" onclick="completeReminder(${reminder.id})" title="Mark as complete">✓</button>
                <button class="btn-delete" onclick="deleteReminder(${reminder.id})" title="Delete">✕</button>
            </div>
        `;

        reminderList.prepend(card);
        card.style.animation = 'fadeInUp 0.3s ease-out';
    }

    /**
     * Mark a reminder as completed.
     */
    window.completeReminder = async function(id) {
        try {
            const headers = {
                'Content-Type': 'application/json'
            };
            if (csrfToken && csrfHeader) {
                headers[csrfHeader] = csrfToken;
            }

            const response = await fetch(`/api/reminders/${id}/status`, {
                method: 'PUT',
                headers: headers,
                body: JSON.stringify({ status: 'COMPLETED' })
            });

            if (!response.ok) throw new Error('Failed to update reminder');

            const card = reminderList.querySelector(`[data-id="${id}"]`);
            if (card) {
                card.classList.remove('pending', 'dismissed');
                card.classList.add('completed');
                const dot = card.querySelector('.reminder-status-dot');
                if (dot) { dot.className = 'reminder-status-dot completed'; }
                const badge = card.querySelector('.badge');
                if (badge) { badge.className = 'badge completed'; badge.textContent = 'completed'; }
            }

        } catch (error) {
            console.error('Complete reminder error:', error);
            alert('Failed to update reminder.');
        }
    };

    /**
     * Delete a reminder.
     */
    window.deleteReminder = async function(id) {
        if (!confirm('Are you sure you want to delete this reminder?')) return;

        try {
            const headers = {};
            if (csrfToken && csrfHeader) {
                headers[csrfHeader] = csrfToken;
            }

            const response = await fetch(`/api/reminders/${id}`, {
                method: 'DELETE',
                headers: headers
            });

            if (!response.ok) throw new Error('Failed to delete reminder');

            const card = reminderList.querySelector(`[data-id="${id}"]`);
            if (card) {
                card.style.animation = 'fadeInUp 0.3s ease-out reverse';
                setTimeout(() => card.remove(), 300);
            }

        } catch (error) {
            console.error('Delete reminder error:', error);
            alert('Failed to delete reminder.');
        }
    };

    /**
     * Format ISO datetime to readable string.
     */
    function formatDateTime(dateStr) {
        if (!dateStr) return 'Unknown';
        const date = new Date(dateStr);
        return date.toLocaleString([], {
            month: 'short', day: 'numeric',
            hour: '2-digit', minute: '2-digit'
        });
    }

    /**
     * Escape HTML to prevent XSS.
     */
    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }
});
