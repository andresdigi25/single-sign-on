# 🚀 GitHub Pages Deployment Guide

This guide shows you how to deploy your MkDocs documentation to GitHub Pages using GitHub Actions.

## 📋 Prerequisites

- GitHub repository with your SSO API code
- Admin access to the repository
- Documentation files in the `docs/` directory
- MkDocs configuration (`mkdocs.yml`)

## 🔧 Setup Steps

### 1. Update Repository Configuration

First, update the `mkdocs.yml` file with your GitHub repository information:

```yaml
# In mkdocs.yml
site_url: https://yourusername.github.io/your-repo-name
repo_name: yourusername/your-repo-name
repo_url: https://github.com/yourusername/your-repo-name
```

**Replace:**
- `yourusername` with your GitHub username or organization
- `your-repo-name` with your repository name

### 2. Enable GitHub Pages

1. **Go to your GitHub repository**
2. **Click Settings** (in the repository menu)
3. **Scroll down to "Pages"** in the left sidebar
4. **Under "Source"** select **"GitHub Actions"**
5. **Click Save**

### 3. Push Your Changes

The GitHub Actions workflow is already configured in `.github/workflows/deploy-docs.yml`.

```bash
# Add all files
git add .

# Commit changes
git commit -m "Add MkDocs documentation with GitHub Pages deployment

- Add comprehensive documentation (User Guide, Tutorials, Architecture, FAQ)
- Configure MkDocs Material theme
- Set up GitHub Actions workflow for automatic deployment
- Add deployment scripts and configuration

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to main branch
git push origin main
```

### 4. Monitor Deployment

1. **Go to the "Actions" tab** in your GitHub repository
2. **Look for the "Deploy Documentation to GitHub Pages" workflow**
3. **Click on the latest run** to see deployment progress
4. **Wait for the green checkmark** ✅

### 5. Access Your Documentation

Once deployed, your documentation will be available at:
```
https://yourusername.github.io/your-repo-name/
```

## 🔄 Automatic Updates

The workflow is configured to automatically deploy when you:

- **Push changes** to the `main` branch that affect:
  - Files in the `docs/` directory
  - `mkdocs.yml` configuration
  - `requirements-docs.txt` dependencies
  - The workflow file itself

- **Manually trigger** the workflow from the Actions tab

## 📁 Workflow Details

The deployment workflow (`.github/workflows/deploy-docs.yml`) performs these steps:

### Build Job
1. **Checkout code** from the repository
2. **Setup Python 3.11** with pip cache
3. **Install dependencies** from `requirements-docs.txt`
4. **Configure GitHub Pages** environment
5. **Build documentation** with `mkdocs build`
6. **Upload build artifacts** for deployment

### Deploy Job
1. **Deploy to GitHub Pages** using the built artifacts
2. **Set environment URL** to the deployed site

## ⚙️ Configuration Options

### Custom Domain (Optional)

To use a custom domain:

1. **Add a `CNAME` file** to the `docs/` directory:
   ```
   docs.yourdomain.com
   ```

2. **Update `mkdocs.yml`**:
   ```yaml
   site_url: https://docs.yourdomain.com
   ```

3. **Configure DNS** to point to `yourusername.github.io`

### Branch Protection (Recommended)

For production repositories:

1. **Go to Settings > Branches**
2. **Add rule for `main` branch**
3. **Enable "Require status checks"**
4. **Select "build" from the workflow**

## 🐛 Troubleshooting

### Common Issues

#### ❌ Workflow Fails on Build
**Problem**: Dependencies not installing or build errors

**Solutions**:
```bash
# Test locally first
pip install -r requirements-docs.txt
mkdocs build --clean --strict

# Check workflow logs in GitHub Actions tab
```

#### ❌ Pages Not Updating
**Problem**: Site shows old content

**Solutions**:
1. **Hard refresh** browser (Ctrl+F5 or Cmd+Shift+R)
2. **Check workflow** completed successfully
3. **Verify GitHub Pages source** is set to "GitHub Actions"

#### ❌ 404 Errors
**Problem**: Site shows 404 or doesn't load

**Solutions**:
1. **Check `site_url`** in `mkdocs.yml` matches your GitHub Pages URL
2. **Verify repository name** is correct
3. **Ensure Pages is enabled** in repository settings

#### ❌ Permission Denied
**Problem**: Workflow can't deploy to Pages

**Solutions**:
1. **Check repository settings** > Actions > General
2. **Ensure "Read and write permissions"** is enabled
3. **Verify Pages source** is set to "GitHub Actions"

### Debugging Steps

1. **Check Actions tab** for detailed error logs
2. **Test build locally**:
   ```bash
   mkdocs build --clean --strict --verbose
   ```
3. **Validate configuration**:
   ```bash
   mkdocs config
   ```

## 🔒 Security Notes

### Permissions
The workflow uses minimal permissions:
- `contents: read` - Read repository files
- `pages: write` - Deploy to GitHub Pages
- `id-token: write` - Authentication for deployment

### Branch Protection
The workflow only runs on the `main` branch and only affects documentation files.

### No Secrets Required
The deployment uses GitHub's built-in `GITHUB_TOKEN` - no additional secrets needed.

## 📊 Monitoring

### View Deployment Status
- **Actions tab**: See all workflow runs
- **Environments tab**: Track deployments
- **Settings > Pages**: Check configuration

### Analytics (Optional)
Add Google Analytics to track documentation usage:

```yaml
# In mkdocs.yml
extra:
  analytics:
    provider: google
    property: G-XXXXXXXXXX
```

## 🎯 Best Practices

### Documentation Updates
1. **Test locally** before pushing:
   ```bash
   ./serve-docs.sh
   ```

2. **Use descriptive commit messages** for documentation changes

3. **Review changes** in pull requests before merging

### Performance
1. **Optimize images** before adding to docs
2. **Use external links** for large assets
3. **Enable minification** (already configured)

### SEO
1. **Add descriptive titles** to all pages
2. **Use proper heading hierarchy** (H1 > H2 > H3)
3. **Include meta descriptions** in page frontmatter

## 🚀 Advanced Configuration

### Multiple Environments
Deploy to different environments:

```yaml
# Add to workflow for staging
- name: Deploy to staging
  if: github.ref == 'refs/heads/develop'
  # Deploy to staging environment
```

### Custom Build Scripts
Enhance the build process:

```yaml
# Add custom build steps
- name: Pre-build validation
  run: |
    # Custom validation scripts
    python scripts/validate-docs.py
```

## ✅ Verification Checklist

After setup, verify:

- [ ] Repository has GitHub Pages enabled
- [ ] Workflow file is in `.github/workflows/`
- [ ] `mkdocs.yml` has correct site URL
- [ ] Dependencies file exists
- [ ] First deployment completed successfully
- [ ] Documentation site loads correctly
- [ ] All navigation links work
- [ ] Search functionality works
- [ ] Mobile view displays properly
- [ ] Dark/light mode toggle functions

## 🎉 Success!

Your documentation is now automatically deployed to GitHub Pages! 🚀

Every time you update the documentation and push to the main branch, GitHub Actions will automatically rebuild and deploy your site.

**Next Steps:**
1. Share your documentation URL with your team
2. Add the documentation link to your repository README
3. Consider setting up a custom domain for professional use

---

**Documentation URL**: `https://yourusername.github.io/your-repo-name/`

Happy documenting! 📚✨