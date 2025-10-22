/**
 * Enhanced Training Materials Modal Integration
 * Intercepts React button clicks and opens materials in modal
 */

(function() {
    'use strict';

    // Material mapping - maps button text to material IDs
    const MATERIAL_MAP = {
        'One-Page Summary (PDF)': 1,
        'Action Worksheet (PDF)': 2,
        'Script Templates (PDF)': null, // Not yet in database
        // Add more as modules are populated
    };

    // Create modal HTML structure
    function createModal() {
        const modalHTML = `
            <div id="training-material-modal" class="training-modal" style="display: none;">
                <div class="training-modal-overlay"></div>
                <div class="training-modal-content">
                    <div class="training-modal-header">
                        <button class="training-modal-close" aria-label="Close">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <line x1="18" y1="6" x2="6" y2="18"></line>
                                <line x1="6" y1="6" x2="18" y2="18"></line>
                            </svg>
                        </button>
                    </div>
                    <div class="training-modal-body">
                        <div class="training-modal-loading">
                            <div class="training-modal-loading-spinner"></div>
                            <p>Loading training material...</p>
                        </div>
                        <iframe id="training-material-iframe" src="" frameborder="0" style="display: none;"></iframe>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Add event listeners
        const modal = document.getElementById('training-material-modal');
        const overlay = modal.querySelector('.training-modal-overlay');
        const closeBtn = modal.querySelector('.training-modal-close');
        
        overlay.addEventListener('click', closeTrainingModal);
        closeBtn.addEventListener('click', closeTrainingModal);
    }

    // Create modal styles
    function createStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .training-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 9999;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .training-modal-overlay {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.75);
                backdrop-filter: blur(4px);
                cursor: pointer;
            }

            .training-modal-content {
                position: relative;
                width: 95%;
                height: 95%;
                max-width: 1400px;
                max-height: 90vh;
                background: white;
                border-radius: 12px;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
                display: flex;
                flex-direction: column;
                overflow: hidden;
                animation: modalSlideIn 0.3s ease-out;
            }

            @keyframes modalSlideIn {
                from {
                    opacity: 0;
                    transform: scale(0.95) translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: scale(1) translateY(0);
                }
            }

            .training-modal-header {
                position: relative;
                padding: 16px 20px;
                background: linear-gradient(135deg, #2d5f3f 0%, #1e4229 100%);
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }

            .training-modal-close {
                position: absolute;
                top: 16px;
                right: 20px;
                background: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 6px;
                width: 36px;
                height: 36px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                color: white;
                transition: all 0.2s ease;
            }

            .training-modal-close:hover {
                background: rgba(255, 255, 255, 0.2);
                transform: scale(1.05);
            }

            .training-modal-close:active {
                transform: scale(0.95);
            }

            .training-modal-body {
                flex: 1;
                overflow: hidden;
                position: relative;
            }

            #training-material-iframe {
                width: 100%;
                height: 100%;
                border: none;
            }

            .training-modal-loading {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                text-align: center;
                color: #2d5f3f;
            }

            .training-modal-loading-spinner {
                width: 50px;
                height: 50px;
                border: 4px solid #e5e7eb;
                border-top-color: #2d5f3f;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin: 0 auto 16px;
            }

            @keyframes spin {
                to { transform: rotate(360deg); }
            }

            /* Mobile responsive */
            @media (max-width: 768px) {
                .training-modal-content {
                    width: 100%;
                    height: 100%;
                    max-width: 100%;
                    max-height: 100%;
                    border-radius: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }

    // Open training material in modal
    window.openTrainingMaterial = function(materialId) {
        const modal = document.getElementById('training-material-modal');
        const iframe = document.getElementById('training-material-iframe');
        const loading = modal.querySelector('.training-modal-loading');
        
        if (!modal || !iframe) {
            console.error('Training modal not initialized');
            return;
        }

        // Reset state
        loading.style.display = 'block';
        iframe.style.display = 'none';
        iframe.src = '';

        // Load the training material
        iframe.src = `/api/training/materials/${materialId}`;
        
        // Show iframe when loaded
        iframe.onload = function() {
            loading.style.display = 'none';
            iframe.style.display = 'block';
        };

        // Show modal
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    };

    // Close modal
    window.closeTrainingModal = function() {
        const modal = document.getElementById('training-material-modal');
        if (modal) {
            modal.style.display = 'none';
            document.body.style.overflow = '';
            
            // Clear iframe
            const iframe = document.getElementById('training-material-iframe');
            if (iframe) {
                iframe.src = '';
            }
        }
    };

    // Close modal on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeTrainingModal();
        }
    });

    // Intercept button clicks using event delegation
    function setupButtonInterceptor() {
        document.addEventListener('click', function(e) {
            // Check if clicked element is a button or inside a button
            const button = e.target.closest('button');
            if (!button) return;

            const buttonText = button.textContent.trim();
            
            // Check if this is a training material button
            if (buttonText in MATERIAL_MAP) {
                const materialId = MATERIAL_MAP[buttonText];
                
                if (materialId) {
                    // Prevent default React behavior
                    e.preventDefault();
                    e.stopPropagation();
                    
                    // Open in modal
                    openTrainingMaterial(materialId);
                } else {
                    // Material not in database yet, let it fall through to PDF download
                    console.log('Material not yet in database:', buttonText);
                }
            }
        }, true); // Use capture phase to intercept before React
    }

    // Initialize when DOM is ready
    function init() {
        createStyles();
        createModal();
        setupButtonInterceptor();
        console.log('Training modal system initialized');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();

