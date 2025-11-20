# WMF Image Conversion Guide

## Overview

This project contains 35 Windows Metafile (WMF) images that need to be converted to PNG format for web display. WMF files are not natively supported by web browsers, so the build system automatically converts them.

## How WMF Conversion Works

The conversion uses a three-step chain:

```
WMF → (LibreOffice) → PDF → (Ghostscript) → PNG
```

**ImageMagick** orchestrates this process by:
1. Calling LibreOffice to convert WMF to PDF
2. Calling Ghostscript to convert PDF to PNG

## Required Software

All three tools must be installed and accessible:

### 1. ImageMagick
Orchestrates the conversion process.

**Install:**
```bash
# macOS
brew install imagemagick

# Linux
sudo apt-get install imagemagick
```

**Verify:**
```bash
magick --version
# or
convert --version
```

### 2. Ghostscript
Converts PDF to PNG format.

**Install:**
```bash
# macOS
brew install ghostscript

# Linux
sudo apt-get install ghostscript
```

**Verify:**
```bash
gs --version
```

### 3. LibreOffice
Converts WMF to PDF format.

**Install:**
```bash
# macOS (via Homebrew)
brew install --cask libreoffice

# macOS (via DMG)
# Download from: https://www.libreoffice.org/download/

# Linux
sudo apt-get install libreoffice
```

**Verify:**
```bash
libreoffice --version
```

## macOS Setup Issues

### Problem: LibreOffice Not Accessible to ImageMagick

If you installed LibreOffice from the DMG file (not Homebrew), it won't be in your PATH. ImageMagick won't be able to find it.

**Symptoms:**
- `libreoffice --version` works in your terminal
- Build script says "LibreOffice found but not accessible"
- WMF conversion fails

**Solution:**

#### Option 1: Use the Setup Script (Recommended)
```bash
make setup-libreoffice
```

This script will:
- Check if LibreOffice is installed
- Create `/usr/local/bin` if needed
- Create a symlink from `/usr/local/bin/libreoffice` to LibreOffice.app
- Verify the setup works

#### Option 2: Manual Symlink Creation
```bash
sudo mkdir -p /usr/local/bin
sudo ln -sf /Applications/LibreOffice.app/Contents/MacOS/soffice /usr/local/bin/libreoffice
```

**Verify:**
```bash
libreoffice --version
```

### Why Shell Aliases Don't Work

You might be tempted to add this to your `~/.zshrc` or `~/.bash_profile`:
```bash
alias libreoffice='/Applications/LibreOffice.app/Contents/MacOS/soffice'
```

**This won't work** for the build script because:
- Shell aliases only work in interactive shells
- Python's `subprocess.run()` doesn't inherit aliases
- ImageMagick needs an actual executable in the PATH

You **must** use the symlink approach for the build script to work.

## Troubleshooting

### Check All Dependencies

Run this to see what's installed:
```bash
make check-deps
```

### Test WMF Conversion Manually

1. Find a WMF file:
```bash
find book_content_json -name "*.png" -exec sh -c 'head -c 4 "$1" | xxd -p | grep -q "^d7cdc69a" && echo "$1"' _ {} \; | head -1
```

2. Copy it with .wmf extension:
```bash
cp book_content_json/chapter_XX/pictures/image_XXXX.png test.wmf
```

3. Try converting:
```bash
magick test.wmf test_converted.png
```

4. Check for errors:
   - `libreoffice: command not found` → LibreOffice not in PATH
   - `gs: command not found` → Ghostscript not installed
   - `delegate failed` → ImageMagick can't access LibreOffice

### Common Error Messages

#### "Ghostscript not found"
```
⚠️  Ghostscript not found - required for WMF conversion
```

**Fix:** Install Ghostscript
```bash
brew install ghostscript
```

#### "LibreOffice is installed but ImageMagick can't access it"
```
⚠️  LibreOffice is installed but ImageMagick can't access it!
```

**Fix:** Run the setup script
```bash
make setup-libreoffice
```

#### "delegate failed 'libreoffice'"
This means ImageMagick tried to call LibreOffice but couldn't find the command.

**Fix:** Create the symlink (see macOS Setup Issues above)

#### "gs: command not found" (in ImageMagick error)
ImageMagick found LibreOffice and created a PDF, but can't convert it to PNG.

**Fix:** Install Ghostscript
```bash
brew install ghostscript
```

## Quick Fix Summary

For a fresh macOS system, run these commands in order:

```bash
# 1. Install all dependencies
brew install imagemagick ghostscript
brew install --cask libreoffice

# 2. Set up LibreOffice for ImageMagick
make setup-libreoffice

# 3. Verify everything works
make check-deps

# 4. Build with WMF conversion
make rebuild-all
```

## Statistics

- **Total images:** 1,066
- **WMF images:** 35 (~3% of total)
- **PNG images:** 1,031 (97% of total)

The WMF images are scattered across multiple chapters. Without conversion, they will appear as broken images in the web viewer.

## Technical Details

### WMF File Detection

The build script detects WMF files by:
1. Looking at files with `.png` extension
2. Reading the file header (magic bytes)
3. Checking if the header matches WMF signature: `0xD7CDC69A`

### Conversion Process

For each WMF file:
1. ImageMagick calls: `libreoffice --convert-to pdf --outdir /tmp file.wmf`
2. LibreOffice creates: `file.pdf`
3. ImageMagick calls: `gs ... file.pdf file.png`
4. Ghostscript creates: `file.png`
5. Build script replaces the original `.png` file
6. Original WMF is saved as: `file.png.wmf.backup`

### Performance

- Conversion time: ~2-3 seconds per image
- Total time for 35 images: ~90-105 seconds

## Skipping WMF Conversion

If you don't want to install the required software, you can still build the project:

```bash
make build
```

The build will:
- ✅ Convert the Word document to JSON
- ✅ Extract all PNG images that are actually PNG
- ✅ Copy everything to the viewer
- ⚠️ Skip WMF conversion
- ⚠️ Show warnings about broken images

The 35 WMF images will appear broken in the web viewer, but the other 1,031 images will work fine.

## References

- ImageMagick: https://imagemagick.org/
- Ghostscript: https://www.ghostscript.com/
- LibreOffice: https://www.libreoffice.org/
- WMF Format: https://en.wikipedia.org/wiki/Windows_Metafile

## Getting Help

If you're still having trouble after following this guide:

1. Run `make check-deps` and share the output
2. Try a manual conversion (see Troubleshooting section)
3. Check the error messages in the build output
4. Verify all three tools are installed and accessible

The build script provides detailed error messages to help diagnose issues.