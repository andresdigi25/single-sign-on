# 📚 SSO API Documentation Website

This directory contains the source files and configuration for generating a beautiful documentation website using MkDocs Material.

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip

### Build and Serve Locally

1. **Install dependencies**:
   ```bash
   pip install -r requirements-docs.txt
   ```

2. **Serve locally** (with live reload):
   ```bash
   ./serve-docs.sh
   ```
   Or manually:
   ```bash
   mkdocs serve
   ```

3. **Build for production**:
   ```bash
   ./build-docs.sh
   ```
   Or manually:
   ```bash
   mkdocs build
   ```

## 📁 Project Structure

```
docs/
├── index.md              # Home page (auto-generated from README.md)
├── user-guide.md         # Complete API reference and usage guide
├── tutorials.md          # Step-by-step tutorials with examples
├── architecture.md       # Technical architecture documentation
├── faq.md               # Frequently asked questions
├── stylesheets/
│   └── extra.css        # Custom styling
└── javascripts/
    └── mathjax.js       # MathJax configuration

mkdocs.yml               # MkDocs configuration
requirements-docs.txt    # Documentation dependencies
build-docs.sh           # Build script
serve-docs.sh           # Development server script
```

## 🎨 Features

### Material Design Theme
- Modern, responsive design
- Dark/light mode toggle
- Mobile-friendly navigation
- Search functionality

### Enhanced Markdown Support
- Code syntax highlighting
- Mermaid diagrams
- Admonitions (notes, warnings, tips)
- Tables with sorting
- Tabbed content
- Task lists

### Custom Styling
- Brand colors and styling
- Environment badges (dev, test, UAT, prod)
- API endpoint formatting
- Status indicators
- Quick reference cards

### Navigation Features
- Tabbed navigation
- Section expansion
- Breadcrumbs
- Table of contents
- Search with suggestions

## 🔧 Configuration

### MkDocs Configuration (`mkdocs.yml`)

Key configuration sections:

```yaml
# Site information
site_name: SSO API Documentation
site_description: Comprehensive documentation for the Single Sign-On API

# Theme configuration
theme:
  name: material
  palette:
    - scheme: default
      primary: blue
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: blue  
      toggle:
        icon: material/brightness-4
        name: Switch to light mode

# Navigation structure
nav:
  - Home: index.md
  - Getting Started: ...
  - User Guide: user-guide.md
  - Tutorials: tutorials.md
  - Architecture: architecture.md
  - Help: faq.md
```

### Custom Styling

Add custom CSS in `docs/stylesheets/extra.css`:

```css
/* Brand colors */
:root {
  --sso-primary: #1976d2;
  --sso-secondary: #0d47a1;
}

/* Environment badges */
.env-badge.dev { background-color: #17a2b8; }
.env-badge.prod { background-color: #dc3545; }
```

## 📝 Writing Documentation

### Markdown Extensions

The following extensions are enabled:

- **Admonitions**: For notes, warnings, tips
  ```markdown
  !!! note "Important"
      This is an important note.
  ```

- **Code blocks**: With syntax highlighting
  ```markdown
  ```python
  def hello_world():
      print("Hello, World!")
  ```
  ```

- **Mermaid diagrams**: For flowcharts and diagrams
  ```markdown
  ```mermaid
  graph TD
      A[Start] --> B[Process]
      B --> C[End]
  ```
  ```

- **Tabbed content**: For organizing related information
  ```markdown
  === "Python"
      ```python
      print("Hello from Python")
      ```
  
  === "JavaScript"
      ```javascript
      console.log("Hello from JavaScript");
      ```
  ```

### Best Practices

1. **Use descriptive headings** for navigation
2. **Include code examples** for all API endpoints
3. **Add cross-references** between related sections
4. **Use admonitions** for important notes and warnings
5. **Keep sections focused** and well-organized

## 🚀 Deployment

### Local Development
```bash
# Start development server
./serve-docs.sh

# Or with custom host/port
mkdocs serve --dev-addr 0.0.0.0:8080
```

### Production Build
```bash
# Build static site
./build-docs.sh

# Output will be in site/ directory
ls site/
```

### Deploy Options

1. **Static hosting** (GitHub Pages, Netlify, Vercel):
   - Upload `site/` directory contents

2. **Web server** (Apache, Nginx):
   - Copy `site/` contents to web root

3. **CI/CD Pipeline**:
   ```yaml
   # Example GitHub Actions workflow
   - name: Build docs
     run: |
       pip install -r requirements-docs.txt
       mkdocs build
   
   - name: Deploy
     uses: peaceiris/actions-gh-pages@v3
     with:
       github_token: ${{ secrets.GITHUB_TOKEN }}
       publish_dir: ./site
   ```

## 🔍 Search Configuration

Search is enabled by default with:
- Full-text search across all pages
- Search suggestions
- Highlighting of search terms
- Keyboard shortcuts (/ to focus search)

## 📊 Analytics (Optional)

To add Google Analytics:

```yaml
# In mkdocs.yml
extra:
  analytics:
    provider: google
    property: G-XXXXXXXXXX
```

## 🛠️ Troubleshooting

### Common Issues

1. **Dependencies not installed**:
   ```bash
   pip install -r requirements-docs.txt
   ```

2. **Port already in use**:
   ```bash
   ./serve-docs.sh 8001  # Use different port
   ```

3. **Build fails**:
   ```bash
   mkdocs build --verbose  # See detailed errors
   ```

4. **Mermaid diagrams not rendering**:
   - Check mermaid2 plugin is installed
   - Verify diagram syntax

### Performance Optimization

- Enable minification plugin (already configured)
- Optimize images before adding to docs
- Use CDN for external resources

## 📚 Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Mermaid Documentation](https://mermaid-js.github.io/mermaid/)

---

**Happy documenting!** 📖✨