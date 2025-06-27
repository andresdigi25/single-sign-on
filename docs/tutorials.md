# SSO API Tutorials

## Table of Contents
- [Tutorial 1: Basic User Registration and Login](#tutorial-1-basic-user-registration-and-login)
- [Tutorial 2: Password Recovery Workflow](#tutorial-2-password-recovery-workflow)
- [Tutorial 3: Building a Login Form](#tutorial-3-building-a-login-form)
- [Tutorial 4: Integrating with External Identity Providers](#tutorial-4-integrating-with-external-identity-providers)
- [Tutorial 5: User Import and Bulk Operations](#tutorial-5-user-import-and-bulk-operations)
- [Tutorial 6: Token Management and Session Handling](#tutorial-6-token-management-and-session-handling)

## Tutorial 1: Basic User Registration and Login

This tutorial walks through the complete process of registering a new user and logging them in.

### Step 1: Check API Health

First, verify the API is running:

```bash
curl -X GET "https://dev-sso-api.integrichain.net/health"
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "2.7.2"
}
```

### Step 2: Create a New User

```bash
curl -X POST "https://dev-sso-api.integrichain.net/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice.smith@example.com",
    "email": "alice.smith@example.com",
    "password": "SecurePass123!",
    "first_name": "Alice",
    "last_name": "Smith",
    "phone_number": "+1234567890"
  }'
```

Expected response:
```json
{
  "message": "User created successfully",
  "user_id": "12345678-1234-1234-1234-123456789012"
}
```

### Step 3: Login the User

```bash
curl -X POST "https://dev-sso-api.integrichain.net/users/login" \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "username": "alice.smith@example.com",
    "password": "SecurePass123!"
  }'
```

Expected response:
```json
{
  "message": "Login successful",
  "user": {
    "user_id": "12345678-1234-1234-1234-123456789012",
    "username": "alice.smith@example.com",
    "email": "alice.smith@example.com"
  }
}
```

### Step 4: Access Protected Resource

```bash
curl -X GET "https://dev-sso-api.integrichain.net/users/me" \
  -b cookies.txt
```

Expected response:
```json
{
  "user_id": "12345678-1234-1234-1234-123456789012",
  "username": "alice.smith@example.com",
  "email": "alice.smith@example.com",
  "first_name": "Alice",
  "last_name": "Smith",
  "phone_number": "+1234567890",
  "status": "CONFIRMED"
}
```

## Tutorial 2: Password Recovery Workflow

Learn how to implement password recovery for users who forgot their passwords.

### Step 1: Request Password Reset

```bash
curl -X POST "https://dev-sso-api.integrichain.net/users/forgot-password" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice.smith@example.com"
  }'
```

Expected response:
```json
{
  "message": "Password reset code sent to email"
}
```

### Step 2: Check Email for Reset Code

The user will receive an email with a 6-digit confirmation code.

### Step 3: Confirm Password Reset

```bash
curl -X POST "https://dev-sso-api.integrichain.net/users/confirm-forgot-password" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice.smith@example.com",
    "confirmation_code": "123456",
    "new_password": "NewSecurePass123!"
  }'
```

Expected response:
```json
{
  "message": "Password reset successful"
}
```

### Step 4: Test New Password

```bash
curl -X POST "https://dev-sso-api.integrichain.net/users/login" \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "username": "alice.smith@example.com",
    "password": "NewSecurePass123!"
  }'
```

## Tutorial 3: Building a Login Form

Create a web-based login form that integrates with the SSO API.

### HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SSO Login</title>
    <style>
        .login-form {
            max-width: 400px;
            margin: 50px auto;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
        }
        input[type="email"], input[type="password"] {
            width: 100%;
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 3px;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 3px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .error {
            color: red;
            margin-top: 10px;
        }
        .success {
            color: green;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="login-form">
        <h2>Login</h2>
        <form id="loginForm">
            <div class="form-group">
                <label for="username">Email:</label>
                <input type="email" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
        <div id="message"></div>
        <div id="userInfo" style="display: none;">
            <h3>Welcome!</h3>
            <p id="userDetails"></p>
            <button onclick="logout()">Logout</button>
        </div>
    </div>

    <script>
        const API_BASE = 'https://dev-sso-api.integrichain.net';
        
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const messageDiv = document.getElementById('message');
            
            try {
                const response = await fetch(`${API_BASE}/users/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include', // Important for cookies
                    body: JSON.stringify({ username, password })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    messageDiv.innerHTML = '<div class="success">Login successful!</div>';
                    document.getElementById('loginForm').style.display = 'none';
                    await loadUserInfo();
                } else {
                    messageDiv.innerHTML = `<div class="error">${data.message}</div>`;
                }
            } catch (error) {
                messageDiv.innerHTML = '<div class="error">Network error occurred</div>';
            }
        });
        
        async function loadUserInfo() {
            try {
                const response = await fetch(`${API_BASE}/users/me`, {
                    credentials: 'include'
                });
                
                if (response.ok) {
                    const user = await response.json();
                    document.getElementById('userDetails').innerHTML = 
                        `Name: ${user.first_name} ${user.last_name}<br>Email: ${user.email}`;
                    document.getElementById('userInfo').style.display = 'block';
                }
            } catch (error) {
                console.error('Failed to load user info:', error);
            }
        }
        
        async function logout() {
            try {
                await fetch(`${API_BASE}/users/logout`, {
                    method: 'POST',
                    credentials: 'include'
                });
                
                document.getElementById('loginForm').style.display = 'block';
                document.getElementById('userInfo').style.display = 'none';
                document.getElementById('message').innerHTML = '';
                document.getElementById('loginForm').reset();
            } catch (error) {
                console.error('Logout failed:', error);
            }
        }
        
        // Check if user is already logged in
        window.addEventListener('load', async () => {
            try {
                const response = await fetch(`${API_BASE}/users/me`, {
                    credentials: 'include'
                });
                
                if (response.ok) {
                    document.getElementById('loginForm').style.display = 'none';
                    await loadUserInfo();
                }
            } catch (error) {
                // User not logged in, show login form
            }
        });
    </script>
</body>
</html>
```

## Tutorial 4: Integrating with External Identity Providers

Set up SAML and OAuth integrations for enterprise authentication.

### SAML Integration Example

#### Step 1: Configure SAML Settings

Add SAML configuration to your environment:

```json
{
  "saml_settings": {
    "sp_entity_id": "https://your-app.com/saml/metadata",
    "sp_acs_url": "https://dev-sso-api.integrichain.net/saml/acs",
    "idp_entity_id": "https://idp.company.com/metadata",
    "idp_sso_url": "https://idp.company.com/sso",
    "idp_x509_cert": "-----BEGIN CERTIFICATE-----\nMIIC...certificate...data...\n-----END CERTIFICATE-----"
  }
}
```

#### Step 2: Initiate SAML Login

```html
<a href="https://dev-sso-api.integrichain.net/saml/login?RelayState=https://your-app.com/dashboard">
    Login with Company SSO
</a>
```

#### Step 3: Handle SAML Response

The identity provider will POST to your ACS endpoint. The API handles this automatically.

### OAuth Integration Example

#### Step 1: Configure OAuth Provider

```json
{
  "oauth_providers": {
    "google": {
      "client_id": "your-google-client-id.googleusercontent.com",
      "client_secret": "your-google-client-secret",
      "redirect_uri": "https://dev-sso-api.integrichain.net/oauth/google/callback"
    }
  }
}
```

#### Step 2: Initiate OAuth Flow

```html
<a href="https://dev-sso-api.integrichain.net/oauth/google/login?redirect_uri=https://your-app.com/dashboard">
    Login with Google
</a>
```

## Tutorial 5: User Import and Bulk Operations

Learn how to import multiple users efficiently.

### Step 1: Prepare User Data

Create a CSV file with user data:

```csv
username,email,first_name,last_name,phone_number,temporary_password
john.doe@company.com,john.doe@company.com,John,Doe,+1234567890,TempPass123!
jane.smith@company.com,jane.smith@company.com,Jane,Smith,+0987654321,TempPass456!
```

### Step 2: Import Users

```bash
curl -X POST "https://dev-sso-api.integrichain.net/users/import" \
  -H "Content-Type: multipart/form-data" \
  -b cookies.txt \
  -F "file=@users.csv"
```

Expected response:
```json
{
  "message": "Import completed",
  "successful": 2,
  "failed": 0,
  "errors": []
}
```

### Step 3: Notify Users

Send emails to imported users with their temporary passwords and instructions to change them on first login.

## Tutorial 6: Token Management and Session Handling

Advanced token management for complex applications.

### Python Example with Session Management

```python
import requests
from datetime import datetime, timedelta

class SSOClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.token_expiry = None
    
    def login(self, username, password):
        """Login and store session cookies"""
        response = self.session.post(
            f"{self.base_url}/users/login",
            json={"username": username, "password": password}
        )
        
        if response.status_code == 200:
            # Calculate token expiry (tokens typically last 1 hour)
            self.token_expiry = datetime.now() + timedelta(hours=1)
            return response.json()
        else:
            raise Exception(f"Login failed: {response.json()['message']}")
    
    def is_token_valid(self):
        """Check if current token is still valid"""
        if not self.token_expiry:
            return False
        return datetime.now() < self.token_expiry
    
    def refresh_if_needed(self, username, password):
        """Refresh token if expired"""
        if not self.is_token_valid():
            self.login(username, password)
    
    def get_user_info(self):
        """Get current user information"""
        response = self.session.get(f"{self.base_url}/users/me")
        
        if response.status_code == 401:
            raise Exception("Token expired or invalid")
        
        return response.json()
    
    def logout(self):
        """Logout and clear session"""
        self.session.post(f"{self.base_url}/users/logout")
        self.session.cookies.clear()
        self.token_expiry = None

# Usage example
client = SSOClient("https://dev-sso-api.integrichain.net")

try:
    # Login
    login_result = client.login("user@example.com", "password")
    print(f"Login successful: {login_result['message']}")
    
    # Get user info
    user_info = client.get_user_info()
    print(f"Welcome, {user_info['first_name']}!")
    
    # Simulate token expiry check
    if client.is_token_valid():
        print("Token is still valid")
    else:
        print("Token expired, need to refresh")
    
    # Logout
    client.logout()
    print("Logged out successfully")
    
except Exception as e:
    print(f"Error: {e}")
```

### JavaScript/Node.js Example

```javascript
const axios = require('axios');

class SSOClient {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
        this.client = axios.create({
            baseURL: baseUrl,
            withCredentials: true, // Important for cookies
            timeout: 10000
        });
        
        // Add response interceptor for token refresh
        this.client.interceptors.response.use(
            response => response,
            async error => {
                if (error.response?.status === 401) {
                    // Token expired, could trigger re-login
                    console.log('Token expired, please login again');
                }
                return Promise.reject(error);
            }
        );
    }
    
    async login(username, password) {
        try {
            const response = await this.client.post('/users/login', {
                username,
                password
            });
            return response.data;
        } catch (error) {
            throw new Error(`Login failed: ${error.response?.data?.message || error.message}`);
        }
    }
    
    async getUserInfo() {
        try {
            const response = await this.client.get('/users/me');
            return response.data;
        } catch (error) {
            throw new Error(`Failed to get user info: ${error.response?.data?.message || error.message}`);
        }
    }
    
    async logout() {
        try {
            await this.client.post('/users/logout');
        } catch (error) {
            console.warn('Logout request failed:', error.message);
        }
    }
    
    async changePassword(oldPassword, newPassword) {
        try {
            const response = await this.client.post('/users/change-password', {
                old_password: oldPassword,
                new_password: newPassword
            });
            return response.data;
        } catch (error) {
            throw new Error(`Password change failed: ${error.response?.data?.message || error.message}`);
        }
    }
}

// Usage example
async function example() {
    const sso = new SSOClient('https://dev-sso-api.integrichain.net');
    
    try {
        // Login
        const loginResult = await sso.login('user@example.com', 'password');
        console.log('Login successful:', loginResult.message);
        
        // Get user info
        const userInfo = await sso.getUserInfo();
        console.log(`Welcome, ${userInfo.first_name}!`);
        
        // Change password
        await sso.changePassword('password', 'newPassword123!');
        console.log('Password changed successfully');
        
        // Logout
        await sso.logout();
        console.log('Logged out');
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

module.exports = SSOClient;
```

These tutorials provide comprehensive guidance for integrating with the SSO API across different scenarios and programming languages.