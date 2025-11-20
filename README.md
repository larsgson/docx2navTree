# Animal Health Handbook - Document Conversion System

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Node.js](https://img.shields.io/badge/node.js-16+-green.svg)](https://nodejs.org/)

A comprehensive automated system to convert Microsoft Word documents into an interactive web-based reader with JSON content backend. Originally created for the Animal Health Handbook, this system can be adapted for any large document with chapter/section structure.

## Features

- 🚀 **One-command build** - Single `make build` converts entire document
- 📚 **Smart chapter detection** - Automatically identifies chapters and sections
- 🖼️ **Image extraction** - Extracts all images including WMF conversion
- 📊 **Table processing** - Preserves complex table structures
- 🎨 **Format preservation** - Maintains bold, italic, fonts, alignment
- 📦 **47% size optimization** - Intelligent removal of redundant data
- ✅ **TOC validation** - Cross-references table of contents with actual content
- 🔍 **Verification tools** - Built-in integrity checking
- 📱 **React web viewer** - Responsive mobile-friendly interface

## Quick Start

```bash
# 1. Install dependencies
make install-deps

# 2. Build the book
make build

# 3. Start the web viewer
make viewer
```

Open your browser to `http://localhost:3000` to view the book.

## System Requirements

### Required Dependencies

- **Python 3.8+** with python-docx
- **ImageMagick 7+** - Image processing
- **Ghostscript** - PDF to PNG conversion
- **LibreOffice** - WMF to PDF conversion
- **Node.js 16+** - Web viewer

### Installation

**macOS:**
```bash
brew install imagemagick ghostscript
brew install --cask libreoffice
make install-deps
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install imagemagick ghostscript libreoffice python3-pip nodejs npm
make install-deps
```

**macOS LibreOffice Setup:**

If LibreOffice was installed via DMG (not Homebrew), run:
```bash
make setup-libreoffice
```

This creates a symlink so ImageMagick can access LibreOffice.

## What It Does

### Build Pipeline

```
Word Document
    ↓
1. Extract chapters & sections
2. Parse text with formatting
3. Extract images (WMF → PNG)
4. Process tables
5. Optimize JSON (47% reduction)
6. Build navigation index
    ↓
Interactive Web Viewer
```

### Detailed Steps

1. **Chapter Detection** - Identifies chapters by N.0 headings (e.g., "1.0 Health")
2. **Section Splitting** - Subdivides chapters into N.X sections (e.g., "1.1", "1.2")
3. **TOC Extraction** - Extracts and validates Table of Contents
4. **Content Parsing** - Preserves formatting, images, tables, footnotes
5. **WMF Conversion** - Converts Windows Metafiles to PNG via LibreOffice → PDF → PNG
6. **JSON Optimization** - Removes empty arrays, objects, default values
7. **Index Building** - Creates navigation structure with statistics

## Usage

### Build Commands

```bash
make build           # Build complete book content
make rebuild-all     # Clean and rebuild from scratch
make clean           # Remove generated files
```

### Development Commands

```bash
make dev             # Build and start viewer in one command
make viewer          # Start chapter-viewer dev server
make status          # Show current project status
make stats           # Display content statistics
```

### Verification Commands

```bash
make check-deps      # Verify all dependencies installed
make verify          # Check image integrity and content
```

## Project Structure

```
pp-book/
├── build_book.py                    # Main build system
├── Makefile                         # Build automation
├── setup_libreoffice.sh             # LibreOffice configuration helper
├── LICENSE                          # GPL-3.0 license
│
├── English HAH Word Apr 6 2024.docx # Source document (not in repo)
│
├── book_content_json/               # Generated content (not in repo)
│   ├── index.json                   # Navigation index
│   ├── toc_structure.json           # Table of contents
│   ├── toc_validation_report.json   # TOC validation results
│   └── chapter_XX/                  # Chapter directories
│       ├── section_XX.json          # Section content
│       └── pictures/                # Extracted images
│           └── image_XXXX.png
│
└── chapter-viewer/                  # React web application
    ├── src/                         # React source code
    ├── public/
    │   └── book_content_json/       # Deployed content
    └── package.json
```

## Output Format

### JSON Structure

Each section file contains:
```json
{
  "chapter_number": 1,
  "chapter_title": "1.0 HEALTH & DISEASE",
  "content": [
    {
      "type": "paragraph",
      "index": 0,
      "text": "Full paragraph text",
      "runs": [
        {"text": "Bold text", "bold": true, "font_size": 12.0}
      ],
      "alignment": "LEFT (0)"
    },
    {
      "type": "table",
      "rows": 3,
      "cols": 2,
      "cells": [...]
    }
  ],
  "statistics": {
    "paragraphs": 78,
    "tables": 1,
    "images": 10
  }
}
```

## Key Features

### Smart Chapter Detection

Handles both standard chapters (N.0 format) and appendix-style chapters (starting with N.1):

- **Regular chapters:** Start with N.0 heading (e.g., "1.0 Introduction")
- **Appendix chapters:** Start with N.1 section (e.g., "24.1 Infectious Diseases")
- **29 total chapters** fully detected and processed

### TOC Validation System

- Extracts entire Table of Contents (433 entries)
- Excludes TOC paragraphs from actual content
- Cross-validates TOC against actual content
- Generates detailed discrepancy report
- Uses actual content titles as source of truth

### JSON Optimization

Achieves 47% file size reduction by removing:
- Empty arrays: `"images": []`, `"footnotes": []`
- Empty objects: `"formatting": {}`
- Empty text runs
- Common defaults: `"bold": false`, `"italic": false`

**Result:** 12.8 MB → 6.8 MB (6 MB savings)

See [JSON_OPTIMIZATION_GUIDE.md](JSON_OPTIMIZATION_GUIDE.md) for details.

### WMF Image Conversion

Automatically converts Windows Metafile images using the conversion chain:

```
WMF → LibreOffice → PDF → Ghostscript → PNG
```

Handles 35 WMF images (~3% of 1,066 total images).

## Configuration

Edit `build_book.py` to customize:

```python
INPUT_DOCX = "Your-Document.docx"
JSON_DIR = "book_content_json"
ENABLE_OPTIMIZATION = True          # JSON optimization
ENABLE_TOC_VALIDATION = True        # TOC validation
```

## Build Statistics

Typical results for Animal Health Handbook:

| Metric | Value |
|--------|-------|
| Chapters | 29 (100% detected) |
| Sections | 416 |
| Paragraphs | 12,389 |
| Tables | 70 |
| Images | 1,066 (35 WMF converted) |
| JSON Size | 6.8 MB (47% optimized) |
| Build Time | ~90-100 seconds |

## Troubleshooting

### WMF Images Not Converting

```bash
# Check if LibreOffice is accessible
libreoffice --version

# If not found, configure it
make setup-libreoffice

# Rebuild
make rebuild-all
```

### Images Not Loading in Viewer

```bash
# Check image integrity
make verify

# If issues found, rebuild
make rebuild-all
```

### Build Fails with Missing Dependencies

```bash
# Check what's missing
make check-deps

# Install dependencies
make install-deps
```

### Content Not Updating

```bash
# Clean and rebuild
make clean
make build

# Force browser refresh
# Chrome/Firefox: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows/Linux)
```

## Advanced Usage

### Custom Document Processing

To process your own Word document:

1. Place your `.docx` file in the project root
2. Update `INPUT_DOCX` in `build_book.py`
3. Adjust chapter detection patterns if needed (see `is_chapter_heading()`)
4. Run `make rebuild-all`

### Disabling Optimization

For debugging or compatibility:

```python
# In build_book.py
ENABLE_OPTIMIZATION = False
ENABLE_TOC_VALIDATION = False
```

### Accessing Validation Reports

After build, check:
- `book_content_json/toc_validation_report.json` - TOC discrepancies
- `book_content_json/toc_structure.json` - Extracted TOC

## Documentation

- **[JSON_OPTIMIZATION_GUIDE.md](JSON_OPTIMIZATION_GUIDE.md)** - Optimization details
- **[WMF_CONVERSION_GUIDE.md](WMF_CONVERSION_GUIDE.md)** - Image conversion guide
- **[chapter-viewer/README.md](chapter-viewer/README.md)** - Web viewer documentation

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run `make verify` to check integrity
5. Submit a pull request

## License

This project is licensed under the **GNU General Public License v3.0** (GPL-3.0).

This means you can:
- ✅ Use commercially
- ✅ Modify the code
- ✅ Distribute
- ✅ Use privately

Under the conditions:
- 📋 Disclose source
- 📋 License and copyright notice
- 📋 Same license for derivatives
- 📋 State changes made

See [LICENSE](LICENSE) file for full details.

## Authors

- Original development for Animal Health Handbook document conversion
- Authors: Dr. Peter Quesenberry and Dr. Maureen Birmingham (original handbook)

## Acknowledgments

- **python-docx** - Word document parsing
- **ImageMagick** - Image processing
- **LibreOffice** - Document conversion
- **React** - Web viewer interface
- **Vite** - Build tooling

## Support

For issues, questions, or suggestions:
1. Check the troubleshooting section above
2. Review existing issues on GitHub
3. Create a new issue with:
   - System information (OS, Python version, etc.)
   - Output of `make check-deps`
   - Error messages or unexpected behavior
   - Steps to reproduce

## Roadmap

Potential future enhancements:
- [ ] Support for more document formats (PDF, EPUB input)
- [ ] Full-text search in viewer
- [ ] Export to EPUB/PDF from JSON
- [ ] More aggressive image optimization
- [ ] Multi-language support
- [ ] Cloud deployment guides
- [ ] Docker containerization

---

**Note:** This repository does not include the source Word document or generated content. You'll need to provide your own document to process.