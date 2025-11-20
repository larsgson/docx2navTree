#!/bin/bash

# Setup LibreOffice for ImageMagick on macOS
# This script creates a symlink so ImageMagick can use LibreOffice to convert WMF files

set -e

echo "=========================================="
echo "LibreOffice Setup for ImageMagick"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if LibreOffice is installed
LIBREOFFICE_PATH="/Applications/LibreOffice.app/Contents/MacOS/soffice"

if [ ! -f "$LIBREOFFICE_PATH" ]; then
    echo -e "${RED}✗ LibreOffice not found at: $LIBREOFFICE_PATH${NC}"
    echo ""
    echo "Please install LibreOffice first:"
    echo "  Option 1: brew install --cask libreoffice"
    echo "  Option 2: Download from https://www.libreoffice.org/download/"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ LibreOffice found at: $LIBREOFFICE_PATH${NC}"
echo ""

# Check if libreoffice command already exists
if command -v libreoffice >/dev/null 2>&1; then
    echo -e "${GREEN}✓ 'libreoffice' command is already available${NC}"
    echo ""
    libreoffice --version
    echo ""
    echo "Setup complete! You can now run: make rebuild-all"
    exit 0
fi

echo -e "${YELLOW}⚠ 'libreoffice' command not found in PATH${NC}"
echo ""
echo "Creating symlink to make LibreOffice accessible to ImageMagick..."
echo ""

# Create /usr/local/bin if it doesn't exist
if [ ! -d "/usr/local/bin" ]; then
    echo "Creating /usr/local/bin directory..."
    sudo mkdir -p /usr/local/bin
    echo -e "${GREEN}✓ Created /usr/local/bin${NC}"
    echo ""
fi

# Create symlink
echo "Creating symlink..."
echo "  From: $LIBREOFFICE_PATH"
echo "  To:   /usr/local/bin/libreoffice"
echo ""

if sudo ln -sf "$LIBREOFFICE_PATH" /usr/local/bin/libreoffice; then
    echo -e "${GREEN}✓ Symlink created successfully${NC}"
    echo ""

    # Verify it works
    if command -v libreoffice >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Verification successful:${NC}"
        libreoffice --version
        echo ""
        echo -e "${GREEN}Setup complete!${NC}"
        echo ""
        echo "You can now convert WMF images by running:"
        echo "  make rebuild-all"
    else
        echo -e "${YELLOW}⚠ Symlink created but 'libreoffice' command still not found${NC}"
        echo ""
        echo "You may need to open a new terminal window."
        echo "Then test with: libreoffice --version"
    fi
else
    echo -e "${RED}✗ Failed to create symlink${NC}"
    echo ""
    echo "You can try manually:"
    echo "  sudo ln -sf $LIBREOFFICE_PATH /usr/local/bin/libreoffice"
    exit 1
fi

echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo "1. Open a new terminal (or run: source ~/.zshrc)"
echo "2. Test: libreoffice --version"
echo "3. Convert WMF images: make rebuild-all"
echo ""
