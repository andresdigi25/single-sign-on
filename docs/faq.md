# SSO API - Frequently Asked Questions

## Table of Contents
- [General Questions](#general-questions)
- [Authentication & Login](#authentication-login)
- [JWT Tokens & Cookies](#jwt-tokens-cookies)
- [Password Management](#password-management)
- [External Identity Providers](#external-identity-providers)
- [Development & Integration](#development-integration)
- [Troubleshooting](#troubleshooting)
- [Security & Compliance](#security-compliance)

## General Questions

### Q: What is the SSO API?
**A:** The SSO API is a centralized authentication service built with FastAPI that provides user management, authentication, and integration with external identity providers for Integrichain applications.

### Q: What authentication methods are supported?
**A:** The API supports:
- Username/password authentication
- SAML 2.0 integration
- OAuth 2.0 / OpenID Connect
- Multi-factor authentication (via AWS Cognito)

### Q: Which environments are available?
**A:** Four environments are available:
- **Development**: `https://dev-sso-api.integrichain.net`
- **Test**: `https://test-sso-api.integrichain.net`
- **UAT**: `https://uat-sso-api.integrichain.net`
- **Production**: `https://prod-sso-api.integrichain.net`

### Q: Is the API RESTful?
**A:** Yes, the API follows REST principles with standard HTTP methods (GET, POST, PUT, DELETE) and returns JSON responses.

### Q: What's the current API version?
**A:** The current version is 2.7.2. Version information is available at the `/health` endpoint.

## Authentication Login

### Q: How do I authenticate with the API?
**A:** Authentication is done via JWT tokens stored in HTTP-only cookies. After successful login, the token is automatically included in subsequent requests.

### Q: What's the login endpoint?
**A:** Use `POST /users/login` with username and password in the request body.

### Q: How long do login sessions last?
**A:** JWT tokens expire after 1 hour by default. Users need to login again after expiration.

### Q: Can I extend the session duration?
**A:** Session duration is configurable but should be kept short for security. Contact your administrator to modify the default duration.

### Q: What happens if I try to access a protected endpoint without authentication?
**A:** You'll receive a `401 Unauthorized` response with an error message.

### Q: How do I logout?
**A:** Use `POST /users/logout` to invalidate your session and clear the authentication cookie.

### Q: Can I login from multiple devices simultaneously?
**A:** Yes, each device maintains its own session. There's no limit on concurrent sessions per user.

## JWT Tokens Cookies

### Q: Why are JWT tokens stored in cookies instead of localStorage?
**A:** HTTP-only cookies provide better security by preventing XSS attacks. JavaScript cannot access these cookies, making token theft more difficult.

### Q: What's the cookie name for the JWT token?
**A:** The cookie is named `x-icyte-token-auth`.

### Q: How do I handle tokens in my application?
**A:** For web applications, browsers handle cookies automatically. For API clients, extract the cookie from login responses and include it in subsequent requests.

### Q: Can I decode the JWT token to get user information?
**A:** While JWT tokens can be decoded, it's recommended to use the `/users/me` endpoint to get current user information securely.

### Q: What information is stored in the JWT token?
**A:** Tokens contain user ID, username, email, issued time, expiration time, issuer, and audience claims.

### Q: How do I refresh an expired token?
**A:** There's no refresh token mechanism. Users must login again when tokens expire.

### Q: Are tokens validated on every request?
**A:** Yes, protected endpoints validate tokens on each request to ensure they're not expired or tampered with.

## Password Management

### Q: What are the password requirements?
**A:** Password requirements are enforced by AWS Cognito and typically include:
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

### Q: How do I reset a forgotten password?
**A:** Use the password reset flow:
1. `POST /users/forgot-password` with username
2. Check email for confirmation code
3. `POST /users/confirm-forgot-password` with username, code, and new password

### Q: How long is the password reset code valid?
**A:** Reset codes typically expire after 15 minutes for security.

### Q: Can I change my password while logged in?
**A:** Yes, use `POST /users/change-password` with your current and new passwords.

### Q: What if I don't receive the password reset email?
**A:** Check your spam folder, verify the email address is correct, and ensure the user account exists. Contact support if issues persist.

### Q: Are passwords stored securely?
**A:** Yes, passwords are hashed using industry-standard bcrypt with salt before storage in AWS Cognito.

### Q: Can I reuse old passwords?
**A:** Password reuse policies are configured in AWS Cognito. Check with your administrator for specific rules.

## External Identity Providers

### Q: What external identity providers are supported?
**A:** The API supports:
- SAML 2.0 providers (e.g., Active Directory, Okta, Ping)
- OAuth 2.0 providers (e.g., Google, Microsoft, GitHub)
- OpenID Connect providers

### Q: How do I login with an external provider?
**A:** Access the provider-specific login URL (e.g., `/saml/login` for SAML or `/oauth/google/login` for Google).

### Q: Can I link multiple identity providers to one account?
**A:** This depends on the configuration. Contact your administrator for details about account linking policies.

### Q: What happens if my external provider is unavailable?
**A:** Users with external provider accounts won't be able to login until the provider is restored. Local accounts remain unaffected.

### Q: How do I configure SAML integration?
**A:** SAML configuration requires:
- Service Provider (SP) metadata
- Identity Provider (IdP) metadata
- Certificate exchange
- Attribute mapping configuration

Contact your administrator for SAML setup.

### Q: Can I use multiple SAML providers?
**A:** Yes, multiple SAML providers can be configured with different entity IDs and endpoints.

## Development Integration

### Q: Where can I find the API documentation?
**A:** Interactive documentation is available at:
- OpenAPI UI: `{base_url}/docs`
- ReDoc: `{base_url}/redoc`

### Q: Are there SDKs or client libraries available?
**A:** Currently, there are no official SDKs. Use standard HTTP libraries in your preferred language. Examples are provided in the tutorials.

### Q: How do I handle CORS in my web application?
**A:** The API is configured with CORS support. Ensure your domain is in the allowed origins list and include `credentials: 'include'` in your requests.

### Q: Can I use the API from a mobile application?
**A:** Yes, but you'll need to handle cookie storage manually. Consider using a web view or implement custom token storage.

### Q: How do I test the API?
**A:** Use the provided Postman collections in the `app/test/` directory or any HTTP client like curl or Insomnia.

### Q: Are there rate limits?
**A:** Yes, rate limits are enforced:
- Login attempts: 5 per minute per IP
- Password reset: 3 per hour per user
- General API calls: 1000 per hour per authenticated user

### Q: How do I handle rate limit responses?
**A:** Rate limit responses return `429 Too Many Requests`. Implement exponential backoff in your retry logic.

## Troubleshooting

### Q: I'm getting CORS errors in my browser
**A:** Ensure:
- Your domain is in the allowed origins
- Include `credentials: 'include'` in requests
- Use HTTPS in production

### Q: My login requests are failing with 400 Bad Request
**A:** Check:
- Request body format (JSON)
- Required fields (username, password)
- Content-Type header (`application/json`)

### Q: I'm getting 401 Unauthorized on protected endpoints
**A:** Verify:
- You're logged in
- Token hasn't expired
- Cookies are being sent with requests
- Cookie domain matches API domain

### Q: The API returns 500 Internal Server Error
**A:** This indicates a server-side issue. Check:
- API status page
- Contact support with request details
- Retry the request after a short delay

### Q: Password reset emails aren't being delivered
**A:** Check:
- Spam/junk folder
- Email address is correct
- User account exists
- Email service status

### Q: SAML authentication isn't working
**A:** Verify:
- SAML configuration is correct
- Certificates are valid and not expired
- Clock synchronization between SP and IdP
- Network connectivity to IdP

### Q: How do I debug API integration issues?
**A:** Enable debug logging and check:
- Request/response headers
- HTTP status codes
- Response bodies
- Network connectivity
- SSL certificate validity

## Security Compliance

### Q: Is the API secure?
**A:** Yes, the API implements multiple security measures:
- HTTPS encryption
- JWT token authentication
- HTTP-only cookies
- Input validation
- Rate limiting
- CORS configuration

### Q: How is user data protected?
**A:** User data is protected through:
- Encryption at rest (AWS)
- Encryption in transit (HTTPS)
- Access controls
- Audit logging
- Regular security updates

### Q: Is the API compliant with regulations?
**A:** The API is built with compliance in mind, but specific compliance (GDPR, HIPAA, SOC 2) depends on configuration and usage. Consult with your compliance team.

### Q: How are passwords stored?
**A:** Passwords are never stored in plain text. They're hashed using bcrypt with salt and stored in AWS Cognito.

### Q: What audit logs are available?
**A:** The API logs:
- Authentication attempts
- Password changes
- User management actions
- API access patterns
- Security events

### Q: How do I report security vulnerabilities?
**A:** Report security issues through the designated security contact or create a confidential issue in the repository.

### Q: Are there security headers implemented?
**A:** Yes, the API implements security headers including:
- Strict-Transport-Security
- X-Content-Type-Options
- X-Frame-Options
- X-XSS-Protection

### Q: How often are security updates applied?
**A:** Security updates are applied as soon as possible after they're available. Critical security patches are prioritized.

### Q: Can I use the API over HTTP?
**A:** No, HTTPS is required for all API communication to ensure data security in transit.

---

## Need More Help?

If your question isn't answered here:

1. Check the [User Guide](user-guide.md) for detailed documentation
2. Review the [Tutorials](tutorials.md) for implementation examples
3. Examine the [Architecture Guide](architecture.md) for technical details
4. Contact the development team with specific issues
5. Create an issue in the project repository

For urgent security issues, use the designated security contact rather than public channels.