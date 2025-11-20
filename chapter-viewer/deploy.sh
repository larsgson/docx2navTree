#!/bin/bash

# Deployment script for Animal Health Handbook Chapter Viewer
# This script builds the production version and provides deployment options

set -e

echo "🚀 Animal Health Handbook - Deployment Script"
echo "=============================================="
echo ""

# Check if pnpm is installed
if ! command -v pnpm &> /dev/null; then
    echo "❌ Error: pnpm is not installed"
    echo "Install it with: npm install -g pnpm"
    exit 1
fi

echo "📦 Installing dependencies..."
pnpm install

echo ""
echo "🔨 Building production version..."
pnpm build

echo ""
echo "✅ Build completed successfully!"
echo ""
echo "📊 Build statistics:"
du -sh dist/
echo ""

echo "Deployment Options:"
echo "==================="
echo ""
echo "1. Preview locally:"
echo "   pnpm preview"
echo ""
echo "2. Deploy to static hosting (Netlify, Vercel, etc.):"
echo "   - Upload the 'dist' folder"
echo "   - Set build command: pnpm build"
echo "   - Set publish directory: dist"
echo ""
echo "3. Deploy to Apache/Nginx:"
echo "   - Copy 'dist' folder contents to web root"
echo "   - Ensure server has fallback to index.html for SPA routing"
echo ""
echo "4. Quick preview:"
echo "   cd dist && python -m http.server 8080"
echo ""
echo "5. Deploy with simple HTTP server:"
echo "   npx serve dist -p 8080"
echo ""

# Ask if user wants to preview
read -p "Would you like to preview the build now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🌐 Starting preview server..."
    pnpm preview
fi

echo ""
echo "✨ Deployment preparation complete!"
echo "The production files are in the 'dist' directory."