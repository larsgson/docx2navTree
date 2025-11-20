#!/usr/bin/env python3
"""
Verify that all image references in JSON files have corresponding image files.
This script checks the integrity of the book content structure.
"""

import json
import os
from collections import defaultdict
from pathlib import Path


def verify_images():
    """Check all JSON files for image references and verify files exist."""

    base_path = Path("chapter-viewer/public/book_content_json")

    if not base_path.exists():
        print(f"❌ Base path not found: {base_path}")
        return False

    issues = []
    stats = defaultdict(int)

    # Iterate through all chapter directories
    for chapter_dir in sorted(base_path.glob("chapter_*")):
        if not chapter_dir.is_dir():
            continue

        chapter_num = chapter_dir.name.split("_")[1]
        pictures_dir = chapter_dir / "pictures"

        # Get all section JSON files
        for json_file in sorted(chapter_dir.glob("section_*.json")):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Check all content items
                if "content" in data:
                    for item in data["content"]:
                        if item.get("type") == "paragraph" and "images" in item:
                            for img in item["images"]:
                                stats["total_images"] += 1

                                filename = img.get("filename")
                                path = img.get("path")

                                if not filename:
                                    issues.append(
                                        f"⚠️  {json_file.name}: Image missing filename: {img}"
                                    )
                                    stats["missing_filename"] += 1
                                    continue

                                # Check if file exists
                                if path:
                                    # Use path from JSON
                                    image_file = chapter_dir / path
                                else:
                                    # Fallback to pictures directory
                                    image_file = pictures_dir / filename

                                if not image_file.exists():
                                    issues.append(
                                        f"❌ {chapter_dir.name}/{json_file.name}: "
                                        f"Missing image file: {image_file.relative_to(base_path)}"
                                    )
                                    stats["missing_files"] += 1
                                else:
                                    stats["valid_images"] += 1

            except json.JSONDecodeError as e:
                issues.append(f"❌ Error parsing {json_file}: {e}")
                stats["json_errors"] += 1
            except Exception as e:
                issues.append(f"❌ Error processing {json_file}: {e}")
                stats["other_errors"] += 1

    # Print results
    print("\n" + "=" * 70)
    print("Image Verification Report")
    print("=" * 70)

    print(f"\n📊 Statistics:")
    print(f"   Total images referenced:  {stats['total_images']}")
    print(f"   Valid images found:       {stats['valid_images']}")
    print(f"   Missing image files:      {stats['missing_files']}")
    print(f"   Missing filename field:   {stats['missing_filename']}")
    print(f"   JSON parsing errors:      {stats['json_errors']}")
    print(f"   Other errors:             {stats['other_errors']}")

    if issues:
        print(f"\n⚠️  Found {len(issues)} issue(s):\n")
        for issue in issues[:20]:  # Show first 20 issues
            print(f"   {issue}")

        if len(issues) > 20:
            print(f"\n   ... and {len(issues) - 20} more issues")

        print("\n❌ Verification FAILED")
        return False
    else:
        print("\n✅ All image references verified successfully!")
        return True


def list_orphaned_images():
    """Find image files that are not referenced in any JSON."""

    base_path = Path("chapter-viewer/public/book_content_json")

    if not base_path.exists():
        return

    print("\n" + "=" * 70)
    print("Orphaned Images Report")
    print("=" * 70)

    total_orphaned = 0

    for chapter_dir in sorted(base_path.glob("chapter_*")):
        if not chapter_dir.is_dir():
            continue

        pictures_dir = chapter_dir / "pictures"
        if not pictures_dir.exists():
            continue

        # Get all referenced images in this chapter
        referenced = set()
        for json_file in chapter_dir.glob("section_*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if "content" in data:
                    for item in data["content"]:
                        if item.get("type") == "paragraph" and "images" in item:
                            for img in item["images"]:
                                referenced.add(img.get("filename"))
            except:
                continue

        # Check for orphaned files
        orphaned = []
        for img_file in sorted(pictures_dir.glob("*.png")):
            if img_file.name not in referenced:
                orphaned.append(img_file.name)

        if orphaned:
            print(f"\n📁 {chapter_dir.name}:")
            for img in orphaned:
                print(f"   🔸 {img}")
            total_orphaned += len(orphaned)

    if total_orphaned == 0:
        print("\n✅ No orphaned images found!")
    else:
        print(f"\n📊 Total orphaned images: {total_orphaned}")
        print("   (These images exist but are not referenced in any JSON file)")


if __name__ == "__main__":
    print("\n🔍 Starting image verification...\n")

    success = verify_images()
    list_orphaned_images()

    print("\n" + "=" * 70 + "\n")

    exit(0 if success else 1)
