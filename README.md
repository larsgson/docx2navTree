# docx2app - Document to JSON Converter

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Convert Microsoft Word documents into structured JSON content suitable for web applications, content management systems, or RAG (Retrieval-Augmented Generation) pipelines.

## Features

- **Automatic TOC extraction** - Identifies chapters and sections from Table of Contents
- **md2rag-compatible JSON output** - Structured format with navigation links
- **Image extraction** - Extracts all images including WMF to PNG conversion
- **Table processing** - Preserves complex table structures
- **Markdown export** - Optional parallel Markdown output
- **Smart title detection** - Extracts book title from document content

## Quick Start

```bash
# 1. Install dependencies
make install-deps

# 2. Configure your book (optional - auto-detects from document)
cp book_config.toml.example book_config.toml
# Edit book_config.toml with your book's details

# 3. Place your Word document
cp your-book.docx original-book.docx

# 4. Build
make build
```

Output is generated in `export/` (JSON) and `export_md/` (Markdown).

## Output Structure

```
export/
├── {lang}/                           # Language folder (e.g., "eng")
│   └── {book_id}/                    # Book ID folder
│       ├── _book.toml                # Book manifest
│       ├── 01/                       # Chapter 1
│       │   ├── intro.json            # Chapter intro
│       │   ├── 01.json               # Section 1.1
│       │   └── 02.json               # Section 1.2
│       └── 02/                       # Chapter 2
└── pictures/                         # Pictures at root level
    └── {lang}/
        └── {book_id}/
            └── 01/                   # Mirrors chapter/section numbers
                └── 01/
                    ├── 001.png
                    └── manifest.json

export_md/                            # Markdown export
└── {lang}/
    ├── README.md
    ├── style.css
    └── 01/                           # Chapter 1
        ├── intro.md
        ├── 01.md                     # Section 1.1
        └── 01_01.md                  # Subsection 1.1.1
```

## JSON Format (md2rag compatible)

### Book Manifest (`_book.toml`)

```toml
canonical_id = "my-book-title"
language = "eng"
title = "My Book Title"
is_original = true
```

### Section Files

Each section JSON file contains:

```json
{
  "id": "my-book-title/01/01",
  "title": "Section Title",
  "section_id": "chapter_name/section_name",
  "links": [
    {"type": "previous", "target": "my-book-title/01/intro"},
    {"type": "next", "target": "my-book-title/01/02"}
  ],
  "content": [
    {"type": "paragraph", "text": "Paragraph content..."},
    {"type": "image", "path": "pictures/01/01/001.png", "alt": "", "caption": ""},
    {"type": "table", "rows": [{"cells": [{"text": "Cell content"}]}]}
  ]
}
```

## Configuration

### Book Configuration (`book_config.toml`)

Copy from `book_config.toml.example` and customize:

```toml
# Unique identifier for cross-references between books
canonical_id = "my-book-title"

# ISO 639-2 language code
language = "eng"

# Book title (auto-detected from document if empty)
title = "My Book Title"

# Is this the original language version?
is_original = true

# For translations only:
# original_language = "eng"

# Where to store pictures: "root", "book", or "chapter"
pictures_location = "root"
```

If `title` is left empty, it will be extracted from:
1. DOCX metadata (if available)
2. First paragraph of the document

### Build Configuration

Edit `build_book.py` to customize paths:

```python
INPUT_DOCX = "original-book.docx"
MARKDOWN_DIR = "export_md"
ENABLE_MARKDOWN = True  # Set to False to disable Markdown export
```

## System Requirements

- **Python 3.8+** with python-docx
- **ImageMagick 7+** - Image processing
- **Ghostscript** - PDF to PNG conversion
- **LibreOffice** - WMF to PDF conversion (for Windows Metafile images)

### Installation

**macOS:**
```bash
brew install imagemagick ghostscript
brew install --cask libreoffice
make install-deps
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install imagemagick ghostscript libreoffice python3-pip
make install-deps
```

## Document Preparation

**Important:** Convert automatic numbering to fixed text before processing.

Word/LibreOffice automatic numbering stores section numbers invisibly, causing missing sections.

**Quick Fix:**
- **LibreOffice:** Select All → Format → Lists → No List → Save
- **Word:** Select All → Ctrl+Shift+N → Numbering → None → Save

See [DOCUMENT_PREPARATION_GUIDE.md](DOCUMENT_PREPARATION_GUIDE.md) for detailed instructions.

## Make Commands

```bash
make build           # Build book content to export/
make rebuild-all     # Clean and rebuild from scratch
make clean           # Remove generated files
make check-deps      # Verify dependencies installed
make verify          # Check image integrity
make status          # Show project status
make stats           # Display content statistics
```

## Exception Handling

If your document has known numbering inconsistencies, create `conf/exceptions.conf`:

```
# Format: wrong_number = correct_number
10.7.7 = 10.7.5
21.4.3 = 21.2.3
```

## Troubleshooting

### WMF Images Not Converting

```bash
# Check LibreOffice is accessible
libreoffice --version

# If not found on macOS
make setup-libreoffice

# Rebuild
make rebuild-all
```

### Missing Dependencies

```bash
make check-deps
make install-deps
```

### Build Errors

```bash
make clean
make build
```

## Documentation

- [DOCUMENT_PREPARATION_GUIDE.md](DOCUMENT_PREPARATION_GUIDE.md) - Document preparation
- [WMF_CONVERSION_GUIDE.md](WMF_CONVERSION_GUIDE.md) - Image conversion guide
- [MARKDOWN_GENERATION.md](MARKDOWN_GENERATION.md) - Markdown output guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

## License

GNU General Public License v3.0 (GPL-3.0) - See [LICENSE](LICENSE) file.

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Run `make verify` to check integrity
4. Submit a pull request
