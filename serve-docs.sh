#!/bin/bash

# SSO API Documentation Development Server
# This script serves the documentation website locally for development

set -e  # Exit on error

echo "🚀 Starting SSO API Documentation Development Server..."

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

# Install documentation dependencies if not already installed
if ! pip3 show mkdocs-material &> /dev/null; then
    echo "📦 Installing documentation dependencies..."
    pip3 install -r requirements-docs.txt
fi

# Default values
PORT=${1:-8000}
HOST=${2:-127.0.0.1}

echo "🌐 Serving documentation at: http://${HOST}:${PORT}"
echo "📝 Auto-reload enabled - changes will be reflected automatically"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Serve the documentation with live reload
mkdocs serve --dev-addr "${HOST}:${PORT}"