#!/usr/bin/env python3
"""
Documentation validation script for MkDocs build.
Checks for common issues without being overly strict.
"""

import os
import sys
import re
from pathlib import Path

def check_docs_structure():
    """Check that required documentation files exist."""
    docs_dir = Path("docs")
    required_files = ["index.md", "user-guide.md", "tutorials.md", "architecture.md", "faq.md"]
    
    missing_files = []
    for file in required_files:
        if not (docs_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required documentation files present")
    return True

def check_mkdocs_config():
    """Check that mkdocs.yml exists and has basic configuration."""
    if not Path("mkdocs.yml").exists():
        print("❌ mkdocs.yml not found")
        return False
    
    with open("mkdocs.yml", "r") as f:
        content = f.read()
        
    if "site_name:" not in content:
        print("❌ mkdocs.yml missing site_name")
        return False
        
    if "theme:" not in content:
        print("❌ mkdocs.yml missing theme configuration")
        return False
    
    print("✅ mkdocs.yml configuration looks good")
    return True

def check_internal_links():
    """Check for obvious broken internal links."""
    docs_dir = Path("docs")
    broken_links = []
    
    for md_file in docs_dir.glob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Find markdown links [text](file.md)
        links = re.findall(r'\[.*?\]\(([^)]+\.md[^)]*)\)', content)
        
        for link in links:
            # Remove anchor part if present
            file_part = link.split('#')[0]
            if file_part and not file_part.startswith('http'):
                # Check if file exists
                link_path = docs_dir / file_part
                if not link_path.exists():
                    broken_links.append(f"{md_file.name} -> {link}")
    
    if broken_links:
        print(f"⚠️ Potential broken internal links found:")
        for link in broken_links:
            print(f"  - {link}")
        # Don't fail the build for link issues, just warn
        return True
    
    print("✅ No obvious broken internal links found")
    return True

def main():
    """Run all validation checks."""
    print("🔍 Validating documentation structure...")
    
    checks = [
        check_docs_structure,
        check_mkdocs_config,
        check_internal_links
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
    
    if all_passed:
        print("\n✅ Documentation validation passed!")
        return 0
    else:
        print("\n❌ Documentation validation failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())