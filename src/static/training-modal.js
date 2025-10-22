/**
 * Training Materials Modal Integration
 * Provides popup/modal functionality for viewing web-based training materials
 */

(function() {
    'use strict';

    // Create modal HTML structure
    function createModal() {
        const modalHTML = `
            <div id="training-material-modal" class="training-modal" style="display: none;">
                <div class="training-modal-overlay" onclick="closeTrainingModal()"></div>
                <div class="training-modal-content">
                    <div class="training-modal-header">
                        <button class="training-modal-close" onclick="closeTrainingModal()" aria-label="Close">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <line x1="18" y1="6" x2="6" y2="18"></line>
                                <line x1="6" y1="6" x2="18" y2="18"></line>
                            </svg>
                        </button>
                    </div>
                    <div class="training-modal-body">
                        <iframe id="training-material-iframe" src="" frameborder="0"></iframe>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
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

            /* Loading state */
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
        `;
        document.head.appendChild(style);
    }

    // Open training material in modal
    window.openTrainingMaterial = function(materialId) {
        const modal = document.getElementById('training-material-modal');
        const iframe = document.getElementById('training-material-iframe');
        
        if (!modal || !iframe) {
            console.error('Training modal not initialized');
            return;
        }

        // Show loading state
        const modalBody = modal.querySelector('.training-modal-body');
        modalBody.innerHTML = `
            <div class="training-modal-loading">
                <div class="training-modal-loading-spinner"></div>
                <p>Loading training material...</p>
            </div>
            <iframe id="training-material-iframe" src="" frameborder="0" style="display: none;"></iframe>
        `;

        // Load the training material
        const newIframe = document.getElementById('training-material-iframe');
        newIframe.src = `/api/training/materials/${materialId}`;
        
        // Show iframe when loaded
        newIframe.onload = function() {
            modalBody.querySelector('.training-modal-loading')?.remove();
            newIframe.style.display = 'block';
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
            
            // Clear iframe to stop any loading
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

    // Intercept clicks on training material links
    function interceptTrainingLinks() {
        // Find all links to training materials
        document.addEventListener('click', function(e) {
            const target = e.target.closest('a[href*="/training-materials/"]');
            if (target) {
                e.preventDefault();
                
                // Extract material info from href
                const href = target.getAttribute('href');
                const filename = href.split('/').pop();
                
                // Map PDF filename to material ID
                const materialMap = {
                    'Module_01_One_Page_Summary.pdf': 1,
                    'Module_01_Action_Worksheet.pdf': 2,
                    // More mappings will be added as modules are populated
                };
                
                const materialId = materialMap[filename];
                if (materialId) {
                    openTrainingMaterial(materialId);
                } else {
                    // Fallback to direct PDF download if not in database
                    window.open(href, '_blank');
                }
            }
        });

        // Also intercept button clicks with data-material-id attribute
        document.addEventListener('click', function(e) {
            const target = e.target.closest('[data-material-id]');
            if (target) {
                e.preventDefault();
                const materialId = target.getAttribute('data-material-id');
                openTrainingMaterial(materialId);
            }
        });
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            createStyles();
            createModal();
            interceptTrainingLinks();
        });
    } else {
        createStyles();
        createModal();
        interceptTrainingLinks();
    }

})();

