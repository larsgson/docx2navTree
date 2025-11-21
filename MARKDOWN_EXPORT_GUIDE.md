# Markdown Export Guide

This guide explains how to use the `split_to_md_chapters.py` reference script to convert your Word document into readable Markdown files.

## Overview

The `split_to_md_chapters.py` script is a **reference implementation** that demonstrates the same document processing logic as `build_book.py`, but generates human-readable Markdown files instead of JSON. This makes it perfect for:

- **Learning**: Understanding how the conversion system works
- **Verification**: Comparing Markdown output with chapter-viewer display
- **Documentation**: Creating readable documentation from your Word files
- **Archival**: Storing content in a universal, portable format
- **Alternative Exports**: Using Markdown as a base for other formats (HTML, PDF, EPUB)
- **WMF Conversion**: Automatically converts Windows Metafile images to PNG

## Quick Start

### Basic Usage

```bash
# Run the script
python3 split_to_md_chapters.py

# Or use the Makefile shortcut
make split-markdown
```

### Output Structure

The script creates a `markdown_chapters/` directory with the following structure:

```
markdown_chapters/
├── README.md                        # Main index with navigation
├── chapter_01/
│   ├── README.md                    # Chapter index
│   ├── section_1_0.md               # Chapter heading section
│   ├── section_1_1.md               # First section
│   ├── section_1_2.md               # Second section
│   └── pictures/
│       ├── image_0001.png
│       ├── image_0002.jpg
│       ├── image_0008.png           # Converted from WMF
│       ├── image_0008.wmf.backup    # Original WMF backup
│       └── ...
├── chapter_02/
│   ├── README.md
│   ├── section_2_0.md
│   └── ...
└── ...
```

## What Gets Converted

### Text Formatting

The script preserves all text formatting using Markdown syntax:

| Word Format | Markdown Output | Example |
|-------------|----------------|---------|
| **Bold** | `**text**` | **bold text** |
| *Italic* | `*text*` | *italic text* |
| ***Bold + Italic*** | `***text***` | ***both*** |
| <u>Underline</u> | `<u>text</u>` | <u>underlined</u> (HTML) |

### Headings

Headings are automatically detected and converted:

- **Chapter headings** (N.0) → `# Heading` (H1)
- **Section headings** (N.1, N.2) → `## Heading` (H2)
- **Subsection headings** (N.X.Y) → `### Heading` (H3)
- **Sub-subsections** → `#### Heading` (H4)

### Tables

Tables are converted to Markdown table format:

**Word Table:**
```
┌─────────┬─────────┐
│ Header1 │ Header2 │
├─────────┼─────────┤
│ Cell A  │ Cell B  │
│ Cell C  │ Cell D  │
└─────────┴─────────┘
```

**Markdown Output:**
```markdown
| Header1 | Header2 |
| --- | --- |
| Cell A | Cell B |
| Cell C | Cell D |
```

### Images

Images are extracted and referenced with proper paths:

```markdown
![Image 1](pictures/image_0001.png)
```

- **Supported formats**: PNG, JPG, GIF
- **WMF images**: Automatically converted to PNG (requires ImageMagick and Ghostscript)
- **Paths**: Relative to the section file for portability

### Footnotes

Footnote references are preserved using Markdown syntax:

```markdown
This is text with a footnote.[^1]

[^1]: Footnote content here
```

## Viewing the Output

### Markdown Viewers

Open the generated files in any Markdown viewer:

- **VS Code**: Built-in Markdown preview (`Cmd+Shift+V` or `Ctrl+Shift+V`)
- **Typora**: Beautiful WYSIWYG Markdown editor
- **MacDown**: Lightweight macOS Markdown editor
- **Mark Text**: Cross-platform Markdown editor
- **Web browsers**: Install Markdown viewer extensions

### GitHub

Push the `markdown_chapters/` directory to GitHub for automatic rendering:

```bash
git add markdown_chapters/
git commit -m "Add Markdown export"
git push
```

GitHub will render all `.md` files with proper formatting and clickable navigation.

### Static Site Generators

Use the Markdown files with static site generators:

- **Jekyll**: GitHub Pages compatible
- **Hugo**: Fast static site generator
- **MkDocs**: Project documentation sites
- **Docusaurus**: Modern documentation websites
- **Gatsby**: React-based static sites

## Comparison with JSON Output

| Feature | JSON Output (`build_book.py`) | Markdown Output (`split_to_md_chapters.py`) |
|---------|-------------------------------|---------------------------------------------|
| **Purpose** | Production viewer data | Reference/documentation |
| **Format** | Structured JSON | Human-readable Markdown |
| **Formatting** | Preserved in data | Rendered as Markdown syntax |
| **Tables** | Array of cell objects | Markdown table format |
| **Images** | Metadata + references | Markdown image links |
| **Optimization** | 47% size reduction | Full formatting preserved |
| **WMF Conversion** | Manual (separate step) | Automatic (on-the-fly) |
| **Use Case** | Chapter viewer app | Reading, learning, docs |
| **Editable** | Machine-readable | Directly human-editable |

## Customization

### Change Input File

Edit the script's configuration:

```python
# In split_to_md_chapters.py
INPUT_DOCX = "Your-Document.docx"
MARKDOWN_DIR = "custom_output_directory"
```

### Modify Formatting

Adjust the formatting functions to customize output:

- `format_run_markdown()` - Text formatting
- `extract_table_markdown()` - Table formatting
- `extract_paragraph_markdown()` - Paragraph structure

