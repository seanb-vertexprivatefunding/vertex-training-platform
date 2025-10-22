// Simple PDF Modal System for Vertex Training Platform
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
    };
    
    // Close PDF modal
    window.closePDFModal = function() {
        const modal = document.getElementById('pdf-modal');
        const iframe = document.getElementById('pdf-iframe');
        
        modal.style.display = 'none';
        iframe.src = '';
        document.body.style.overflow = '';
    };
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initModal);
    } else {
        initModal();
    }
    
    // Intercept clicks on training material buttons
    document.addEventListener('click', function(e) {
        const button = e.target.closest('button');
        if (!button) return;
        
        const buttonText = button.textContent;
        
        // Check if this is a training material button
        if (buttonText.includes('One-Page Summary')) {
            e.preventDefault();
            e.stopPropagation();
            openPDFModal('/training-materials/Module_01_One_Page_Summary.pdf', 'Module 1: One-Page Summary');
        } else if (buttonText.includes('Action Worksheet')) {
            e.preventDefault();
            e.stopPropagation();
            openPDFModal('/training-materials/Module_01_Action_Worksheet.pdf', 'Module 1: Action Worksheet');
        } else if (buttonText.includes('Script Templates')) {
            e.preventDefault();
            e.stopPropagation();
            openPDFModal('/training-materials/Module_01_Sales_Mindset_Training_Guide.pdf', 'Module 1: Training Guide');
        }
    }, true); // Use capture phase to intercept before React
    
})();

