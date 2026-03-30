# Makefile for docx2app - Document to JSON Converter
# ==================================================

# Variables
PYTHON := ./venv/bin/python3
PIP := ./venv/bin/pip
INPUT_DOCX := example/sample-book.docx
EXPORT_DIR := export
MARKDOWN_DIR := export_md

# Language selection (override with: make build L=fra)
L ?= eng

# Colors for output
GREEN := \033[0;32m
BLUE := \033[0;34m
YELLOW := \033[0;33m
NC := \033[0m # No Color

.PHONY: help all build images clean install-deps check-deps verify setup-libreoffice status stats rebuild rebuild-all

# Default target
help:
	@echo "$(BLUE)docx2app - Document to JSON Converter$(NC)"
	@echo "======================================="
	@echo ""
	@echo "Available targets:"
	@echo "  $(GREEN)make all$(NC)                - Build JSON/Markdown and process images"
	@echo "  $(GREEN)make build$(NC)              - Generate JSON and Markdown (no image files)"
	@echo "  $(GREEN)make images$(NC)             - Extract and process images from DOCX"
	@echo "  $(GREEN)make clean$(NC)              - Clean generated files"
	@echo "  $(GREEN)make rebuild-all$(NC)        - Clean and rebuild from scratch"
	@echo "  $(GREEN)make verify$(NC)             - Verify all images and content"
	@echo "  $(GREEN)make check-deps$(NC)         - Check if dependencies are installed"
	@echo "  $(GREEN)make install-deps$(NC)       - Install Python dependencies"
	@echo "  $(GREEN)make setup-libreoffice$(NC)  - Configure LibreOffice for ImageMagick (macOS)"
	@echo "  $(GREEN)make status$(NC)             - Show project status"
	@echo "  $(GREEN)make stats$(NC)              - Show content statistics"
	@echo ""
	@echo "Quick start:"
	@echo "  1. make install-deps       # Install dependencies"
	@echo "  2. make check-deps         # Verify everything is ready"
	@echo "  3. make all L=fra       # Build everything for French"
	@echo ""
	@echo "Language selection (default: eng):"
	@echo "  make build L=fra        # Build French"
	@echo "  make all L=kir          # Build Kirghiz"
	@echo "  Available: $(shell ls lang-store/)"
	@echo ""
	@echo "Output:"
	@echo "  - JSON content: $(EXPORT_DIR)/{lang}/{book_id}/"
	@echo "  - Pictures:     $(EXPORT_DIR)/pictures/{lang}/{book_id}/"
	@echo "  - Markdown:     $(MARKDOWN_DIR)/"
	@echo ""

# Check if all dependencies are installed
check-deps:
	@echo "$(BLUE)Checking dependencies...$(NC)"
	@[ -f "venv/bin/python3" ] || \
		(echo "$(YELLOW)⚠️  Virtual environment not found. Run: make install-deps$(NC)" && exit 1)
	@$(PYTHON) -c "import docx" 2>/dev/null || \
		(echo "$(YELLOW)⚠️  python-docx not installed. Run: make install-deps$(NC)" && exit 1)
	@command -v convert >/dev/null 2>&1 || command -v magick >/dev/null 2>&1 || \
		(echo "$(YELLOW)⚠️  ImageMagick not installed. Run: brew install imagemagick$(NC)" && exit 1)
	@command -v gs >/dev/null 2>&1 || \
		(echo "$(YELLOW)⚠️  Ghostscript not installed. Run: brew install ghostscript$(NC)" && exit 1)
	@echo "$(GREEN)✅ Core dependencies are installed$(NC)"
	@echo ""
	@echo "$(BLUE)Checking LibreOffice accessibility...$(NC)"
	@if [ -f "/Applications/LibreOffice.app/Contents/MacOS/soffice" ] && ! command -v libreoffice >/dev/null 2>&1; then \
		echo "$(YELLOW)⚠️  LibreOffice is installed but not accessible$(NC)"; \
		echo "$(YELLOW)   Run: make setup-libreoffice$(NC)"; \
	elif command -v libreoffice >/dev/null 2>&1; then \
		echo "$(GREEN)✅ LibreOffice is accessible$(NC)"; \
	else \
		echo "$(YELLOW)⚠️  LibreOffice not found (needed for WMF image conversion)$(NC)"; \
		echo "   Install: brew install --cask libreoffice"; \
	fi

# Install Python dependencies
install-deps:
	@echo "$(BLUE)Setting up Python virtual environment...$(NC)"
	@[ -d "venv" ] || python3 -m venv venv
	@echo "$(BLUE)Installing Python dependencies...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✅ Python dependencies installed$(NC)"
	@echo ""
	@echo "$(YELLOW)Note: Install system dependencies separately:$(NC)"
	@echo "  macOS:  brew install imagemagick ghostscript"
	@echo "          brew install --cask libreoffice"
	@echo "  Linux:  sudo apt-get install imagemagick ghostscript libreoffice"
	@echo ""
	@echo "$(YELLOW)For WMF image conversion on macOS, also run:$(NC)"
	@echo "  make setup-libreoffice"

# Generate JSON, Markdown, and image manifest (no image file I/O)
build:
	@echo "$(BLUE)Generating JSON and Markdown for $(L)...$(NC)"
	@echo ""
	LANG_CODE=$(L) $(PYTHON) build_book.py
	@echo ""
	@echo "$(GREEN)✅ Build complete!$(NC)"
	@echo "$(GREEN)   JSON:     $(EXPORT_DIR)/$(L)/{book_id}/$(NC)"
	@echo "$(GREEN)   Markdown: $(MARKDOWN_DIR)/$(NC)"

# Extract and process images from DOCX using the image manifest
images:
	@echo "$(BLUE)Processing images for $(L)...$(NC)"
	@echo ""
	LANG_CODE=$(L) $(PYTHON) process_images.py
	@echo ""
	@echo "$(GREEN)✅ Image processing complete!$(NC)"
	@echo "$(GREEN)   Pictures: $(EXPORT_DIR)/pictures/$(NC)"

# Build everything (JSON + Markdown + images)
all: build images

# Clean generated files
clean:
	@echo "$(BLUE)Cleaning generated files...$(NC)"
	rm -rf $(EXPORT_DIR)
	rm -rf $(MARKDOWN_DIR)
	rm -rf markdown_chapters
	rm -rf chapters
	@find . -name "*.wmf.backup" -delete 2>/dev/null || true
	@echo "$(GREEN)✅ Cleaned generated files$(NC)"

# Verify all images and content integrity
verify:
	@echo "$(BLUE)Verifying content integrity for $(L)...$(NC)"
	@[ -d "$(EXPORT_DIR)" ] || \
		(echo "$(YELLOW)⚠️  Content not found. Run 'make build' first$(NC)" && exit 1)
	LANG_CODE=$(L) $(PYTHON) verify_images.py
	@echo ""
	@echo "$(GREEN)✅ Verification complete$(NC)"

# Show statistics about the book content
stats:
	@echo "$(BLUE)Book Content Statistics$(NC)"
	@echo "======================="
	@if [ -d "$(EXPORT_DIR)" ]; then \
		echo "Languages:   $$(ls -d $(EXPORT_DIR)/*/ 2>/dev/null | grep -v pictures | wc -l | tr -d ' ')"; \
		echo "JSON files:  $$(find $(EXPORT_DIR) -name '*.json' 2>/dev/null | wc -l | tr -d ' ')"; \
		echo "Images:      $$(find $(EXPORT_DIR)/pictures -name '*.png' -o -name '*.jpg' 2>/dev/null | wc -l | tr -d ' ')"; \
		echo "Manifests:   $$(find $(EXPORT_DIR) -name '_book.toml' 2>/dev/null | wc -l | tr -d ' ')"; \
	else \
		echo "Not built yet. Run 'make build' first."; \
	fi

# Quick rebuild (clean and build)
rebuild: clean build

# Full rebuild (clean everything and build)
rebuild-all: clean all

# Setup LibreOffice for ImageMagick (macOS only)
setup-libreoffice:
	@echo "$(BLUE)Setting up LibreOffice for ImageMagick...$(NC)"
	@./setup_libreoffice.sh

# Show current status
status:
	@echo "$(BLUE)Project Status$(NC)"
	@echo "=============="
	@echo ""
	@echo "Input file:"
	@[ -f "$(INPUT_DOCX)" ] && \
		echo "  ✓ $(INPUT_DOCX)" || \
		echo "  ✗ $(INPUT_DOCX) (missing)"
	@echo ""
	@echo "Configuration:"
	@[ -f "book_config.toml" ] && \
		echo "  ✓ book_config.toml" || \
		echo "  ✗ book_config.toml (using defaults)"
	@echo ""
	@echo "Generated content:"
	@if [ -d "$(EXPORT_DIR)" ]; then \
		L_COUNT=$$(ls -d $(EXPORT_DIR)/*/ 2>/dev/null | grep -v pictures | wc -l | tr -d ' '); \
		echo "  ✓ $(EXPORT_DIR)/ ($$L_COUNT language(s))"; \
	else \
		echo "  ✗ $(EXPORT_DIR)/ (not created)"; \
	fi
	@if [ -d "$(EXPORT_DIR)/pictures" ]; then \
		echo "  ✓ $(EXPORT_DIR)/pictures/"; \
	else \
		echo "  ✗ $(EXPORT_DIR)/pictures/ (not created)"; \
	fi
	@if [ -d "$(MARKDOWN_DIR)" ]; then \
		echo "  ✓ $(MARKDOWN_DIR)/"; \
	else \
		echo "  ✗ $(MARKDOWN_DIR)/ (not created)"; \
	fi
	@echo ""
	@echo "Dependencies:"
	@[ -f "venv/bin/python3" ] && echo "  ✓ Python venv" || echo "  ✗ Python venv"
	@[ -f "venv/bin/python3" ] && $(PYTHON) -c "import docx" 2>/dev/null && echo "  ✓ python-docx" || echo "  ✗ python-docx"
	@(command -v convert >/dev/null 2>&1 || command -v magick >/dev/null 2>&1) && echo "  ✓ ImageMagick" || echo "  ✗ ImageMagick"
	@command -v gs >/dev/null 2>&1 && echo "  ✓ Ghostscript" || echo "  ✗ Ghostscript"
	@command -v libreoffice >/dev/null 2>&1 && echo "  ✓ LibreOffice" || echo "  ⚠ LibreOffice (optional, for WMF)"
	@echo ""