### Add Features

The script is designed to be extended. You can add:

- Custom CSS styling in HTML export
- Code block detection and formatting
- Cross-reference linking
- Automatic table of contents generation
- Custom metadata in frontmatter

## Advanced Usage

### Batch Processing

Process multiple documents:

```bash
for docx in *.docx; do
    python3 split_to_md_chapters.py "$docx"
done
```

### Pipeline Integration

Use as part of a documentation pipeline:

```bash
# Convert to Markdown
python3 split_to_md_chapters.py

# Generate static site
cd markdown_chapters
mkdocs build

# Or generate PDF
pandoc **/*.md -o book.pdf
```

### Custom Post-Processing

Process the generated Markdown:

```python
import os
from pathlib import Path

# Add custom metadata to all files
for md_file in Path("markdown_chapters").rglob("*.md"):
    content = md_file.read_text()
    
    # Add frontmatter
    frontmatter = "---\ntitle: Custom Title\nauthor: Your Name\n---\n\n"
    
    md_file.write_text(frontmatter + content)
```

## Troubleshooting

### Images Not Displaying

**Problem**: Images show as broken links

**Solutions**:
1. Ensure image paths are correct relative to the Markdown file
2. Check that images were extracted to `pictures/` directory
3. Some viewers may need absolute paths or base URL configuration

### Table Formatting Issues

**Problem**: Tables don't render correctly

**Solutions**:
1. Ensure your viewer supports Markdown tables
2. Check for pipe characters (`|`) in cell content (should be escaped as `\|`)
3. Complex nested tables may need manual adjustment

### WMF Images

**Problem**: WMF images don't display

**Solutions**:
1. The script automatically converts WMF to PNG if ImageMagick and Ghostscript are installed
2. If conversion fails, ensure dependencies are installed:
   ```bash
   # macOS
   brew install imagemagick ghostscript
   
   # Linux
   sudo apt-get install imagemagick ghostscript libreoffice
   ```
3. Check the script output for conversion status messages
4. Original WMF files are backed up as `.wmf.backup`

### Character Encoding

**Problem**: Special characters display incorrectly

**Solutions**:
1. The script uses UTF-8 encoding by default
2. Ensure your viewer/editor is set to UTF-8
3. Check that the source Word document uses proper character encoding

### Large Documents

**Problem**: Script is slow or fails on very large documents

**Solutions**:
1. Process chapters individually by modifying the script
2. Increase Python memory limit if needed
3. Process in batches by chapter range

## Differences from Chapter Viewer

While the Markdown output closely matches the chapter-viewer display, there are some differences:

### Similarities ✅

- Text formatting (bold, italic)
- Heading hierarchy
- Image inclusion
- Table structure
- Section organization

### Differences ⚠️

- **Interactive features**: The viewer has navigation, search, etc.
- **Styling**: Viewer uses custom CSS, Markdown uses viewer's theme
- **Image sizing**: Viewer controls dimensions, Markdown relies on viewer
- **Footnotes**: Viewer may display differently than Markdown footnotes
- **Tables**: Complex table layouts may differ in rendering

## Best Practices

1. **Always verify output**: Review at least a few chapters after conversion
2. **Check images**: Ensure all images extracted correctly
3. **Test tables**: Complex tables may need manual adjustment
4. **Use version control**: Track changes to Markdown files with Git
5. **Document customizations**: If you modify the script, document changes
6. **Keep originals**: Always preserve the original Word document

## Examples

### Example Output

Here's what a typical section looks like:

```markdown
# 1.1 Introduction to Animal Health

**Chapter 1 - Section 1.1**

---

This chapter introduces **basic concepts** of animal health and disease prevention.

## Key Topics

- Disease identification
- *Preventive measures*
- Treatment protocols

### Common Diseases

The following table summarizes common diseases:

| Disease | Symptoms | Treatment |
| --- | --- | --- |
| Disease A | Fever, lethargy | Antibiotic therapy |
| Disease B | Coughing, weight loss | Supportive care |

![Symptom diagram](pictures/image_0001.png)

For more information, see the references.[^1]

[^1]: Reference citation here
```

## Integration with Existing Tools

### With Chapter Viewer

The Markdown export complements the chapter viewer:

```bash
# Build JSON for viewer
make build

# Also generate Markdown for documentation
make split-markdown

# Now you have both:
# - Interactive viewer: http://localhost:3000
# - Static documentation: markdown_chapters/
```

### With Documentation Sites

Deploy alongside your viewer:

```
website/
├── app/                    # Chapter viewer app
│   ├── index.html
│   └── book_content_json/
└── docs/                   # Markdown documentation
    ├── chapter_01/
    ├── chapter_02/
    └── ...
```

## Contributing

If you improve the Markdown export functionality:

1. Test with various document types
2. Ensure backwards compatibility
3. Update this guide with new features
4. Submit a pull request with examples

## Resources

- **Markdown Guide**: https://www.markdownguide.org/
- **CommonMark Spec**: https://commonmark.org/
- **GitHub Flavored Markdown**: https://github.github.com/gfm/
- **Markdown Cheatsheet**: https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet

## License

Like the main project, this script is licensed under GPL-3.0. See [LICENSE](LICENSE) for details.

---

**Questions or Issues?**

If you encounter problems or have suggestions for improving the Markdown export:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Review existing issues on GitHub
3. Create a new issue with:
   - Sample input/output
   - Expected vs actual behavior
   - System information

Happy documenting! 📝