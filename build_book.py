#!/usr/bin/env python3
"""
Comprehensive Book Builder Script
==================================

This script does everything needed to prepare the book content for the chapter-viewer:
1. Split the Word document into chapters (DOCX files)
2. Convert chapters to JSON format with images
3. Detect and convert WMF images to PNG format automatically
4. Copy everything to chapter-viewer/public directory
5. Build the index.json file

Usage:
    python3 build_book.py

Requirements:
    - python-docx
    - ImageMagick (for WMF to PNG conversion)
"""

import json
import os
import re
import shutil
import subprocess
import sys
from io import BytesIO
from pathlib import Path

from docx import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph

# ============================================================================
# Configuration
# ============================================================================

INPUT_DOCX = "English HAH Word Apr 6 2024.docx"
JSON_DIR = "chapter-viewer/book_content_json"
VIEWER_PUBLIC_DIR = "chapter-viewer/public/book_content_json"
ENABLE_OPTIMIZATION = True  # Set to False to skip default value optimization
ENABLE_TOC_VALIDATION = True  # Set to False to skip TOC validation


# ============================================================================
# Color Output for Terminal
# ============================================================================


class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"
    BOLD = "\033[1m"


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'=' * 70}{Colors.END}\n")


def print_step(step_num, text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}Step {step_num}: {text}{Colors.END}")
    print(f"{Colors.BLUE}{'-' * 70}{Colors.END}")


def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")


def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def print_info(text):
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.END}")


# ============================================================================
# Utility Functions
# ============================================================================


def clean_toc_formatting(text):
    """Remove TOC formatting from title text (dots and page numbers).

    Examples:
        "1.3.3 Title ............... 14" -> "1.3.3 Title"
        "Chapter 5 .......... 42" -> "Chapter 5"
    """
    import re

    if not text:
        return text

    # Remove trailing dots and page numbers
    # Pattern: spaces, dots (with optional spaces), and ending numbers
    cleaned = re.sub(r"\s*\.+\s*\.+.*?\d+\s*$", "", text)

    # Also handle simple pattern: spaces followed by multiple dots followed by optional number
    cleaned = re.sub(r"\s+\.{2,}.*$", "", cleaned)

    return cleaned.strip()


def is_toc_entry(text):
    """Check if text looks like a TOC entry (has multiple dots)."""
    return text and "....." in text


def extract_toc_structure(doc):
    """Extract TOC entries from the document.

    Returns:
        dict: TOC structure with entries organized by chapter/section,
              and a set of paragraph texts that are TOC entries
    """
    print("Extracting Table of Contents...")

    toc_entries = []
    toc_paragraph_texts = set()

    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()

        if is_toc_entry(text):
            # Store the text for later comparison
            toc_paragraph_texts.add(text)

            # Clean the text and extract chapter/section number
            cleaned_text = clean_toc_formatting(text)

            # Try to match chapter/section pattern
            match = re.match(r"^(\d+)\.(\d+)", cleaned_text)
            if match:
                chapter_num = int(match.group(1))
                section_num = int(match.group(2))

                toc_entries.append(
                    {
                        "paragraph_index": i,
                        "chapter": chapter_num,
                        "section": section_num,
                        "title": cleaned_text,
                        "original": text,
                    }
                )
            else:
                # Might be intro or other section
                toc_entries.append(
                    {
                        "paragraph_index": i,
                        "chapter": None,
                        "section": None,
                        "title": cleaned_text,
                        "original": text,
                    }
                )

    print(f"  Found {len(toc_entries)} TOC entries")

    # Organize by chapter
    toc_by_chapter = {}
    for entry in toc_entries:
        if entry["chapter"] is not None:
            chapter_num = entry["chapter"]
            if chapter_num not in toc_by_chapter:
                toc_by_chapter[chapter_num] = []
            toc_by_chapter[chapter_num].append(entry)

    return {
        "entries": toc_entries,
        "by_chapter": toc_by_chapter,
        "paragraph_texts": toc_paragraph_texts,
    }


def should_skip_toc_paragraph(paragraph, toc_structure):
    """Check if a paragraph is part of the TOC and should be skipped."""
    if not toc_structure:
        return False

    # Check if this paragraph's text matches a TOC entry
    para_text = paragraph.text.strip()
    return para_text in toc_structure["paragraph_texts"]


