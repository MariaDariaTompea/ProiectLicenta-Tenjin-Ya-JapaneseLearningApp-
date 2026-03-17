"""Login and registration page templates"""

def get_login_page_html():
    """Generate HTML login page with animated transitions"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Japanese App - Login</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
        <style>
            body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; position: relative; overflow: hidden; }
            #bgVideo { position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; object-position: center bottom; z-index: -1; }
            .container { width: 350px; height: 400px; perspective: 1000px; }
            
            .form-container { background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 100%; position: absolute; transition: all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55); }
            
            #loginForm { top: 0; opacity: 1; }
            #loginForm.slide-up { top: -500px; opacity: 0; }
            
            #registerForm { top: 500px; opacity: 0; }
            #registerForm.slide-down { top: 0; opacity: 1; }
            
            h1 { font-family: 'Playfair Display', serif; text-align: center; color: #300825; margin-bottom: 10px; font-size: 28px; margin-top: 0; font-weight: 700; }
            .subtitle { text-align: center; color: #300825; margin-bottom: 25px; font-size: 14px; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; color: #300825; font-weight: bold; }
            input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; font-size: 14px; }
            button { width: 100%; padding: 12px; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 16px; margin-top: 10px; }
            .login-btn { background-color: #EF87BE; color: white; }
            .login-btn:hover { background-color: #e870b1; }
            .register-btn { background-color: #EF87BE; color: white; }
            .register-btn:hover { background-color: #e870b1; }
            .create-account { text-align: center; margin-top: 20px; font-size: 14px; color: #300825; }
            .create-account a { color: #EF87BE; text-decoration: none; font-weight: bold; cursor: pointer; }
            .create-account a:hover { text-decoration: underline; }
            .back-login { text-align: center; margin-top: 20px; font-size: 14px; color: #300825; }
            .back-login a { color: #EF87BE; text-decoration: none; font-weight: bold; cursor: pointer; }
            .back-login a:hover { text-decoration: underline; }
            .error { color: #dc3545; font-size: 12px; margin-top: 5px; }
            .fade-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: black; opacity: 0; pointer-events: none; z-index: 9999; transition: opacity 0.8s ease; }
            .fade-overlay.active { opacity: 1; pointer-events: all; }
        </style>
    </head>
    <body>
        <video id="bgVideo" autoplay muted loop>
            <source src="/videos/kitsune.mp4" type="video/mp4">
            <source src="/videos/kitsune.webm" type="video/webm">
        </video>
        
        <div class="fade-overlay" id="fadeOverlay"></div>
        <div class="container">
            <form class="form-container" id="loginForm">
                <h1>Japanese Learning App</h1>
                <p class="subtitle">Welcome back! Login to continue</p>
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <div id="loginError" class="error"></div>
                <button type="submit" class="login-btn">Login</button>
                <div class="create-account">
                    You don't have an account? <a onclick="switchToRegister()">Create one!</a>
                </div>
            </form>
            
            <form class="form-container" id="registerForm">
                <h1>Create Account</h1>
                <p class="subtitle">Join us to start learning Japanese!</p>
                <div class="form-group">
                    <label for="regName">Full Name:</label>
                    <input type="text" id="regName" name="name" required>
                </div>
                <div class="form-group">
                    <label for="regEmail">Email:</label>
                    <input type="email" id="regEmail" name="email" required>
                </div>
                <div class="form-group">
                    <label for="regPassword">Password:</label>
                    <input type="password" id="regPassword" name="password" required>
                </div>
                <div id="registerError" class="error"></div>
                <button type="submit" class="register-btn">Create Account</button>
                <div class="back-login">
                    Already have an account? <a onclick="switchToLogin()">Login here</a>
                </div>
            </form>
        </div>
        
        <script>
            function switchToRegister() {
                const loginForm = document.getElementById('loginForm');
                const registerForm = document.getElementById('registerForm');
                loginForm.classList.add('slide-up');
                registerForm.classList.add('slide-down');
            }
            
            function switchToLogin() {
                const loginForm = document.getElementById('loginForm');
                const registerForm = document.getElementById('registerForm');
                loginForm.classList.remove('slide-up');
                registerForm.classList.remove('slide-down');
            }
            
            document.getElementById('loginForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;
                const errorDiv = document.getElementById('loginError');
                errorDiv.textContent = '';
                
                try {
                    const response = await fetch('/login', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({email, password}),
                        redirect: 'follow'
                    });
                    if (response.ok) {
                        document.getElementById('fadeOverlay').classList.add('active');
                        setTimeout(() => { window.location.href = '/welcome'; }, 800);
                    } else {
                        errorDiv.textContent = 'Invalid email or password';
                    }
                } catch (error) {
                    errorDiv.textContent = 'Login failed: ' + error;
                }
            });
            
            document.getElementById('registerForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const name = document.getElementById('regName').value;
                const email = document.getElementById('regEmail').value;
                const password = document.getElementById('regPassword').value;
                const errorDiv = document.getElementById('registerError');
                errorDiv.textContent = '';
                
                try {
                    const response = await fetch('/register', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({name, email, password})
                    });
                    if (response.ok) {
                        alert('Registration successful! Logging in...');
                        document.getElementById('regEmail').value = email;
                        document.getElementById('regPassword').value = '';
                        switchToLogin();
                        setTimeout(() => {
                            document.getElementById('password').value = password;
                            document.getElementById('loginForm').submit();
                        }, 600);
                    } else {
                        const error = await response.json();
                        errorDiv.textContent = 'Error: ' + error.detail;
                    }
                } catch (error) {
                    errorDiv.textContent = 'Registration error: ' + error;
                }
            });
        </script>
    </body>
    </html>
    """


def get_register_page_html():
    """Generate HTML registration page - redirects to login with animation"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Japanese App</title>
    </head>
    <body>
        <script>
            window.location.href = '/login';
        </script>
    </body>
    </html>
    """
