// Dashboard Resources Injector
// Adds DSCR Calculator and Loan Program Guidelines buttons to the Additional Resources section

(function() {
    'use strict';
    
    console.log('[Dashboard Resources] Script loaded');
    
    // Function to add resource buttons
    function addResourceButtons() {
        // Check if we're on the resources page
        const currentPath = window.location.pathname;
        if (!currentPath.includes('/resources')) {
            console.log('[Dashboard Resources] Not on resources page, skipping');
            return;
        }
        
        // Find the Additional Resources section
        const additionalResourcesHeading = Array.from(document.querySelectorAll('h3, h2, div')).find(el => 
            el.textContent.trim() === 'Additional Resources'
        );
        
        if (!additionalResourcesHeading) {
            console.log('[Dashboard Resources] Additional Resources section not found yet');
            return false;
        }
        
        console.log('[Dashboard Resources] Found Additional Resources section');
        
        // Find the container with the resource buttons (should be the next sibling or nearby)
        let resourceContainer = additionalResourcesHeading.nextElementSibling;
        
        // If not found, try to find by looking for existing resource buttons
        if (!resourceContainer || !resourceContainer.querySelector('button')) {
            const existingButtons = document.querySelectorAll('button');
            for (let btn of existingButtons) {
                if (btn.textContent.includes('Trainer Implementation Guide') || 
                    btn.textContent.includes('Loan Products Comparison')) {
                    resourceContainer = btn.parentElement;
                    break;
                }
            }
        }
        
        if (!resourceContainer) {
            console.log('[Dashboard Resources] Resource container not found');
            return false;
        }
        
        console.log('[Dashboard Resources] Found resource container');
        
        // Check if buttons already exist
        const existingDSCRButton = Array.from(resourceContainer.querySelectorAll('button')).find(btn =>
            btn.textContent.includes('DSCR Calculator')
        );
        
        if (existingDSCRButton) {
            console.log('[Dashboard Resources] Buttons already added');
            return true;
        }
        
        // Get the style from existing buttons
        const existingButton = resourceContainer.querySelector('button');
        if (!existingButton) {
            console.log('[Dashboard Resources] No existing button to copy style from');
            return false;
        }
        
        // Create DSCR Calculator button
        const dscrButton = existingButton.cloneNode(true);
        dscrButton.innerHTML = `
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
            </svg>
            <div>
                <div style="font-weight: 600;">📊 DSCR Calculator</div>
                <div style="font-size: 0.875rem; opacity: 0.8;">Calculate debt service coverage ratio</div>
            </div>
        `;
        dscrButton.onclick = function(e) {
            e.preventDefault();
            window.open('https://dscrcalc-nscrbdlc.manus.space/', '_blank');
        };
        
        // Create Loan Program Guidelines button
        const guidelinesButton = existingButton.cloneNode(true);
        guidelinesButton.innerHTML = `
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            <div>
                <div style="font-weight: 600;">📋 Loan Program Guidelines</div>
                <div style="font-size: 0.875rem; opacity: 0.8;">Complete lender program reference</div>
            </div>
        `;
        guidelinesButton.onclick = function(e) {
            e.preventDefault();
            window.open('/loan-guidelines.html', '_blank');
        };
        
        // Add the buttons to the container
        resourceContainer.appendChild(dscrButton);
        resourceContainer.appendChild(guidelinesButton);
        
        console.log('[Dashboard Resources] Successfully added DSCR Calculator and Loan Guidelines buttons');
        return true;
    }
    
    // Try to add buttons immediately
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(addResourceButtons, 500);
        });
    } else {
        setTimeout(addResourceButtons, 500);
    }
    
    // Use MutationObserver to detect when React renders the page
    const observer = new MutationObserver(function(mutations) {
        for (let mutation of mutations) {
            if (mutation.addedNodes.length > 0) {
                // Check if Additional Resources section was added
                for (let node of mutation.addedNodes) {
                    if (node.nodeType === 1) { // Element node
                        const text = node.textContent || '';
                        if (text.includes('Additional Resources') || text.includes('Trainer Implementation Guide')) {
                            console.log('[Dashboard Resources] Detected Additional Resources section added');
                            setTimeout(addResourceButtons, 100);
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
        if (addResourceButtons() || attempts >= maxAttempts) {
            clearInterval(interval);
            console.log('[Dashboard Resources] Stopped periodic attempts');
        }
    }, 500);
    
})();
