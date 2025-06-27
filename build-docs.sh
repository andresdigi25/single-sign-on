#!/bin/bash

# SSO API Documentation Build Script
# This script builds the documentation website using MkDocs Material

set -e  # Exit on error

echo "🚀 Building SSO API Documentation..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed"
    exit 1
fi

# Install documentation dependencies
echo "📦 Installing documentation dependencies..."
pip3 install -r requirements-docs.txt

# Build the documentation
echo "🔨 Building documentation site..."
mkdocs build --clean

echo "✅ Documentation built successfully!"
echo "📁 Output directory: site/"
echo "🌐 To serve locally, run: ./serve-docs.sh"
echo "🚀 To deploy, upload the 'site/' directory to your web server"