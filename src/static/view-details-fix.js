// View Details Button Fix
// Makes the "View Details" buttons on the trainer dashboard functional

(function() {
    'use strict';
    
    console.log('[View Details Fix] Script loaded');
    
    // Function to fix View Details buttons
    function fixViewDetailsButtons() {
        // Check if we're on the trainer dashboard
        const currentPath = window.location.pathname;
        if (!currentPath.includes('/trainer') || currentPath.includes('/resources')) {
            console.log('[View Details Fix] Not on trainer dashboard, skipping');
            return false;
        }
        
        // Find all "View Details" buttons
        const allButtons = document.querySelectorAll('button');
        let viewDetailsButtons = Array.from(allButtons).filter(btn => 
            btn.textContent.trim() === 'View Details'
        );
        
        if (viewDetailsButtons.length === 0) {
            console.log('[View Details Fix] No View Details buttons found yet');
            return false;
        }
        
        console.log(`[View Details Fix] Found ${viewDetailsButtons.length} View Details buttons`);
        
        // Fix each button
        viewDetailsButtons.forEach((button, index) => {
            // Check if already fixed
            if (button.dataset.fixed === 'true') {
                return;
            }
            
            // Find the salesperson email (should be in the same card)
            let emailElement = null;
            let currentNode = button.parentElement;
            
            // Search up the DOM tree to find the email
            for (let i = 0; i < 10; i++) {
                if (!currentNode) break;
                
                // Look for email text
                const emailMatch = currentNode.textContent.match(/([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)/);
                if (emailMatch) {
                    emailElement = emailMatch[1];
                    break;
                }
                
                currentNode = currentNode.parentElement;
            }
            
            if (!emailElement) {
                console.log(`[View Details Fix] Could not find email for button ${index}`);
                return;
            }
            
            console.log(`[View Details Fix] Found email: ${emailElement}`);
            
            // Add click handler
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                console.log(`[View Details Fix] Navigating to detail page for ${emailElement}`);
                
                // Navigate to detail page
                const detailUrl = `/salesperson-detail.html?email=${encodeURIComponent(emailElement)}`;
                window.location.href = detailUrl;
            }, true); // Use capture phase
            
            // Mark as fixed
            button.dataset.fixed = 'true';
            
            console.log(`[View Details Fix] Fixed button ${index} for ${emailElement}`);
        });
        
        return true;
    }
    
    // Try to fix buttons immediately
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(fixViewDetailsButtons, 500);
        });
    } else {
        setTimeout(fixViewDetailsButtons, 500);
    }
    
    // Use MutationObserver to detect when React renders the page
    const observer = new MutationObserver(function(mutations) {
        for (let mutation of mutations) {
            if (mutation.addedNodes.length > 0) {
                // Check if View Details buttons were added
                for (let node of mutation.addedNodes) {
                    if (node.nodeType === 1) { // Element node
                        const text = node.textContent || '';
                        if (text.includes('View Details')) {
                            console.log('[View Details Fix] Detected View Details button added');
                            setTimeout(fixViewDetailsButtons, 100);
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
        if (fixViewDetailsButtons() || attempts >= maxAttempts) {
            clearInterval(interval);
            console.log('[View Details Fix] Stopped periodic attempts');
        }
    }, 500);
    
})();
