/**
 * board.js - Kanban Board Drag-and-Drop Functionality
 * 
 * This file uses SortableJS to enable drag-and-drop between task columns.
 * When a task card is dropped into a new column, it sends an AJAX request
 * to update the task's status in the database.
 * 
 * How it works:
 * 1. SortableJS is initialized on each column (todo, in_progress, done)
 * 2. All columns share the same "group" so cards can move between them
 * 3. When a card is dropped, the onEnd callback fires
 * 4. We send a PATCH request to the server with the new status
 * 5. If the request fails, we move the card back to where it was
 */

document.addEventListener('DOMContentLoaded', function() {
    // Get all task column containers
    const columns = document.querySelectorAll('.task-column');
    
    // Initialize SortableJS on each column
    columns.forEach(function(column) {
        new Sortable(column, {
            // 'tasks' group name allows dragging between all columns
            group: 'tasks',
            
            // Animation speed in milliseconds (makes dragging feel smooth)
            animation: 150,
            
            // CSS classes applied during drag operations
            ghostClass: 'sortable-ghost',    // The placeholder where the card will land
            chosenClass: 'sortable-chosen',  // The card being picked up
            dragClass: 'sortable-drag',      // The card while being moved
            
            // Only drag elements with the 'task-card' class (not empty states)
            draggable: '.task-card',
            
            // Called when a card is dropped into any column
            onEnd: function(evt) {
                const taskCard = evt.item;                    // The dragged card element
                const taskId = taskCard.dataset.taskId;       // Task ID from data-task-id attribute
                const newColumn = evt.to;                     // The column it was dropped into
                const oldColumn = evt.from;                   // The column it came from
                const newStatus = newColumn.dataset.status;   // New status from data-status attribute
                
                // Only update if the card actually moved to a different column
                if (newColumn !== oldColumn) {
                    updateTaskStatus(taskId, newStatus, taskCard, oldColumn);
                }
                
                // Hide empty state messages when a column has cards
                updateEmptyStates();
            }
        });
    });
    
    // Initial check for empty states
    updateEmptyStates();
});


/**
 * Send an AJAX PATCH request to update a task's status in the database.
 * 
 * If the request fails (network error or server error), the card is
 * automatically moved back to its original column.
 * 
 * @param {string} taskId - The ID of the task to update
 * @param {string} newStatus - The new status ('todo', 'in_progress', or 'done')
 * @param {HTMLElement} taskCard - The task card DOM element
 * @param {HTMLElement} originalColumn - The column the card was dragged from
 */
function updateTaskStatus(taskId, newStatus, taskCard, originalColumn) {
    fetch(`/tasks/${taskId}/status`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            // CSRF token prevents unauthorized requests (security feature)
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ status: newStatus })
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        if (data.success) {
            // Show a brief green flash animation to confirm the update
            taskCard.classList.add('status-updated');
            setTimeout(function() {
                taskCard.classList.remove('status-updated');
            }, 1000);
            
            // Update the count badges in column headers
            updateColumnCounts();
        } else {
            // Server returned an error - move the card back
            console.error('Failed to update task:', data.error);
            originalColumn.appendChild(taskCard);
            updateColumnCounts();
            updateEmptyStates();
            showToast('Failed to update task status: ' + (data.error || 'Unknown error'), 'danger');
        }
    })
    .catch(function(error) {
        // Network error - move the card back to its original column
        console.error('Network error:', error);
        originalColumn.appendChild(taskCard);
        updateColumnCounts();
        updateEmptyStates();
        showToast('Network error. Please check your connection and try again.', 'danger');
    });
}


/**
 * Get the CSRF token from the meta tag in the HTML head.
 * 
 * CSRF (Cross-Site Request Forgery) protection ensures that only
 * requests from our own pages are accepted by the server.
 * 
 * @returns {string} The CSRF token value
 */
function getCSRFToken() {
    const metaTag = document.querySelector('meta[name="csrf-token"]');
    return metaTag ? metaTag.getAttribute('content') : '';
}


/**
 * Update the task count badges displayed in each column header.
 * Called after any drag-and-drop operation.
 */
function updateColumnCounts() {
    const columns = document.querySelectorAll('.task-column');
    columns.forEach(function(column) {
        const count = column.querySelectorAll('.task-card').length;
        const status = column.dataset.status;
        const badge = document.getElementById(status + '-count');
        if (badge) {
            badge.textContent = count;
        }
    });
}


/**
 * Show or hide the "empty state" messages in each column.
 * If a column has task cards, the empty message is hidden.
 * If a column is empty, the message is shown.
 */
function updateEmptyStates() {
    const columns = document.querySelectorAll('.task-column');
    columns.forEach(function(column) {
        const cards = column.querySelectorAll('.task-card');
        const emptyState = column.querySelector('.empty-state');
        
        if (emptyState) {
            // Hide empty state if there are cards, show if empty
            emptyState.style.display = cards.length > 0 ? 'none' : 'block';
        }
    });
}


/**
 * Show a temporary notification message (toast) to the user.
 * Used to display error messages when drag-and-drop fails.
 * 
 * @param {string} message - The message to display
 * @param {string} type - Bootstrap alert type ('success', 'danger', 'warning', 'info')
 */
function showToast(message, type) {
    // Create an alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Add it to the flash messages container
    const container = document.querySelector('.container.mt-3');
    if (container) {
        container.appendChild(alertDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(function() {
            alertDiv.remove();
        }, 5000);
    }
}
