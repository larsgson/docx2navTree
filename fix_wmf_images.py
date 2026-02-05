#!/usr/bin/env python3
"""
Fix WMF images that were saved with PNG extensions.

This script:
1. Scans for PNG files that are actually WMF format
2. Converts them to proper PNG using ImageMagick
3. Backs up the original WMF files
"""

import os
import shutil
import subprocess
from pathlib import Path


def postprocess_image(image_path, max_size=1200, border=10, white_threshold=240):
    """Auto-crop whitespace and limit resolution of an image."""
    try:
        from PIL import Image, ImageChops
    except ImportError:
        return

    try:
        img = Image.open(image_path)
    except Exception:
        return

    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")

    bg = Image.new(img.mode, img.size, tuple([white_threshold] * len(img.getbands())))
    diff = ImageChops.subtract(bg, img)
    bbox = diff.getbbox()
    if bbox:
        left, top, right, bottom = bbox
        left = max(0, left - border)
        top = max(0, top - border)
        right = min(img.width, right + border)
        bottom = min(img.height, bottom + border)
        img = img.crop((left, top, right, bottom))

    if max_size > 0:
        longest = max(img.width, img.height)
        if longest > max_size:
            scale = max_size / longest
            new_w = int(img.width * scale)
            new_h = int(img.height * scale)
            img = img.resize((new_w, new_h), Image.LANCZOS)

    img.save(image_path)


def is_wmf_image(image_path):
    """Check if image file is WMF format by checking magic bytes."""
    try:
        with open(image_path, "rb") as f:
            magic = f.read(4)
            return magic == b"\xd7\xcd\xc6\x9a" or magic == b"\x01\x00\x09\x00"
    except Exception:
        return False


def convert_wmf_to_png(wmf_path, output_path):
    """Convert WMF to PNG using LibreOffice + ImageMagick chain."""
    import tempfile

    # Try LibreOffice first (best for WMF)
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if soffice:
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                # Convert WMF to PDF using LibreOffice
                pdf_path = os.path.join(tmpdir, "output.pdf")
                result = subprocess.run(
                    [
                        soffice,
                        "--headless",
                        "--convert-to",
                        "pdf",
                        "--outdir",
                        tmpdir,
                        wmf_path,
                    ],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                # Find the generated PDF (LibreOffice might name it differently)
                pdf_files = list(Path(tmpdir).glob("*.pdf"))
                if pdf_files:
                    pdf_path = str(pdf_files[0])

                    # Convert PDF to PNG using ImageMagick
                    # Use -trim to extract just the vector content (not the full page)
                    magick_cmd = None
                    if shutil.which("magick"):
                        magick_cmd = [
                            "magick",
                            "-density",
                            "150",
                            pdf_path,
                            "-flatten",
                            "-trim",
                            "+repage",
                            "png:" + output_path,
                        ]
                    elif shutil.which("convert"):
                        magick_cmd = [
                            "convert",
                            "-density",
                            "150",
                            pdf_path,
                            "-flatten",
                            "-trim",
                            "+repage",
                            "png:" + output_path,
                        ]

                    if magick_cmd:
                        result = subprocess.run(
                            magick_cmd,
                            capture_output=True,
                            text=True,
                            timeout=30,
                        )

                        if result.returncode == 0 and os.path.exists(output_path):
                            # Verify it's actually a PNG
                            with open(output_path, "rb") as f:
                                header = f.read(8)
                                if header[:4] == b"\x89PNG":
                                    return True
                                else:
                                    print(f"    ⚠️  Output is not PNG format")
                                    return False

        except subprocess.TimeoutExpired:
            print(f"    ⚠️  Conversion timeout")
            return False
        except Exception as e:
            print(f"    ⚠️  LibreOffice conversion error: {e}")

    # Fallback: Try ImageMagick directly (needs WMF delegates)
    try:
        magick_cmd = None
        if shutil.which("magick"):
            magick_cmd = ["magick", wmf_path, "png:" + output_path]
        elif shutil.which("convert"):
            magick_cmd = ["convert", wmf_path, "png:" + output_path]
        else:
            print("    ⚠️  No conversion tools found")
            return False

        result = subprocess.run(
            magick_cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0 and os.path.exists(output_path):
            # Verify it's actually a PNG
            with open(output_path, "rb") as f:
                header = f.read(8)
                if header[:4] == b"\x89PNG":
                    return True
                else:
                    print(f"    ⚠️  Output is not PNG format")
                    return False
        else:
            print(f"    ⚠️  Conversion failed: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"    ⚠️  Conversion timeout")
        return False
    except Exception as e:
        print(f"    ⚠️  Conversion error: {e}")
        return False


def fix_wmf_images(base_dir="export/pictures"):
    """Find and convert all WMF files with PNG extensions."""
    print("=" * 80)
    print("FIX WMF IMAGES")
    print("=" * 80)
    print()

    base_path = Path(base_dir)
    if not base_path.exists():
        print(f"❌ Pictures directory not found: {base_dir}")
        print("   Run 'make build' first to generate content.")
        return

    # Check if conversion tools are available
    has_soffice = shutil.which("soffice") or shutil.which("libreoffice")
    has_magick = shutil.which("magick") or shutil.which("convert")

    if not has_soffice and not has_magick:
        print("❌ No conversion tools found. Please install:")
        print("   brew install libreoffice imagemagick")
        return

    if not has_soffice:
        print("⚠️  LibreOffice not found - using ImageMagick only (may fail)")
    if not has_magick:
        print("⚠️  ImageMagick not found - using LibreOffice only")

    # Find all PNG files
    png_files = list(base_path.rglob("*.png"))
    print(f"Scanning {len(png_files)} PNG files...")
    print()

    wmf_count = 0
    converted_count = 0
    failed_count = 0

    for png_path in png_files:
        if is_wmf_image(png_path):
            wmf_count += 1
            print(f"Found WMF: {png_path.relative_to(base_path)}")

            # Create temporary WMF file
            wmf_temp = str(png_path) + ".wmf.tmp"
            png_temp = str(png_path) + ".png.tmp"

            try:
                # Copy to temp WMF file
                shutil.copy2(png_path, wmf_temp)

                # Convert to PNG
                if convert_wmf_to_png(wmf_temp, png_temp):
                    # Backup original WMF
                    backup_path = str(png_path) + ".wmf.backup"
                    shutil.move(str(png_path), backup_path)

                    # Move converted PNG to final location
                    shutil.move(png_temp, str(png_path))

                    # Post-process: auto-crop whitespace and limit resolution
                    postprocess_image(str(png_path))

                    # Clean up temp WMF
                    os.remove(wmf_temp)

                    print(f"  ✓ Converted and post-processed successfully")
                    print(f"  ✓ Original backed up to: {Path(backup_path).name}")
                    converted_count += 1
                else:
                    # Clean up temp files
                    if os.path.exists(wmf_temp):
                        os.remove(wmf_temp)
                    if os.path.exists(png_temp):
                        os.remove(png_temp)
                    failed_count += 1

            except Exception as e:
                print(f"  ❌ Error: {e}")
                # Clean up temp files
                if os.path.exists(wmf_temp):
                    os.remove(wmf_temp)
                if os.path.exists(png_temp):
                    os.remove(png_temp)
                failed_count += 1

            print()

    print("=" * 80)
    print(f"Found {wmf_count} WMF files with PNG extensions")
    print(f"  ✓ Converted: {converted_count}")
    if failed_count > 0:
        print(f"  ⚠️  Failed: {failed_count}")
    print("=" * 80)


if __name__ == "__main__":
    fix_wmf_images()
