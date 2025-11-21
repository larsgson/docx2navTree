# Contributing to Animal Health Handbook Document Conversion System

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive experience for everyone. We expect all contributors to:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- Python 3.8 or higher
- Node.js 16 or higher
- Git installed and configured
- Basic understanding of Python, JavaScript, and React
- Familiarity with the project structure (see README.md)

### Development Setup

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/docx2app.git
   cd docx2app
   ```

2. **Install dependencies**
   ```bash
   make install-deps
   ```

3. **Verify your setup**
   ```bash
   make check-deps
   make status
   ```

4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **Bug fixes** - Fix issues in the build system or viewer
- **Feature enhancements** - Add new functionality
- **Documentation** - Improve guides, comments, or examples
- **Testing** - Add or improve test coverage
- **Performance** - Optimize build time or output size
- **Code quality** - Refactoring, cleanup, or modernization

### Areas Needing Help

Priority areas for contribution:

1. **Document Format Support**
   - Add support for PDF input
   - Add support for EPUB input
   - Support for more Word format variations

2. **Image Processing**
   - Better WMF conversion handling
   - Image optimization improvements
   - Support for more image formats

3. **Viewer Features**
   - Full-text search functionality
   - Bookmark/note-taking features
   - Print/export options
   - Accessibility improvements

4. **Build System**
   - Faster processing algorithms
   - Better error messages
   - Progress indicators
   - Incremental builds

5. **Testing**
   - Unit tests for build_book.py
   - Integration tests
   - End-to-end tests for viewer

## Coding Standards

### Python Code

Follow PEP 8 style guide:

```python
# Good
def convert_chapter_to_json(chapter_num, elements):
    """Convert a chapter's elements to JSON format.
    
    Args:
        chapter_num: Chapter number (int)
        elements: List of document elements
        
    Returns:
        dict: Chapter data in JSON format
    """
    chapter_data = {
        "number": chapter_num,
        "sections": []
    }
    return chapter_data

# Use descriptive variable names
image_counter = 0
section_title = "Introduction"

# Use type hints where helpful
def process_image(filepath: Path) -> bool:
    """Process and optimize an image."""
    pass
```

### JavaScript/React Code

Follow modern ES6+ conventions:

```javascript
// Good - Use const/let, arrow functions
const ChapterView = ({ chapterId }) => {
  const [content, setContent] = useState(null);
  
  useEffect(() => {
    loadChapterContent(chapterId);
  }, [chapterId]);
  
  return <div className="chapter">{content}</div>;
};

// Use descriptive names
const handleImageLoad = (event) => {
  console.log('Image loaded:', event.target.src);
};
```

### Documentation

- Add docstrings to all functions
- Comment complex logic
- Update README.md for user-facing changes
- Keep comments up-to-date

### Commit Messages

Use clear, descriptive commit messages:

```
# Good
feat: Add PDF export functionality to viewer
fix: Correct WMF image detection regex pattern
docs: Update installation instructions for Linux
refactor: Simplify chapter detection logic
test: Add unit tests for TOC extraction

# Bad
Update stuff
Fix bug
Changes
```

Format:
```
<type>: <short description>

<optional longer description>

<optional footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Testing Guidelines

### Before Submitting

1. **Test your changes**
   ```bash
   make clean
   make build
   make verify
   ```

2. **Check for errors**
   - No Python exceptions
   - No console errors in viewer
   - Images load correctly
   - Navigation works

3. **Test on different content**
   - Try with different Word documents if possible
   - Test edge cases (empty sections, large images, etc.)

### Adding Tests

If adding new functionality, please include tests:

```python
# Example test structure (future)
def test_chapter_detection():
    """Test that chapters are correctly detected."""
    doc = Document("test_document.docx")
    chapters = detect_chapters(doc)
    assert len(chapters) == 5
    assert chapters[0]["number"] == 1
```

## Pull Request Process

### Before Submitting PR

1. **Update your fork**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run verification**
   ```bash
   make check-deps
   make verify
   ```

3. **Update documentation**
   - Update README.md if needed
   - Add comments to complex code
   - Update relevant guides

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: Add feature description"
   git push origin feature/your-feature-name
   ```

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review of code completed
- [ ] Comments added for complex logic
- [ ] Documentation updated (if needed)
- [ ] No new warnings or errors
- [ ] Tested with sample documents
- [ ] PR description explains the changes
- [ ] Linked to relevant issue (if applicable)

### PR Template

When creating a PR, include:

**Description**
Clear description of what changed and why

**Type of Change**
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

**Testing Done**
Describe how you tested the changes

**Related Issues**
Closes #123 (if applicable)

**Screenshots** (if UI changes)
Before/after screenshots

## Reporting Bugs

### Before Reporting

1. Check existing issues
2. Try the latest version
3. Verify dependencies are up-to-date

### Bug Report Template

```markdown
**Describe the bug**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Run command '...'
2. See error '...'

**Expected behavior**
What you expected to happen

**System Information:**
- OS: [e.g. macOS 13.0]
- Python version: [e.g. 3.10.0]
- Node version: [e.g. 18.0.0]
- ImageMagick version: [output of `magick --version`]

**Additional context**
- Output of `make check-deps`
- Error messages
- Relevant log output
```

## Suggesting Enhancements

### Enhancement Request Template

```markdown
**Problem to solve**
What problem does this solve?

**Proposed solution**
How would you implement it?

**Alternatives considered**
What other approaches did you consider?

**Additional context**
Examples, mockups, references
```

## Development Tips

### Useful Commands

```bash
# Quick rebuild for testing
make rebuild-all

# Check what changed
make status
make stats

# Verify integrity
make verify

# Clean everything
make clean
```

### Debugging

```python
# Add debug output
print(f"DEBUG: Processing chapter {chapter_num}")
print(f"DEBUG: Found {len(elements)} elements")

# Use logging for production code
import logging
logging.info(f"Processing chapter {chapter_num}")
logging.warning(f"Unexpected format in section {section_id}")
```

### Common Pitfalls

1. **File paths** - Always use `Path` objects for cross-platform compatibility
2. **Encoding** - Always specify `encoding="utf-8"` when opening files
3. **Large files** - Be mindful of memory when processing large documents
4. **Git** - Don't commit generated content or large binary files

## Questions?

If you have questions:

1. Check the [README.md](README.md)
2. Review existing issues and PRs
3. Create a new issue with your question
4. Tag it with the `question` label

## License

By contributing, you agree that your contributions will be licensed under the GPL-3.0 License.

## Recognition

All contributors will be recognized in the project. Thank you for helping improve this project!