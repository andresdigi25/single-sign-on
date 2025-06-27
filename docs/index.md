# Welcome to SSO API Documentation

Welcome to the SSO API documentation! This comprehensive guide will help you understand, integrate, and use the Single Sign-On authentication service effectively.

## 📚 Documentation Overview

This documentation is organized into several sections to help you find the information you need:

### 🚀 [User Guide](user-guide.md)
Complete reference for using the SSO API, including:
- Getting started guide
- User management operations
- Authentication workflows
- Password operations
- JWT token handling
- External identity provider integration
- API reference and troubleshooting

### 📖 [Tutorials](tutorials.md)
Step-by-step tutorials and code examples:
- Basic user registration and login
- Password recovery implementation
- Building login forms (HTML/JavaScript)
- External identity provider integration
- User import and bulk operations
- Advanced token management with Python/Node.js

### 🏗️ [Architecture Guide](architecture.md)
Technical deep-dive into the system architecture:
- System overview and design principles
- Component architecture
- Security model and JWT token management
- External IDP integration patterns
- Data flow diagrams
- Deployment architecture
- Performance considerations

### ❓ [FAQ](faq.md)
Frequently asked questions covering:
- General questions about the API
- Authentication and login issues
- JWT tokens and cookie handling
- Password management
- External identity providers
- Development and integration
- Troubleshooting common problems
- Security and compliance

## 🎯 Quick Start

### 1. Choose Your Path

**New to the SSO API?** Start with the [User Guide](user-guide.md#getting-started)

**Want hands-on examples?** Jump to the [Tutorials](tutorials.md#tutorial-1-basic-user-registration-and-login)

**Need technical details?** Check the [Architecture Guide](architecture.md#system-overview)

**Having issues?** Browse the [FAQ](faq.md) or [troubleshooting section](user-guide.md#troubleshooting)

### 2. Basic Usage Example

```bash
# 1. Health check
curl -X GET "https://dev-sso-api.integrichain.net/health"

# 2. Create user
curl -X POST "https://dev-sso-api.integrichain.net/users" \
  -H "Content-Type: application/json" \
  -d '{"username": "user@example.com", "password": "SecurePass123!", "email": "user@example.com"}'

# 3. Login
curl -X POST "https://dev-sso-api.integrichain.net/users/login" \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"username": "user@example.com", "password": "SecurePass123!"}'

# 4. Get user info
curl -X GET "https://dev-sso-api.integrichain.net/users/me" \
  -b cookies.txt
```

## 🌟 Key Features

- **🔐 Secure Authentication**: JWT-based authentication with HTTP-only cookies
- **👥 User Management**: Complete CRUD operations for user accounts
- **🔑 Password Operations**: Secure password reset and change workflows
- **🏢 External Identity Providers**: SAML 2.0 and OAuth 2.0 integration
- **📱 Multi-Platform**: Support for web, mobile, and API integrations
- **🚀 High Performance**: Built with FastAPI for optimal performance
- **☁️ Cloud Native**: Designed for AWS deployment with auto-scaling
- **🛡️ Security First**: Industry-standard security practices

## 🌐 Environment URLs

| Environment | URL | Purpose |
|-------------|-----|---------|
| Development | `https://dev-sso-api.integrichain.net` | Development and testing |
| Test | `https://test-sso-api.integrichain.net` | Integration testing |
| UAT | `https://uat-sso-api.integrichain.net` | User acceptance testing |
| Production | `https://prod-sso-api.integrichain.net` | Production use |

## 📋 API Documentation

Interactive API documentation is available for each environment:
- **OpenAPI UI**: `{environment-url}/docs`
- **ReDoc**: `{environment-url}/redoc`

## 🔧 Integration Examples

### JavaScript/Browser
```javascript
// Login
const response = await fetch('/users/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  credentials: 'include',
  body: JSON.stringify({ username: 'user@example.com', password: 'password' })
});

// Get user info
const userInfo = await fetch('/users/me', { credentials: 'include' });
```

### Python
```python
import requests

session = requests.Session()

# Login
response = session.post('https://dev-sso-api.integrichain.net/users/login',
                       json={'username': 'user@example.com', 'password': 'password'})

# Get user info
user_info = session.get('https://dev-sso-api.integrichain.net/users/me')
```

### cURL
```bash
# Login and save cookies
curl -X POST "https://dev-sso-api.integrichain.net/users/login" \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"username": "user@example.com", "password": "password"}'

# Use saved cookies for authenticated requests
curl -X GET "https://dev-sso-api.integrichain.net/users/me" -b cookies.txt
```

## 🧪 Testing

### Postman Collections
Pre-built Postman collections are available in the `app/test/` directory:
- **E2E Testing**: `app/test/e2e/single-sign-on-service.postman_collection.json`
- **Performance Testing**: `app/test/performance/sso-api.jmx`
- **User Verification**: `app/test/verify-user/sso-verify-user.postman_collection.json`

### Environment Files
Environment-specific configurations:
- Development: `app/test/e2e/single-sign-on-service-dev.postman_environment.json`
- Test: `app/test/e2e/single-sign-on-service-test.postman_environment.json`
- UAT: `app/test/e2e/single-sign-on-service-uat.postman_environment.json`
- Production: `app/test/e2e/single-sign-on-service-prod.postman_environment.json`

## 🔍 Common Use Cases

1. **Web Application Login**: [Tutorial 3](tutorials.md#tutorial-3-building-a-login-form)
2. **Password Recovery**: [Tutorial 2](tutorials.md#tutorial-2-password-recovery-workflow)
3. **Enterprise SSO**: [Tutorial 4](tutorials.md#tutorial-4-integrating-with-external-identity-providers)
4. **Bulk User Import**: [Tutorial 5](tutorials.md#tutorial-5-user-import-and-bulk-operations)
5. **API Integration**: [Tutorial 6](tutorials.md#tutorial-6-token-management-and-session-handling)

## ⚠️ Important Notes

- **HTTPS Required**: All API communication must use HTTPS
- **Cookie-Based Auth**: JWT tokens are stored in HTTP-only cookies for security
- **Rate Limiting**: API calls are rate-limited to prevent abuse
- **Token Expiration**: JWT tokens expire after 1 hour by default
- **CORS Configuration**: Ensure your domain is in the allowed origins list

## 🆘 Support

### Getting Help
1. **Documentation**: Check this documentation first
2. **FAQ**: Common questions are answered in the [FAQ](faq.md)
3. **Issues**: Create an issue in the project repository
4. **Security**: Use designated security channels for security issues

### Useful Links
- 📊 [API Status Page]: Check service status
- 🐛 [Bug Reports]: Report issues
- 💬 [Discussions]: Community discussions
- 📧 [Support Email]: Direct support contact

## 📈 What's Next?

Ready to integrate? Here's your next steps:

1. **Read the basics**: Start with the [User Guide](user-guide.md)
2. **Try examples**: Work through the [Tutorials](tutorials.md)
3. **Understand the system**: Review the [Architecture Guide](architecture.md)
4. **Test integration**: Use the Postman collections
5. **Get help**: Check the [FAQ](faq.md) if you run into issues

---

**Happy coding!** 🚀

*This documentation is maintained by the Integrichain development team. Last updated: January 2024*