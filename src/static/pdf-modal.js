// Enhanced PDF Modal System for Vertex Training Platform
// Handles both static and React-rendered buttons
(function() {
    'use strict';
    
    // Create modal HTML
    const modalHTML = `
        <div id="pdf-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 10000; backdrop-filter: blur(5px);">
            <div style="position: relative; width: 90%; height: 90%; margin: 2.5% auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.3);">
                <div style="background: linear-gradient(135deg, #1a5f3f 0%, #2d8659 100%); padding: 20px; display: flex; justify-content: space-between; align-items: center;">
                    <h2 style="color: white; margin: 0; font-size: 24px;">Training Material</h2>
                    <button id="close-pdf-modal" style="background: rgba(255,255,255,0.2); border: 2px solid white; color: white; width: 40px; height: 40px; border-radius: 50%; font-size: 24px; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.3s;">×</button>
                </div>
                <iframe id="pdf-iframe" style="width: 100%; height: calc(100% - 80px); border: none;"></iframe>
            </div>
        </div>
    `;
    
    // Add modal to page when DOM is ready
    function initModal() {
        if (document.getElementById('pdf-modal')) return;
        
        const div = document.createElement('div');
        div.innerHTML = modalHTML;
        document.body.appendChild(div.firstElementChild);
        
        // Close button handler
        document.getElementById('close-pdf-modal').addEventListener('click', closePDFModal);
        
        // Close on overlay click
        document.getElementById('pdf-modal').addEventListener('click', function(e) {
            if (e.target.id === 'pdf-modal') {
                closePDFModal();
            }
        });
        
        // Close on Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && document.getElementById('pdf-modal').style.display === 'block') {
                closePDFModal();
            }
        });
        
        console.log('PDF modal system initialized');
    }
    
    // Open PDF in modal
    window.openPDFModal = function(pdfUrl, title) {
        const modal = document.getElementById('pdf-modal');
        const iframe = document.getElementById('pdf-iframe');
        const titleEl = modal.querySelector('h2');
        
        if (title) {
            titleEl.textContent = title;
        }
        
        iframe.src = pdfUrl;
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
        console.log('Opening PDF:', pdfUrl, title);
    };
    
    // Close PDF modal
    window.closePDFModal = function() {
        const modal = document.getElementById('pdf-modal');
        const iframe = document.getElementById('pdf-iframe');
        
        modal.style.display = 'none';
        iframe.src = '';
        document.body.style.overflow = '';
    };
    
    // Function to handle button clicks
    function handleButtonClick(button, e) {
        const buttonText = button.textContent.trim();
        console.log('Button clicked:', buttonText);
        
        // Check if this is a training material button on module page
        if (buttonText.includes('One-Page Summary')) {
            if (e) {
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
            }
            openPDFModal('/training-materials/Module_01_One_Page_Summary.pdf', 'Module 1: One-Page Summary');
            return true;
        } else if (buttonText.includes('Action Worksheet')) {
            if (e) {
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
            }
            openPDFModal('/training-materials/Module_01_Action_Worksheet.pdf', 'Module 1: Action Worksheet');
            return true;
        } else if (buttonText.includes('Script Templates')) {
            if (e) {
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
            }
            openPDFModal('/training-materials/Module_01_Sales_Mindset_Training_Guide.pdf', 'Module 1: Training Guide');
            return true;
        }
        // Handle trainer resource page buttons
        else if (buttonText.includes('Training Guide')) {
            if (e) {
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
            }
            
            // Determine which module based on context
            const moduleCard = button.closest('[class*="Module"]') || button.closest('div');
            const cardText = moduleCard ? moduleCard.textContent : '';
            
            console.log('Training Guide button - Card text:', cardText);
            
            if (cardText.includes('Module 1') || cardText.includes('Sales Mindset')) {
                openPDFModal('/training-materials/Module_01_Sales_Mindset_Training_Guide.pdf', 'Module 1: Training Guide');
            } else if (cardText.includes('Module 2') || cardText.includes('Understanding Your Buyer')) {
                openPDFModal('/training-materials/Module_02_Understanding_Buyer_Training_Guide.pdf', 'Module 2: Training Guide');
            }
            return true;
        } else if (buttonText.includes('Worksheet') && !buttonText.includes('Action')) {
            if (e) {
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
            }
            
            // Determine which module based on context
            const moduleCard = button.closest('[class*="Module"]') || button.closest('div');
            const cardText = moduleCard ? moduleCard.textContent : '';
            
            console.log('Worksheet button - Card text:', cardText);
            
            // Extract module number from context
            const moduleMatch = cardText.match(/Module (\d+)/);
            if (moduleMatch) {
                const moduleNum = moduleMatch[1].padStart(2, '0');
                openPDFModal(`/training-materials/Module_${moduleNum}_Worksheet.pdf`, `Module ${parseInt(moduleNum)}: Worksheet`);
            }
            return true;
        }
        
        return false;
    }
    
    // Attach click handlers to buttons
    function attachButtonHandlers() {
        const buttons = document.querySelectorAll('button');
        buttons.forEach(button => {
            // Skip if already processed
            if (button.dataset.pdfHandlerAttached) return;
            
            const buttonText = button.textContent.trim();
            
            // Check if this is a training material button
            if (buttonText.includes('One-Page Summary') ||
                buttonText.includes('Action Worksheet') ||
                buttonText.includes('Script Templates') ||
                buttonText.includes('Training Guide') ||
                (buttonText.includes('Worksheet') && !buttonText.includes('Action'))) {
                
                console.log('Attaching handler to button:', buttonText);
                
                // Mark as processed
                button.dataset.pdfHandlerAttached = 'true';
                
                // Add click handler with highest priority
                button.addEventListener('click', function(e) {
                    console.log('Direct click handler triggered for:', buttonText);
                    handleButtonClick(button, e);
                }, true); // Capture phase
                
                // Also add a regular listener as backup
                button.addEventListener('click', function(e) {
                    console.log('Backup click handler triggered for:', buttonText);
                    handleButtonClick(button, e);
                }, false);
            }
        });
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            initModal();
            attachButtonHandlers();
        });
    } else {
        initModal();
        attachButtonHandlers();
    }
    
    // Global click interceptor (capture phase - highest priority)
    document.addEventListener('click', function(e) {
        const button = e.target.closest('button');
        if (!button) return;
        
        if (handleButtonClick(button, e)) {
            console.log('Global interceptor handled button');
        }
    }, true); // Use capture phase to intercept before React
    
    // MutationObserver to handle dynamically added buttons (React rendering)
    const observer = new MutationObserver(function(mutations) {
        let shouldAttach = false;
        
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length > 0) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) { // Element node
                        if (node.tagName === 'BUTTON' || node.querySelector('button')) {
                            shouldAttach = true;
                        }
                    }
                });
            }
        });
        
        if (shouldAttach) {
            console.log('New buttons detected, attaching handlers');
            attachButtonHandlers();
        }
    });
    
    // Start observing when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
            console.log('MutationObserver started');
        });
    } else {
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
        console.log('MutationObserver started');
    }
    
    // Re-attach handlers periodically as a safety net
    setInterval(attachButtonHandlers, 1000);
    
})();

