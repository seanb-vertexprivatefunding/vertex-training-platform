// Override hardcoded authentication with API-based authentication
(function() {
    console.log('Auth override loaded');
    
    // Intercept login form submissions
    document.addEventListener('submit', async function(e) {
        const form = e.target;
        if (form.querySelector('input[type="email"]') && form.querySelector('input[type="password"]')) {
            e.preventDefault();
            
            const email = form.querySelector('input[type="email"]').value;
            const password = form.querySelector('input[type="password"]').value;
            
            try {
                const response = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Store user data in localStorage
                    localStorage.setItem('currentUser', JSON.stringify(data.user));
                    // Reload page to trigger React to pick up the user
                    window.location.reload();
                } else {
                    alert(data.error || 'Invalid email or password');
                }
            } catch (error) {
                console.error('Login error:', error);
                alert('Login failed. Please try again.');
            }
        }
    });
})();