def check_imagemagick():
    """Check if ImageMagick is installed."""
    try:
        result = subprocess.run(
            ["convert", "-version"], capture_output=True, text=True, timeout=5
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def check_ghostscript():
    """Check if Ghostscript is installed."""
    try:
        result = subprocess.run(
            ["gs", "--version"], capture_output=True, text=True, timeout=5
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def check_file_type(filepath):
    """Check if a file is a Windows Metafile."""
    try:
        result = subprocess.run(
            ["file", "-b", str(filepath)], capture_output=True, text=True, timeout=5
        )
        output = result.stdout.strip().lower()
        return "windows metafile" in output or "wmf" in output
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def find_libreoffice_soffice():
    """Find LibreOffice soffice executable in common locations."""
    # Common macOS locations
    macos_locations = [
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        "/usr/local/bin/soffice",
        "/opt/homebrew/bin/soffice",
    ]

    # Check if soffice is in PATH
    try:
        result = subprocess.run(
            ["which", "soffice"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return "soffice"
    except:
        pass

    # Check common macOS installation locations
    for location in macos_locations:
        if os.path.exists(location):
            return location

    return None


def convert_wmf_to_png(filepath):
    """Convert a WMF file to PNG using ImageMagick.

    ImageMagick will automatically handle the conversion chain:
    WMF -> (LibreOffice) -> PDF -> (Ghostscript) -> PNG
    """
    # Use .wmf extension (not .wmf.tmp) so ImageMagick recognizes the format
    temp_wmf = filepath.parent / f"{filepath.stem}_temp.wmf"
    temp_png = filepath.parent / f"{filepath.stem}_temp.png"

    try:
        # Rename file to .wmf extension so ImageMagick recognizes the format
        shutil.copy2(filepath, temp_wmf)

        # Convert WMF to PNG - ImageMagick handles PDF intermediate automatically
        result = subprocess.run(
            ["magick", str(temp_wmf), str(temp_png)],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0 and temp_png.exists():
            # Verify it's actually a PNG
            check_result = subprocess.run(
                ["file", "-b", str(temp_png)],
                capture_output=True,
                text=True,
            )
            if "PNG" not in check_result.stdout:
                # Not a proper PNG, fail
                if temp_wmf.exists():
                    temp_wmf.unlink()
                if temp_png.exists():
                    temp_png.unlink()
                return False

            # Backup original WMF file
            backup_path = filepath.with_suffix(".wmf.backup")
            shutil.copy2(filepath, backup_path)

            # Replace with converted PNG
            shutil.move(str(temp_png), str(filepath))

            # Clean up temp WMF file
            if temp_wmf.exists():
                temp_wmf.unlink()

            return True
        else:
            # Clean up temp files
            if temp_wmf.exists():
                temp_wmf.unlink()
            if temp_png.exists():
                temp_png.unlink()
            return False

    except Exception as e:
        # Clean up temp files
        if temp_wmf.exists():
            temp_wmf.unlink()
        if temp_png.exists():
            temp_png.unlink()
        return False


# ============================================================================
# Table Processing Functions
# ============================================================================


def split_cell_content(cell_text):
    """Split cell content by newlines into separate entries."""
    if not cell_text or cell_text.strip() == "":
        return [""]

    lines = [line.strip() for line in cell_text.split("\n")]
    lines = [line for line in lines if line]

    return lines if lines else [""]


def should_expand_table_rows(table_data):
    """Determine if a table needs row expansion."""
    if "cells" not in table_data or not table_data["cells"]:
        return False

    for row_idx, row in enumerate(table_data["cells"]):
        for cell in row:
            text = cell.get("text", "").strip()
            if "\n" in text and text:
                lines = split_cell_content(text)
                if len(lines) > 1:
                    return True

    return False


def expand_table_rows(table_data):
    """Expand table rows that have newline-separated content."""
    if not should_expand_table_rows(table_data):
        return table_data

    original_cells = table_data["cells"]
    original_rows = len(original_cells)

    # Analyze cells to find max splits
    max_splits_per_row = []
    for row in original_cells:
        max_splits = 1
        for cell in row:
            text = cell.get("text", "").strip()
            lines = split_cell_content(text)
            max_splits = max(max_splits, len(lines))
        max_splits_per_row.append(max_splits)

    # Expand rows
    expanded_cells = []
    for row_idx, row in enumerate(original_cells):
        splits_needed = max_splits_per_row[row_idx]

        if splits_needed == 1:
            expanded_cells.append(row)
        else:
            # Split each cell
            split_cells = []
            for cell in row:
                text = cell.get("text", "").strip()
                lines = split_cell_content(text)

                # Pad with empty strings if needed
                while len(lines) < splits_needed:
                    lines.append("")

                split_cells.append(lines)

            # Create new rows
            for split_idx in range(splits_needed):
                new_row = []
                for col_idx, cell in enumerate(row):
                    new_cell = {
                        "row": len(expanded_cells),
                        "col": col_idx,
                        "text": split_cells[col_idx][split_idx],
                    }

                    # Copy paragraphs if present
                    if "paragraphs" in cell and split_idx == 0:
                        new_cell["paragraphs"] = cell["paragraphs"]

                    new_row.append(new_cell)

                expanded_cells.append(new_row)

    # Update table data
    table_data["cells"] = expanded_cells
    table_data["rows"] = len(expanded_cells)
    table_data["expanded"] = True
    table_data["original_rows"] = original_rows

    return table_data


# ============================================================================
# Chapter Detection Functions
# ============================================================================


def is_chapter_heading(paragraph):
    """Check if paragraph is a chapter heading."""
    text = paragraph.text.strip()
    # Match N.0 format (e.g., "1.0 Health & Disease")
    # Can be bold, Heading 1 style, or just N.0 format
    if not text:
        return False

    # Check if it matches N.0 pattern
    if not re.match(r"^\d+\.0\s+", text):
        return False

    # Accept if it has bold formatting OR Heading 1 style
    has_bold = any(run.bold for run in paragraph.runs if run.text.strip())
    is_heading_style = paragraph.style and "Heading" in paragraph.style.name

    return has_bold or is_heading_style


def extract_chapter_number(paragraph):
    """Extract chapter number from heading."""
    match = re.match(r"^(\d+)\.0\s+", paragraph.text.strip())
    return int(match.group(1)) if match else None


def extract_section_number(paragraph):
    """Extract chapter and section number from paragraph (e.g., '19.1' -> (19, 1))."""
    text = paragraph.text.strip()
    match = re.match(r"^(\d+)\.(\d+)\s+", text)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None


def is_first_section_heading(paragraph):
    """Check if paragraph is a N.1 heading (first section of appendix-style chapter)."""
    text = paragraph.text.strip()
    # Match N.1 format
    match = re.match(r"^(\d+)\.1\s+", text)
    if not match:
        return False

    # Check formatting (bold or heading style)
    has_bold = any(run.bold for run in paragraph.runs if run.text.strip())
    is_heading_style = paragraph.style and "Heading" in paragraph.style.name

    return has_bold or is_heading_style


# ============================================================================
# Footnote Functions
# ============================================================================


def get_footnote_references_from_paragraph(paragraph):
    """Extract footnote references from a paragraph."""
    footnote_refs = []

    for run in paragraph.runs:
        footnote_reference = run._element.find(
            ".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}footnoteReference"
        )
        if footnote_reference is not None:
            footnote_id = footnote_reference.get(
                "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id"
            )
            if footnote_id:
                footnote_refs.append(footnote_id)

    return footnote_refs


def get_footnote_references_from_table(table):
    """Extract footnote references from a table."""
    footnote_refs = []

    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                refs = get_footnote_references_from_paragraph(paragraph)
                footnote_refs.extend(refs)

    return footnote_refs


# ============================================================================
# Content Extraction Functions
# ============================================================================


def extract_paragraph_json(
    paragraph, chapter_num, para_index, image_counter, image_dir, source_doc
):
    """Extract paragraph data to JSON format with image references."""

    # Use paragraph text as-is (TOC entries are now filtered out before this point)
    para_text = paragraph.text

    para_data = {
        "type": "paragraph",
        "index": para_index,
        "text": para_text,
        "runs": [],
        "images": [],
        "footnotes": [],
        "formatting": {},
    }

    # Extract alignment
    if paragraph.alignment is not None:
        para_data["alignment"] = str(paragraph.alignment)

    # Extract runs with formatting
    for run in paragraph.runs:
        run_data = {
            "text": run.text,
            "bold": run.bold,
            "italic": run.italic,
            "underline": run.underline,
        }

        if run.font.size:
            run_data["font_size"] = run.font.size.pt

        para_data["runs"].append(run_data)

    # Extract inline images
    for run in paragraph.runs:
        inline_shapes = run._element.findall(
            ".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}drawing"
        )

        for shape in inline_shapes:
            blip = shape.find(
                ".//{http://schemas.openxmlformats.org/drawingml/2006/main}blip"
            )
            if blip is not None:
                image_rId = blip.get(
                    "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"
                )

                if image_rId:
                    try:
                        image_part = source_doc.part.related_parts[image_rId]
                        image_bytes = image_part.blob

                        # Get image dimensions
                        extent = shape.find(
                            ".//{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}extent"
                        )
                        if extent is not None:
                            width = int(extent.get("cx", 0))
                            height = int(extent.get("cy", 0))
                            width_inches = width / 914400.0
                            height_inches = height / 914400.0
                        else:
                            width_inches = 3.0
                            height_inches = 3.0

                        # Determine image format
                        content_type = image_part.content_type
                        if "png" in content_type:
                            ext = "png"
                        elif "jpeg" in content_type or "jpg" in content_type:
                            ext = "jpg"
                        elif "gif" in content_type:
                            ext = "gif"
                        else:
                            ext = "png"

                        # Save image
                        image_filename = f"image_{image_counter:04d}.{ext}"
                        image_path = os.path.join(image_dir, image_filename)
                        with open(image_path, "wb") as f:
                            f.write(image_bytes)

                        # Add image reference
                        image_data = {
                            "filename": image_filename,
                            "path": f"pictures/{image_filename}",
                            "width_inches": width_inches,
                            "height_inches": height_inches,
                        }

                        para_data["images"].append(image_data)
                        image_counter += 1

                    except Exception as e:
                        print_warning(f"Could not extract image: {e}")

    # Extract footnote references
    footnote_refs = get_footnote_references_from_paragraph(paragraph)
    for ref_id in footnote_refs:
        para_data["footnotes"].append({"id": ref_id})

    return para_data, image_counter


def extract_table_json(table, table_index):
    """Extract table data to JSON format."""

    rows = len(table.rows)
    cols = len(table.columns) if table.columns else 0

    cells_data = []

    for row_idx, row in enumerate(table.rows):
        row_data = []
        for col_idx, cell in enumerate(row.cells):
            cell_data = {"row": row_idx, "col": col_idx, "text": cell.text.strip()}

            # Extract paragraphs with formatting
            paragraphs = []
            for para in cell.paragraphs:
                para_info = {"text": para.text.strip(), "runs": []}

                for run in para.runs:
                    run_info = {
                        "text": run.text,
                        "bold": run.bold,
                        "italic": run.italic,
                        "underline": run.underline,
                    }
                    para_info["runs"].append(run_info)

                if para_info["text"] or para_info["runs"]:
                    paragraphs.append(para_info)

            if paragraphs:
                cell_data["paragraphs"] = paragraphs

            row_data.append(cell_data)

        cells_data.append(row_data)

    table_data = {
        "type": "table",
        "index": table_index,
        "rows": rows,
        "cols": cols,
        "cells": cells_data,
    }

    # Apply table expansion
    table_data = expand_table_rows(table_data)

    return table_data


def get_document_elements(doc):
    """Get all elements (paragraphs and tables) in document order."""
    elements = []
    for element in doc.element.body:
        if isinstance(element, CT_P):
            elements.append(("paragraph", Paragraph(element, doc)))
        elif isinstance(element, CT_Tbl):
            elements.append(("table", Table(element, doc)))
    return elements


def collect_chapter_footnotes(elements):
    """Collect all footnote IDs referenced in a chapter."""
    footnote_ids = set()

    for elem_type, elem in elements:
        if elem_type == "paragraph":
            refs = get_footnote_references_from_paragraph(elem)
            footnote_ids.update(refs)
        elif elem_type == "table":
            refs = get_footnote_references_from_table(elem)
            footnote_ids.update(refs)

    return footnote_ids


def extract_footnotes_content(source_doc, footnote_ids):
    """Extract footnote content from the document."""
    footnotes = {}

    # If no footnote IDs to extract, return empty dict
    if not footnote_ids:
        return footnotes

    try:
        # Check if the document has a footnotes part
        if not hasattr(source_doc.part, "footnotes_part"):
            return footnotes

        footnotes_part = source_doc.part.footnotes_part
        if footnotes_part:
            for footnote_id in footnote_ids:
                footnote_elem = footnotes_part.element.find(
                    f'.//{{{footnotes_part.element.nsmap["w"]}}}footnote[@{{http://schemas.openxmlformats.org/wordprocessingml/2006/main}}id="{footnote_id}"]'
                )

                if footnote_elem is not None:
                    text_parts = []
                    for para_elem in footnote_elem.findall(
                        f".//{{{footnotes_part.element.nsmap['w']}}}p"
                    ):
                        para = Paragraph(para_elem, source_doc)
                        text_parts.append(para.text.strip())

                    footnote_text = " ".join(text_parts)
                    if footnote_text:
                        footnotes[footnote_id] = footnote_text
    except AttributeError:
        # Document doesn't have footnotes - this is normal
        pass
    except Exception as e:
        print_warning(f"Error extracting footnotes: {e}")

    return footnotes


# ============================================================================
# JSON Conversion (Direct from Word Document)
# ============================================================================


def convert_book_to_json():
    """Convert the Word document directly to JSON format, organized by chapters."""

    if not os.path.exists(INPUT_DOCX):
        print_error(f"Input file not found: {INPUT_DOCX}")
        return False

    # Create output directory
    os.makedirs(JSON_DIR, exist_ok=True)

    print(f"Loading document: {INPUT_DOCX}")
    source_doc = Document(INPUT_DOCX)

    # Extract TOC structure for validation
    toc_structure = None
    if ENABLE_TOC_VALIDATION:
        toc_structure = extract_toc_structure(source_doc)

    # Get all elements and group by chapter
    elements = get_document_elements(source_doc)

    # Find chapter boundaries
    chapters = []
    current_chapter = None
    current_elements = []

    for elem_type, elem in elements:
        # Skip TOC paragraphs
        if elem_type == "paragraph":
            if toc_structure and should_skip_toc_paragraph(elem, toc_structure):
                continue

        if elem_type == "paragraph" and is_chapter_heading(elem):
            # Save previous chapter
            if current_chapter is not None:
                chapters.append(
                    {"number": current_chapter, "elements": current_elements}
                )

            # Start new chapter
            chapter_num = extract_chapter_number(elem)
            if chapter_num is not None:
                current_chapter = chapter_num
                current_elements = [(elem_type, elem)]
        else:
            if current_chapter is not None:
                current_elements.append((elem_type, elem))

    # Save last chapter
    if current_chapter is not None:
        chapters.append({"number": current_chapter, "elements": current_elements})

    # Second pass: Find orphaned chapters (those that start with N.1 instead of N.0)
    # Track which chapters we already have
    existing_chapter_nums = {ch["number"] for ch in chapters}

    orphaned_chapters = []
    current_orphan = None
    orphan_elements = []

    for elem_type, elem in elements:
        # Skip TOC paragraphs
        if elem_type == "paragraph":
            if toc_structure and should_skip_toc_paragraph(elem, toc_structure):
                continue

        # Check if this is a chapter heading (N.0) - should stop orphaned chapter
        if elem_type == "paragraph" and is_chapter_heading(elem):
            # This is a N.0 heading, which means the orphaned chapter has ended
            if current_orphan is not None:
                orphaned_chapters.append(
                    {"number": current_orphan, "elements": orphan_elements}
                )
                current_orphan = None
                orphan_elements = []
            # Don't add this element - it belongs to a regular chapter
            continue

        if elem_type == "paragraph" and is_first_section_heading(elem):
            chapter_num, _ = extract_section_number(elem)

            # Only create chapter if it doesn't already exist and this is truly the first section
            if chapter_num and chapter_num not in existing_chapter_nums:
                # Save previous orphaned chapter
                if current_orphan is not None:
                    orphaned_chapters.append(
                        {"number": current_orphan, "elements": orphan_elements}
                    )

                # Start new orphaned chapter
                current_orphan = chapter_num
                orphan_elements = [(elem_type, elem)]
                existing_chapter_nums.add(chapter_num)
        else:
            # Add to current orphaned chapter
            if current_orphan is not None:
                orphan_elements.append((elem_type, elem))

    # Save last orphaned chapter
    if current_orphan is not None:
        orphaned_chapters.append(
            {"number": current_orphan, "elements": orphan_elements}
        )

    # Merge and sort all chapters
    all_chapters = chapters + orphaned_chapters
    all_chapters.sort(key=lambda x: x["number"])

    if orphaned_chapters:
        print(
            f"Found {len(orphaned_chapters)} appendix-style chapters without N.0 headings"
        )

    print(f"Converting {len(all_chapters)} chapters to JSON...")

    # Validation report
    validation_report = []

    total_stats = {
        "chapters": 0,
        "sections": 0,
        "paragraphs": 0,
        "tables": 0,
        "images": 0,
    }

    for chapter_data in all_chapters:
        chapter_num = chapter_data["number"]
        elements = chapter_data["elements"]

        print(f"\n  Processing Chapter {chapter_num}...")

        # Create chapter directory
        chapter_dir = os.path.join(JSON_DIR, f"chapter_{chapter_num:02d}")
        os.makedirs(chapter_dir, exist_ok=True)

        # Create pictures directory
        pictures_dir = os.path.join(chapter_dir, "pictures")
        os.makedirs(pictures_dir, exist_ok=True)

        # Find section headings (N.X pattern)
        section_indices = []
        for i, (elem_type, elem) in enumerate(elements):
            if elem_type == "paragraph":
                text = elem.text.strip()
                if re.match(rf"^{chapter_num}\.\d+", text):
                    section_indices.append(i)

        # Split into sections
        sections = []
        if section_indices:
            # Intro section (before first N.X)
            sections.append(("intro", elements[: section_indices[0]]))

            # Numbered sections
            for i, start_idx in enumerate(section_indices):
                end_idx = (
                    section_indices[i + 1]
                    if i + 1 < len(section_indices)
                    else len(elements)
                )
                section_num = i + 1
                sections.append((section_num, elements[start_idx:end_idx]))
        else:
            # No sections, entire chapter is intro
            sections.append(("intro", elements))

        # Process each section
        image_counter = 1

        for section_id, section_elements in sections:
            content_items = []
            para_index = 0
            table_index = 0

            for elem_type, elem in section_elements:
                if elem_type == "paragraph":
                    para_data, image_counter = extract_paragraph_json(
                        elem,
                        chapter_num,
                        para_index,
                        image_counter,
                        pictures_dir,
                        source_doc,
                    )
                    content_items.append(para_data)
                    para_index += 1

                elif elem_type == "table":
                    table_data = extract_table_json(elem, table_index)
                    content_items.append(table_data)
                    table_index += 1

            # Collect footnotes
            footnote_ids = collect_chapter_footnotes(section_elements)
            footnotes = extract_footnotes_content(source_doc, footnote_ids)

            # Calculate statistics
            num_paragraphs = sum(
                1 for item in content_items if item["type"] == "paragraph"
            )
            num_tables = sum(1 for item in content_items if item["type"] == "table")
            num_images = sum(
                len(item.get("images", []))
                for item in content_items
                if item["type"] == "paragraph"
            )

            # Get section title (from actual content, not TOC)
            section_title = None
            for item in content_items:
                if item.get("type") == "paragraph" and item.get("text"):
                    raw_title = item["text"].strip()
                    # Don't use TOC-formatted text as title
                    if not is_toc_entry(raw_title):
                        section_title = raw_title
                        break

            # For appendix-style chapters, if this is the first section and no title found,
            # try to get it from TOC
            if not section_title and section_id == 1 and toc_structure:
                if chapter_num in toc_structure["by_chapter"]:
                    # Use chapter name from TOC for first section
                    for toc_entry in toc_structure["by_chapter"][chapter_num]:
                        if toc_entry["section"] == 0:  # Chapter-level TOC entry
                            section_title = f"{chapter_num}.0 {toc_entry['title'].split(' ', 1)[1] if ' ' in toc_entry['title'] else toc_entry['title']}"
                            break

            # Validate against TOC if enabled
            if ENABLE_TOC_VALIDATION and toc_structure and section_title:
                # Try to find matching TOC entry
                if chapter_num in toc_structure["by_chapter"]:
                    toc_entries = toc_structure["by_chapter"][chapter_num]

                    # Find matching section
                    section_match = None
                    for toc_entry in toc_entries:
                        if toc_entry["section"] == section_id:
                            section_match = toc_entry
                            break

                    if section_match:
                        # Compare titles
                        toc_title = section_match["title"]
                        if section_title != toc_title:
                            validation_report.append(
                                {
                                    "chapter": chapter_num,
                                    "section": section_id,
                                    "toc_title": toc_title,
                                    "actual_title": section_title,
                                    "message": "Title mismatch between TOC and content",
                                }
                            )
                    else:
                        validation_report.append(
                            {
                                "chapter": chapter_num,
                                "section": section_id,
                                "toc_title": None,
                                "actual_title": section_title,
                                "message": "Section not found in TOC",
                            }
                        )

            # Build section JSON
            section_json = {
                "chapter_number": chapter_num,
                "chapter_title": section_title or f"Chapter {chapter_num}",
                "content": content_items,
                "footnotes": footnotes,
                "statistics": {
                    "paragraphs": num_paragraphs,
                    "tables": num_tables,
                    "images": num_images,
                },
            }

            # Save section file
            if section_id == "intro":
                filename = "chapter.json"
            else:
                filename = f"section_{section_id:02d}.json"

            filepath = os.path.join(chapter_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(section_json, f, indent=2, ensure_ascii=False)

            print(
                f"    Saved: {filename} ({num_paragraphs} paras, {num_tables} tables, {num_images} images)"
            )

            # Update stats
            total_stats["sections"] += 1
            total_stats["paragraphs"] += num_paragraphs
            total_stats["tables"] += num_tables
            total_stats["images"] += num_images

        total_stats["chapters"] += 1

    print_success(
        f"Converted {total_stats['chapters']} chapters with {total_stats['sections']} sections"
    )

    # Save TOC structure for use in index building
    if toc_structure:
        toc_file = os.path.join(JSON_DIR, "toc_structure.json")
        with open(toc_file, "w", encoding="utf-8") as f:
            # Save only the entries and by_chapter structure (not paragraph_texts set)
            toc_data = {
                "entries": toc_structure["entries"],
                "by_chapter": toc_structure["by_chapter"],
            }
            json.dump(toc_data, f, indent=2, ensure_ascii=False)

    # Print validation report if there are discrepancies
    if ENABLE_TOC_VALIDATION and validation_report:
        print()
        print_warning(
            f"Found {len(validation_report)} discrepancies between TOC and content:"
        )
        print()

        for issue in validation_report[:20]:  # Show first 20
            chapter = issue["chapter"]
            section = issue["section"]
            print(f"  Chapter {chapter}, Section {section}:")
            if issue["toc_title"]:
                print(f"    TOC:     {issue['toc_title'][:70]}")
            print(f"    Content: {issue['actual_title'][:70]}")
            print(f"    → {issue['message']}")
            print()

        if len(validation_report) > 20:
            print(f"  ... and {len(validation_report) - 20} more discrepancies")
            print()

        # Save detailed report to file
        report_file = os.path.join(JSON_DIR, "toc_validation_report.json")
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(validation_report, f, indent=2, ensure_ascii=False)
        print_info(f"Full validation report saved to: {report_file}")
        print()
    elif ENABLE_TOC_VALIDATION:
        print_success("✅ All titles match between TOC and content")

    print_info(
        f"Total: {total_stats['paragraphs']} paragraphs, {total_stats['tables']} tables, {total_stats['images']} images"
    )

    return True


# ============================================================================
# JSON Optimization (Step 2)
# ============================================================================


def optimize_json_files():
    """Optimize JSON files by removing common default values and empty placeholders."""

    if not ENABLE_OPTIMIZATION:
        print("Optimization disabled, skipping...")
        return True

    print("Optimizing JSON files (removing defaults and empty placeholders)...")

    from collections import Counter, defaultdict

    # Collect statistics about all values
    stats = defaultdict(Counter)
    json_path = Path(JSON_DIR)

    json_files = list(json_path.rglob("*.json"))
    if not json_files:
        print_warning("No JSON files found to optimize")
        return True

    print(f"Analyzing {len(json_files)} JSON files...")

    # Calculate size before optimization
    size_before = sum(f.stat().st_size for f in json_files)

    # Collect value statistics from all JSON files
    for json_file in json_files:
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                collect_value_stats(data, stats)
        except Exception as e:
            print_warning(f"Error analyzing {json_file.name}: {e}")

    # Find common default values (appearing in >60% of cases)
    defaults = extract_defaults(stats, len(json_files))

    if not defaults:
        print("No common defaults found to optimize")
        return True

    print(f"Found {len(defaults)} common default values")

    # Apply optimization to all files
    optimized_count = 0
    for json_file in json_files:
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Remove default values
            optimized_data = remove_defaults(data, defaults)

            # Save optimized version
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(optimized_data, f, indent=2, ensure_ascii=False)

            optimized_count += 1
        except Exception as e:
            print_warning(f"Error optimizing {json_file.name}: {e}")

    # Calculate size after optimization
    size_after = sum(f.stat().st_size for f in json_files)
    savings = size_before - size_after
    percent = int(100 * savings / size_before) if size_before > 0 else 0

    print_success(f"Optimized {optimized_count} JSON files")
    print(
        f"  Size before: {size_before / 1024 / 1024:.2f} MB → After: {size_after / 1024 / 1024:.2f} MB"
    )
    print(f"  Savings: {savings / 1024 / 1024:.2f} MB ({percent}%)")
    print(f"  Removed: empty arrays, empty objects, empty runs, default values")
    return True


def collect_value_stats(obj, stats, path=""):
    """Recursively collect statistics about values in JSON."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            current_path = f"{path}.{key}" if path else key

            # Skip unique keys
            skip_keys = {
                "index",
                "number",
                "chapter_number",
                "row",
                "col",
                "id",
                "text",
                "filename",
                "path",
                "title",
                "chapter_title",
            }

            if key in skip_keys:
                continue

            if isinstance(value, (str, int, float, bool, type(None))):
                stats[current_path][str(value)] += 1
            elif isinstance(value, list):
                for item in value:
                    collect_value_stats(item, stats, current_path)
            elif isinstance(value, dict):
                collect_value_stats(value, stats, current_path)

    elif isinstance(obj, list):
        for item in obj:
            collect_value_stats(item, stats, path)


def extract_defaults(stats, total_files, min_frequency=0.6):
    """Extract values that appear frequently enough to be defaults."""
    defaults = {}

    for path, counter in stats.items():
        if not counter:
            continue

        most_common_value, count = counter.most_common(1)[0]
        frequency = count / total_files

        if frequency >= min_frequency and count >= 10:
            # Parse the value back to correct type
            try:
                if most_common_value == "None":
                    defaults[path] = None
                elif most_common_value == "True":
                    defaults[path] = True
                elif most_common_value == "False":
                    defaults[path] = False
                elif most_common_value.isdigit():
                    defaults[path] = int(most_common_value)
                else:
                    defaults[path] = most_common_value
            except:
                pass

    return defaults


def is_empty_value(value):
    """Check if a value is an empty placeholder that should be removed."""
    if value is None:
        return False  # Keep explicit None values
    if isinstance(value, str) and value == "":
        return True
    if isinstance(value, list) and len(value) == 0:
        return True
    if isinstance(value, dict) and len(value) == 0:
        return True
    return False


def remove_defaults(obj, defaults, path=""):
    """Recursively remove default values and empty placeholders from object."""
    if isinstance(obj, dict):
        new_dict = {}
        for key, value in obj.items():
            current_path = f"{path}.{key}" if path else key

            # Keys that should be kept even if empty (critical for structure)
            critical_keys = {
                "type",
                "index",
                "number",
                "chapter_number",
                "row",
                "col",
            }

            # Keys that are commonly empty and should be removed if empty
            removable_if_empty = {
                "text",
                "runs",
                "images",
                "footnotes",
                "formatting",
                "paragraphs",
            }

            # Process the value first if it's a container
            if isinstance(value, dict):
                processed_value = remove_defaults(value, defaults, current_path)
            elif isinstance(value, list):
                processed_value = remove_defaults(value, defaults, current_path)
            else:
                processed_value = value

            # Decide whether to keep this key
            should_skip = False

            # Don't remove critical keys
            if key in critical_keys:
                new_dict[key] = processed_value
                continue

            # Remove empty placeholders for removable keys
            if key in removable_if_empty and is_empty_value(processed_value):
                should_skip = True

            # Check if matches default value
            if (
                not should_skip
                and current_path in defaults
                and processed_value == defaults[current_path]
            ):
                should_skip = True

            # Remove any other empty structures (unless critical)
            if not should_skip and is_empty_value(processed_value):
                should_skip = True

            if not should_skip:
                new_dict[key] = processed_value

        return new_dict

    elif isinstance(obj, list):
        # Process each item and filter out any that became empty
        processed_list = []
        for item in obj:
            processed_item = remove_defaults(item, defaults, path)

            # Special handling for runs: filter out runs with no text
            if path.endswith("runs") and isinstance(processed_item, dict):
                # Skip runs that have no text or empty text
                if "text" not in processed_item or processed_item.get("text", "") == "":
                    continue

            # Keep non-empty items, but don't filter out items with only critical keys
            if not is_empty_value(processed_item):
                processed_list.append(processed_item)
        return processed_list

    else:
        return obj


# ============================================================================
# WMF Conversion (Step 3)
# ============================================================================


def convert_wmf_images():
    """Find and convert all WMF images to PNG format."""

    has_imagemagick = check_imagemagick()

    if not has_imagemagick:
        print_warning("ImageMagick not found - skipping WMF conversion")
        print_info("To install ImageMagick: brew install imagemagick")
        return True

    # Check if Ghostscript is installed (required by ImageMagick for PDF conversion)
    has_ghostscript = check_ghostscript()

    if not has_ghostscript:
        print_warning("Ghostscript not found - required for WMF conversion")
        print_info("ImageMagick uses: LibreOffice (WMF→PDF) → Ghostscript (PDF→PNG)")
        print_info("To install Ghostscript: brew install ghostscript")
        print()
        print_info("Skipping WMF conversion until Ghostscript is installed")
        return True

    # Check if LibreOffice is accessible via 'libreoffice' command
    try:
        result = subprocess.run(
            ["libreoffice", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        libreoffice_accessible = result.returncode == 0
    except Exception:
        libreoffice_accessible = False

    # Find LibreOffice installation even if not accessible via command
    soffice_path = find_libreoffice_soffice()

    if not libreoffice_accessible and soffice_path:
        print_warning("⚠ LibreOffice is installed but not accessible to ImageMagick")
        print_info(f"  Found at: {soffice_path}")
        print_info(
            "  ImageMagick needs 'libreoffice' command in PATH to convert WMF files"
        )
        print_info("  See instructions below if WMF conversion fails.")
        print()

    print("Scanning for WMF files with .png extension...")

    # Find all .png files that are actually WMF
    wmf_files = []
    json_path = Path(JSON_DIR)

    for png_file in json_path.rglob("*.png"):
        if check_file_type(png_file):
            wmf_files.append(png_file)

    if not wmf_files:
        print_success("No WMF files found - all images are valid PNG format")
        return True

    print(f"Found {len(wmf_files)} WMF files to convert...")

    success_count = 0
    failed_count = 0

    for wmf_file in wmf_files:
        rel_path = wmf_file.relative_to(json_path)
        print(f"  Converting: {rel_path}...", end=" ")

        if convert_wmf_to_png(wmf_file):
            print(f"{Colors.GREEN}✓{Colors.END}")
            success_count += 1
        else:
            print(f"{Colors.RED}✗{Colors.END}")
            failed_count += 1

    if success_count > 0:
        print_success(f"Converted {success_count} WMF files to PNG")

    if failed_count > 0:
        print_warning(f"Failed to convert {failed_count} WMF files")
        print_warning(
            "ImageMagick requires LibreOffice AND Ghostscript to convert WMF files"
        )
        print_info("Conversion chain: WMF → (LibreOffice) → PDF → (Ghostscript) → PNG")
        print()

        # Check what's missing
        has_gs = check_ghostscript()
        soffice_path = find_libreoffice_soffice()

        if not has_gs:
            print_warning("✗ Ghostscript not found")
            print_info("Install Ghostscript: brew install ghostscript")
            print()

        # Check if LibreOffice is installed but not detected
        if soffice_path:
            print_info(f"✓ LibreOffice found at: {soffice_path}")
            print()
            print_warning("LibreOffice is installed but ImageMagick can't access it!")
            print_info("ImageMagick needs 'libreoffice' command in PATH")
            print()
            print_info("To fix this on macOS, choose one of these options:")
            print()
            print_info("Option 1: Create a symlink (recommended)")
            print_info("  sudo mkdir -p /usr/local/bin")
            print_info(
                "  sudo ln -sf /Applications/LibreOffice.app/Contents/MacOS/soffice /usr/local/bin/libreoffice"
            )
            print()
            print_info(
                "Option 2: Add alias to your shell profile (~/.zshrc or ~/.bash_profile)"
            )
            print_info(
                "  alias libreoffice='/Applications/LibreOffice.app/Contents/MacOS/soffice'"
            )
            print_info("  Then: source ~/.zshrc")
            print()
            print_info("After fixing, test with: libreoffice --version")
        else:
            print_warning("✗ LibreOffice not found on this system")
            print()
            print_info("Install options:")
            print_info("  1. Via Homebrew: brew install --cask libreoffice")
            print_info("  2. Download from: https://www.libreoffice.org/download/")
            print()

        print_info("After installing/fixing dependencies, run: make rebuild-all")
        print()
        print_info(
            f"Note: {failed_count} images (~{failed_count * 100 // len(wmf_files)}% of {len(wmf_files)}) will show as broken in browser"
        )
        print_info("The other images will display correctly")

    return True  # Don't fail the build for WMF conversion issues


# ============================================================================
# Copy to Viewer (Step 4)
# ============================================================================


def copy_to_viewer():
    """Create symlink in chapter-viewer public directory to book_content_json.

    This makes the viewer self-contained with data stored in chapter-viewer/book_content_json
    and accessible via public/book_content_json symlink.
    """

    if not os.path.exists(JSON_DIR):
        print_error(f"JSON directory not found: {JSON_DIR}")
        return False

    # Create viewer public directory if it doesn't exist
    viewer_public = Path(VIEWER_PUBLIC_DIR).parent
    viewer_public.mkdir(parents=True, exist_ok=True)

    viewer_path = Path(VIEWER_PUBLIC_DIR)

    # Remove existing symlink or directory
    if viewer_path.exists() or viewer_path.is_symlink():
        if viewer_path.is_symlink():
            print("Removing old symlink...")
            viewer_path.unlink()
        else:
            print("Removing old chapter-viewer content...")
            shutil.rmtree(viewer_path)

    # Create symlink from public/book_content_json to ../book_content_json
    print(f"Creating symlink: {VIEWER_PUBLIC_DIR} -> ../book_content_json")

    # Symlink target is relative: ../book_content_json (from public/ to chapter-viewer/)
    viewer_path.symlink_to("../book_content_json")

    # Count files in the actual data directory
    json_path = Path(JSON_DIR)
    file_count = sum(1 for _ in json_path.rglob("*") if _.is_file())

    print_success(f"Symlink created - {file_count} files accessible in viewer")
    print_info("Chapter-viewer is now self-contained and can be used standalone!")

    return True


# ============================================================================
# Build Index (Step 5)
# ============================================================================


def build_index():
    """Build index.json from the chapter structure."""

    source_path = Path(VIEWER_PUBLIC_DIR)

    if not source_path.exists():
        print_error(f"Viewer directory not found: {VIEWER_PUBLIC_DIR}")
        return False

    print("Building index from chapter structure...")

    # Load TOC structure if available
    toc_file = source_path / "toc_structure.json"
    toc_data = None
    if toc_file.exists():
        with open(toc_file, "r", encoding="utf-8") as f:
            toc_data = json.load(f)

    chapters = []
    chapter_dirs = sorted(source_path.glob("chapter_*"))

    for chapter_dir in chapter_dirs:
        match = re.match(r"chapter_(\d+)", chapter_dir.name)
        if not match:
            continue

        chapter_num = int(match.group(1))

        # Get chapter title from section_01.json (N.0 section)
        first_section_file = chapter_dir / "section_01.json"
        chapter_title = f"Chapter {chapter_num}"

        if first_section_file.exists():
            with open(first_section_file, "r", encoding="utf-8") as f:
                first_section_data = json.load(f)
                chapter_title = first_section_data.get(
                    "chapter_title", f"Chapter {chapter_num}"
                )

                # For appendix-style chapters (starting with N.1), get title from TOC
                if chapter_title.startswith(f"{chapter_num}.1") and toc_data:
                    # Look for N.0 entry in TOC
                    if str(chapter_num) in toc_data.get("by_chapter", {}):
                        for entry in toc_data["by_chapter"][str(chapter_num)]:
                            if entry["section"] == 0:
                                chapter_title = entry["title"]
                                break

        # Scan sections
        sections = []

        # Add numbered sections (renumbered to start from 0)
        section_files = sorted(chapter_dir.glob("section_*.json"))
        for idx, section_file in enumerate(section_files):
            match = re.match(r"section_(\d+)\.json", section_file.name)
            if match:
                with open(section_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Get section title from first paragraph
                title = None
                for item in data.get("content", []):
                    if item.get("type") == "paragraph" and item.get("text"):
                        title = item["text"].strip()
                        break

                sections.append(
                    {
                        "section_number": idx,  # Renumber: 0, 1, 2, 3...
                        "title": title or f"Section {idx}",
                        "path": f"{chapter_dir.name}/{section_file.name}",
                        "statistics": data.get("statistics", {}),
                    }
                )

        chapters.append(
            {
                "number": chapter_num,
                "title": chapter_title,
                "path": f"{chapter_dir.name}/section_01.json",  # Point to first section
                "sections": sections,
                "total_sections": len(sections),
            }
        )

        print(f"  Chapter {chapter_num}: {chapter_title} ({len(sections)} sections)")

    # Build index structure
    index = {
        "book_title": "Animal Health Handbook",
        "total_chapters": len(chapters),
        "total_sections": sum(c["total_sections"] for c in chapters),
        "chapters": chapters,
        "_metadata": {
            "generated_from": "build_book.py",
            "structure_version": "2.0",
            "features": [
                "section subdivision",
                "default value optimization",
                "per-section statistics",
                "wmf_to_png_conversion",
            ],
        },
    }

    # Save index
    index_file = source_path / "index.json"
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print_success(
        f"Built index with {len(chapters)} chapters and {index['total_sections']} sections"
    )

    return True


# ============================================================================
# Main Execution
# ============================================================================


def main():
    """Main execution function."""

    print_header("Comprehensive Book Builder")
    print_info(f"Input document: {INPUT_DOCX}")
    print_info(f"Output directory: {JSON_DIR}")
    print_info(f"Viewer directory: {VIEWER_PUBLIC_DIR}")
    print()

    # Check prerequisites
    if not os.path.exists(INPUT_DOCX):
        print_error(f"Input file not found: {INPUT_DOCX}")
        print_info(f"Please ensure '{INPUT_DOCX}' exists in the current directory")
        return 1

    try:
        from docx import Document
    except ImportError:
        print_error("python-docx library not found")
        print_info("Install with: pip install python-docx")
        return 1

    # Step 1: Convert directly to JSON (no intermediate DOCX files)
    print_step(1, "Convert Word Document to JSON Format")
    if not convert_book_to_json():
        print_error("Failed to convert to JSON")
        return 1

    # Step 2: Optimize JSON files
    print_step(2, "Optimize JSON Files (Remove Default Values)")
    if not optimize_json_files():
        print_warning("Optimization failed, but continuing...")

    # Step 3: Convert WMF images
    print_step(3, "Convert WMF Images to PNG")
    if not convert_wmf_images():
        print_warning("Some WMF conversions failed, but continuing...")

    # Step 4: Copy to viewer
    print_step(4, "Copy Content to Chapter Viewer")
    if not copy_to_viewer():
        print_error("Failed to copy to viewer")
        return 1

    # Step 5: Build index
    print_step(5, "Build Index File")
    if not build_index():
        print_error("Failed to build index")
        return 1

    # Success summary
    print_header("Build Complete!")
    print_success("All steps completed successfully")
    print()
    print("Generated directories:")
    print(f"  📁 {JSON_DIR}/ - JSON content with images")
    print(f"  📁 {VIEWER_PUBLIC_DIR}/ - Ready for chapter-viewer")
    print()
    print("Next steps:")
    print("  1. Start the chapter-viewer development server")
    print("  2. Navigate to the app in your browser")
    print("  3. Browse the chapters and verify content")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
