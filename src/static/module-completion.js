// Module Completion Tracking
// Adds "Mark as Complete" buttons to salesperson dashboard modules

(function() {
    'use strict';
    
    console.log('[Module Completion] Script loaded');
    
    // Get current user email from the page
    function getCurrentUserEmail() {
        // Try to find email in the page
        const emailElements = document.querySelectorAll('[href^="mailto:"]');
        if (emailElements.length > 0) {
            const mailto = emailElements[0].getAttribute('href');
            return mailto.replace('mailto:', '');
        }
        
        // Fallback: check if there's user info in the page
        const bodyText = document.body.textContent;
        const emailMatch = bodyText.match(/([a-zA-Z0-9._-]+@vertexprivatefunding\.com)/);
        if (emailMatch) {
            return emailMatch[1];
        }
        
        return null;
    }
    
    // Add completion buttons to module cards
    function addCompletionButtons() {
        // Check if we're on the salesperson dashboard
        const currentPath = window.location.pathname;
        if (!currentPath.includes('/salesperson') || currentPath.includes('/resources')) {
            console.log('[Module Completion] Not on salesperson dashboard, skipping');
            return false;
        }
        
        const userEmail = getCurrentUserEmail();
        if (!userEmail) {
            console.log('[Module Completion] Could not determine user email');
            return false;
        }
        
        console.log('[Module Completion] User email:', userEmail);
        
        // Find all module cards (they contain "Module 1", "Module 2", etc.)
        const allCards = document.querySelectorAll('[class*="card"], [class*="Card"], div');
        let moduleCards = [];
        
        for (let card of allCards) {
            const text = card.textContent;
            const moduleMatch = text.match(/Module (\d+)/);
            if (moduleMatch && !card.querySelector('.completion-button')) {
                // Check if this card has module content
                const hasModuleContent = text.includes('Week') || text.includes('Training Guide') || text.includes('Worksheet');
                if (hasModuleContent) {
                    moduleCards.push({
                        element: card,
                        moduleNumber: parseInt(moduleMatch[1])
                    });
                }
            }
        }
        
        if (moduleCards.length === 0) {
            console.log('[Module Completion] No module cards found yet');
            return false;
        }
        
        console.log(`[Module Completion] Found ${moduleCards.length} module cards`);
        
        // Add completion button to each card
        moduleCards.forEach(({element, moduleNumber}) => {
            // Check if button already exists
            if (element.querySelector('.completion-button')) {
                return;
            }
            
            // Create button container
            const buttonContainer = document.createElement('div');
            buttonContainer.style.cssText = 'margin-top: 12px; padding-top: 12px; border-top: 1px solid #e5e7eb;';
            buttonContainer.className = 'completion-button-container';
            
            // Create completion button
            const button = document.createElement('button');
            button.className = 'completion-button';
            button.textContent = '✓ Mark as Complete';
            button.style.cssText = `
                background: linear-gradient(135deg, #2d6a4f 0%, #1e5128 100%);
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
                width: 100%;
            `;
            
            button.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px)';
                this.style.boxShadow = '0 4px 12px rgba(45, 106, 79, 0.3)';
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = 'none';
            });
            
            button.addEventListener('click', async function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                // Disable button during API call
                button.disabled = true;
                button.textContent = '⏳ Saving...';
                button.style.opacity = '0.6';
                
                try {
                    // Call API to mark module as complete
                    const response = await fetch(`/api/progress/salesperson/${encodeURIComponent(userEmail)}/module/${moduleNumber}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            status: 'completed'
                        })
                    });
                    
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    
                    const data = await response.json();
                    console.log('[Module Completion] Module marked as complete:', data);
                    
                    // Update button to show completion
                    button.textContent = '✅ Completed!';
                    button.style.background = '#22c55e';
                    button.style.cursor = 'default';
                    
                    // Add completion indicator to card
                    element.style.background = '#f0fdf4';
                    element.style.borderColor = '#22c55e';
                    
                    // Show success message
                    showNotification(`Module ${moduleNumber} marked as complete!`, 'success');
                    
                } catch (error) {
                    console.error('[Module Completion] Error marking module as complete:', error);
                    
                    // Reset button
                    button.disabled = false;
                    button.textContent = '✓ Mark as Complete';
                    button.style.opacity = '1';
                    
                    // Show error message
                    showNotification('Failed to save progress. Please try again.', 'error');
                }
            });
            
            buttonContainer.appendChild(button);
            
            // Find a good place to insert the button
            // Try to find the last child that's not a button
            let insertPoint = element;
            const children = Array.from(element.children);
            if (children.length > 0) {
                insertPoint = children[children.length - 1];
                insertPoint.parentNode.insertBefore(buttonContainer, insertPoint.nextSibling);
            } else {
                element.appendChild(buttonContainer);
            }
            
            console.log(`[Module Completion] Added completion button for Module ${moduleNumber}`);
        });
        
        return true;
    }
    
    // Show notification message
    function showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 16px 24px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 14px;
            z-index: 10000;
            animation: slideIn 0.3s ease-out;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        
        if (type === 'success') {
            notification.style.background = '#22c55e';
            notification.style.color = 'white';
        } else {
            notification.style.background = '#ef4444';
            notification.style.color = 'white';
        }
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
    
    // Add CSS animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(400px);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Try to add buttons immediately
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(addCompletionButtons, 500);
        });
    } else {
        setTimeout(addCompletionButtons, 500);
    }
    
    // Use MutationObserver to detect when React renders the page
    const observer = new MutationObserver(function(mutations) {
        for (let mutation of mutations) {
            if (mutation.addedNodes.length > 0) {
                // Check if module cards were added
                for (let node of mutation.addedNodes) {
                    if (node.nodeType === 1) { // Element node
                        const text = node.textContent || '';
                        if (text.includes('Module')) {
                            console.log('[Module Completion] Detected module content added');
                            setTimeout(addCompletionButtons, 100);
                            break;
                        }
                    }
                }
            }
        }
    });
    
    // Start observing
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // Also try periodically for the first 10 seconds
    let attempts = 0;
    const maxAttempts = 20;
    const interval = setInterval(function() {
        attempts++;
        if (addCompletionButtons() || attempts >= maxAttempts) {
            clearInterval(interval);
            console.log('[Module Completion] Stopped periodic attempts');
        }
    }, 500);
    
})();
