# SSO API User Guide

## Table of Contents
- [Getting Started](#getting-started)
- [User Management](#user-management)
- [Authentication & Login](#authentication-login)
- [Password Operations](#password-operations)
- [JWT Token Management](#jwt-token-management)
- [External Identity Providers (IDP)](#external-identity-providers-idp)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)

## Getting Started

The SSO API is a comprehensive authentication service built with FastAPI that provides user management, authentication, and integration with external identity providers.

### Base URLs
- **Development**: `https://dev-sso-api.integrichain.net`
- **Test**: `https://test-sso-api.integrichain.net`
- **UAT**: `https://uat-sso-api.integrichain.net`
- **Production**: `https://prod-sso-api.integrichain.net`

### Quick Start
1. Check API health: `GET /health`
2. Create a user: `POST /users`
3. Login: `POST /users/login`
4. Access protected resources using the JWT token from cookies

## User Management

### Creating Users

Create new users in the system with required information.

**Endpoint**: `POST /users`

**Request Body**:
```json
{
  "username": "john.doe@example.com",
  "email": "john.doe@example.com",
  "password": "SecurePassword123!",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890"
}
```

**Response**:
```json
{
  "message": "User created successfully",
  "user_id": "12345678-1234-1234-1234-123456789012"
}
```

### Retrieving User Information

Get current user information using the authentication token.

**Endpoint**: `GET /users/me`

**Headers**:
```
Cookie: x-icyte-token-auth=your-jwt-token-here
```

**Response**:
```json
{
  "user_id": "12345678-1234-1234-1234-123456789012",
  "username": "john.doe@example.com",
  "email": "john.doe@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890",
  "status": "CONFIRMED"
}
```

### Updating User Information

Update user profile information.

**Endpoint**: `PUT /users/me`

**Request Body**:
```json
{
  "first_name": "John",
  "last_name": "Smith",
  "phone_number": "+0987654321"
}
```

## Authentication Login

### User Login

Authenticate users and receive JWT tokens via secure HTTP-only cookies.

**Endpoint**: `POST /users/login`

**Request Body**:
```json
{
  "username": "john.doe@example.com",
  "password": "SecurePassword123!"
}
```

**Response**:
```json
{
  "message": "Login successful",
  "user": {
    "user_id": "12345678-1234-1234-1234-123456789012",
    "username": "john.doe@example.com",
    "email": "john.doe@example.com"
  }
}
```

**Important**: The JWT token is automatically set in an HTTP-only cookie named `x-icyte-token-auth`.

### User Logout

Invalidate the current session and clear authentication cookies.

**Endpoint**: `POST /users/logout`

**Headers**:
```
Cookie: x-icyte-token-auth=your-jwt-token-here
```

**Response**:
```json
{
  "message": "Logout successful"
}
```

## Password Operations

### Password Reset Request

Initiate a password reset process by sending a reset code to the user's email.

**Endpoint**: `POST /users/forgot-password`

**Request Body**:
```json
{
  "username": "john.doe@example.com"
}
```

**Response**:
```json
{
  "message": "Password reset code sent to email"
}
```

### Confirm Password Reset

Complete the password reset using the code received via email.

**Endpoint**: `POST /users/confirm-forgot-password`

**Request Body**:
```json
{
  "username": "john.doe@example.com",
  "confirmation_code": "123456",
  "new_password": "NewSecurePassword123!"
}
```

**Response**:
```json
{
  "message": "Password reset successful"
}
```

### Change Password

Change password for authenticated users.

**Endpoint**: `POST /users/change-password`

**Headers**:
```
Cookie: x-icyte-token-auth=your-jwt-token-here
```

**Request Body**:
```json
{
  "old_password": "OldPassword123!",
  "new_password": "NewSecurePassword123!"
}
```

**Response**:
```json
{
  "message": "Password changed successfully"
}
```

## JWT Token Management

### Understanding JWT Tokens

The SSO API uses JWT (JSON Web Tokens) for authentication. Tokens are:
- Stored in HTTP-only cookies for security
- Named `x-icyte-token-auth`
- Automatically included in requests by browsers
- Contain user information and permissions

### Token Usage

#### Automatic Cookie Handling
When using a web browser, tokens are handled automatically:
```javascript
// Login request - token is set automatically
fetch('/users/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'user@example.com', password: 'password' })
});

// Subsequent requests include the token automatically
fetch('/users/me'); // Token sent via cookie
```

#### Manual Token Handling (for API clients)
For non-browser clients, extract and manage tokens manually:
```python
import requests

# Login and capture cookies
response = requests.post('https://dev-sso-api.integrichain.net/users/login', 
                        json={'username': 'user@example.com', 'password': 'password'})

# Extract token from cookies
token = response.cookies.get('x-icyte-token-auth')

# Use token in subsequent requests
headers = {'Cookie': f'x-icyte-token-auth={token}'}
user_info = requests.get('https://dev-sso-api.integrichain.net/users/me', headers=headers)
```

### Token Validation

Check if a token is valid:

**Endpoint**: `GET /users/me`

- **200 OK**: Token is valid
- **401 Unauthorized**: Token is invalid or expired

## External Identity Providers (IDP)

### SAML Integration

The API supports SAML-based external identity providers for enterprise authentication.

#### Initiate SAML Authentication

**Endpoint**: `GET /saml/login`

**Parameters**:
- `RelayState` (optional): URL to redirect after successful authentication

**Response**: Redirects to the configured SAML Identity Provider

#### SAML Callback

**Endpoint**: `POST /saml/acs`

This endpoint receives SAML assertions from the identity provider and processes authentication.

### OAuth/OIDC Integration

Support for OAuth 2.0 and OpenID Connect providers.

#### OAuth Login

**Endpoint**: `GET /oauth/{provider}/login`

**Parameters**:
- `provider`: OAuth provider name (e.g., `google`, `microsoft`)
- `redirect_uri`: URL to redirect after authentication

### Configuration

External providers are configured via environment variables or AWS Secrets Manager:

```json
{
  "saml_settings": {
    "sp_entity_id": "your-service-provider-id",
    "idp_sso_url": "https://idp.example.com/sso",
    "idp_x509_cert": "-----BEGIN CERTIFICATE-----..."
  },
  "oauth_providers": {
    "google": {
      "client_id": "your-google-client-id",
      "client_secret": "your-google-client-secret"
    }
  }
}
```

## API Reference

### Authentication Headers

All protected endpoints require authentication via the JWT token cookie:

```
Cookie: x-icyte-token-auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Common Response Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Authentication required or invalid
- **403 Forbidden**: Access denied
- **404 Not Found**: Resource not found
- **409 Conflict**: Resource already exists
- **500 Internal Server Error**: Server error

### Error Response Format

```json
{
  "message": "Detailed error description"
}
```

### Rate Limiting

The API implements rate limiting to prevent abuse:
- **Login attempts**: 5 attempts per minute per IP
- **Password reset**: 3 requests per hour per user
- **General API calls**: 1000 requests per hour per authenticated user

## Troubleshooting

### Common Issues

#### Authentication Errors

**Problem**: Getting 401 Unauthorized errors
**Solutions**:
1. Ensure the JWT token cookie is present and valid
2. Check if the token has expired (login again)
3. Verify the cookie domain matches the API domain

#### CORS Issues

**Problem**: Browser blocking requests due to CORS
**Solutions**:
1. Ensure your domain is in the allowed origins list
2. Include credentials in your requests: `credentials: 'include'`
3. Check that cookies are being sent with cross-origin requests

#### Password Reset Not Working

**Problem**: Not receiving password reset emails
**Solutions**:
1. Check spam/junk folders
2. Verify the email address is correct
3. Ensure the user account exists and is confirmed

#### External IDP Integration Issues

**Problem**: SAML/OAuth authentication failing
**Solutions**:
1. Verify IDP configuration is correct
2. Check certificate validity for SAML
3. Ensure callback URLs are properly configured
4. Review IDP logs for specific error messages

### Debug Mode

Enable debug logging by setting environment variables:
```bash
export LOG_LEVEL=DEBUG
export config_secret_manager=dev/sso-api
python main.py
```

### Health Check

Monitor API health:
**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "2.7.2"
}
```

### Support

For additional support:
1. Check the OpenAPI documentation at `/docs`
2. Review server logs for detailed error information
3. Contact the development team with specific error messages and request details