# Makefile for Animal Health Handbook Book Builder
# ==================================================
# This Makefile provides convenient commands for building and managing
# the book content for the chapter-viewer React application.

# Variables
PYTHON := ./venv/bin/python3
PIP := ./venv/bin/pip
INPUT_DOCX := English\ HAH\ Word\ Apr\ 6\ 2024.docx
JSON_DIR := chapter-viewer/book_content_json
VIEWER_DIR := chapter-viewer
VIEWER_PUBLIC := $(VIEWER_DIR)/public/book_content_json

# Colors for output
GREEN := \033[0;32m
BLUE := \033[0;34m
YELLOW := \033[0;33m
NC := \033[0m # No Color

.PHONY: help build clean install-deps check-deps viewer dev clean-all verify setup-libreoffice split-chapters split-markdown

# Default target
help:
	@echo "$(BLUE)Animal Health Handbook - Build System$(NC)"
	@echo "======================================"
	@echo ""
	@echo "Available targets:"
	@echo "  $(GREEN)make build$(NC)              - Build complete book content (all steps)"
	@echo "  $(GREEN)make clean$(NC)              - Clean generated files"
	@echo "  $(GREEN)make clean-all$(NC)          - Clean everything (same as clean)"
	@echo "  $(GREEN)make viewer$(NC)             - Start chapter-viewer dev server"
	@echo "  $(GREEN)make dev$(NC)                - Build and start viewer"
	@echo "  $(GREEN)make verify$(NC)             - Verify all images and content"
	@echo "  $(GREEN)make check-deps$(NC)         - Check if dependencies are installed"
	@echo "  $(GREEN)make install-deps$(NC)       - Install Python dependencies"
	@echo "  $(GREEN)make setup-libreoffice$(NC)  - Configure LibreOffice for ImageMagick (macOS)"
	@echo ""
	@echo "Reference scripts:"
	@echo "  $(GREEN)make split-chapters$(NC)     - Split book into DOCX chapter files"
	@echo "  $(GREEN)make split-markdown$(NC)     - Convert chapters to Markdown format"
	@echo ""
	@echo "Quick start:"
	@echo "  1. make check-deps         # Check if everything is installed"
	@echo "  2. make setup-libreoffice  # Configure LibreOffice (if needed for WMF images)"
	@echo "  3. make build              # Build the book content"
	@echo "  4. make viewer             # Start the web viewer"
	@echo ""

# Check if all dependencies are installed
check-deps:
	@echo "$(BLUE)Checking dependencies...$(NC)"
	@[ -f "venv/bin/python3" ] || \
		(echo "$(YELLOW)⚠️  Virtual environment not found. Run: make install-deps$(NC)" && exit 1)
	@$(PYTHON) -c "import docx" 2>/dev/null || \
		(echo "$(YELLOW)⚠️  python-docx not installed. Run: make install-deps$(NC)" && exit 1)
	@command -v convert >/dev/null 2>&1 || \
		(echo "$(YELLOW)⚠️  ImageMagick not installed. Run: brew install imagemagick$(NC)" && exit 1)
	@command -v node >/dev/null 2>&1 || \
		(echo "$(YELLOW)⚠️  Node.js not found$(NC)" && exit 1)
	@[ -d "$(VIEWER_DIR)/node_modules" ] || \
		(echo "$(YELLOW)⚠️  Viewer dependencies not installed. Run: cd $(VIEWER_DIR) && npm install$(NC)" && exit 1)
	@echo "$(GREEN)✅ All dependencies are installed$(NC)"
	@echo ""
	@echo "$(BLUE)Checking LibreOffice accessibility...$(NC)"
	@if [ -f "/Applications/LibreOffice.app/Contents/MacOS/soffice" ] && ! command -v libreoffice >/dev/null 2>&1; then \
		echo "$(YELLOW)⚠️  LibreOffice is installed but not accessible to ImageMagick$(NC)"; \
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
	@echo "$(BLUE)Installing Node dependencies...$(NC)"
	cd $(VIEWER_DIR) && npm install
	@echo "$(GREEN)✅ Node dependencies installed$(NC)"
	@echo ""
	@echo "$(YELLOW)Note: Install ImageMagick and Ghostscript separately:$(NC)"
	@echo "  macOS:  brew install imagemagick ghostscript"
	@echo "  Linux:  sudo apt-get install imagemagick ghostscript"
	@echo ""
	@echo "$(YELLOW)For WMF image conversion support (all 3 required):$(NC)"
	@echo "  1. Install ImageMagick: brew install imagemagick"
	@echo "  2. Install Ghostscript: brew install ghostscript"
	@echo "  3. Install LibreOffice: brew install --cask libreoffice"
	@echo "  4. Configure it: make setup-libreoffice"

# Build everything from the Word document
build: check-deps
	@echo "$(BLUE)Building complete book content...$(NC)"
	@echo "This will:"
	@echo "  1. Convert Word document directly to JSON with images"
	@echo "  2. Optimize JSON files (remove common defaults)"
	@echo "  3. Convert WMF images to PNG format"
	@echo "  4. Copy content to chapter-viewer"
	@echo "  5. Build index file"
	@echo ""
	@test -f $(INPUT_DOCX) || (echo "$(YELLOW)⚠️  Input file not found: $(INPUT_DOCX)$(NC)" && exit 1)
	$(PYTHON) build_book.py
	@echo ""
	@echo "$(GREEN)✅ Build complete!$(NC)"

# Clean generated files
clean:
	@echo "$(BLUE)Cleaning generated files...$(NC)"
	rm -rf $(JSON_DIR)
	rm -rf $(VIEWER_PUBLIC)
	rm -rf markdown_chapters
	rm -rf chapters
	@find . -name "*.wmf.backup" -delete
	@echo "$(GREEN)✅ Cleaned generated files$(NC)"

# Clean everything (same as clean now)
clean-all: clean

# Start the chapter-viewer development server
viewer:
	@echo "$(BLUE)Starting chapter-viewer...$(NC)"
	@[ -d "$(VIEWER_PUBLIC)" ] || \
		(echo "$(YELLOW)⚠️  Content not found. Run 'make build' first$(NC)" && exit 1)
	cd $(VIEWER_DIR) && npm run dev

# Build and start viewer in one command
dev: build viewer

# Verify all images and content integrity
verify:
	@echo "$(BLUE)Verifying content integrity...$(NC)"
	@[ -d "$(VIEWER_PUBLIC)" ] || \
		(echo "$(YELLOW)⚠️  Content not found. Run 'make build' first$(NC)" && exit 1)
	$(PYTHON) verify_images.py
	@echo ""
	@echo "$(GREEN)✅ Verification complete$(NC)"

# Show statistics about the book content
stats:
	@echo "$(BLUE)Book Content Statistics$(NC)"
	@echo "======================="
	@[ -d "$(JSON_DIR)" ] && \
		echo "Chapters:    $$(ls -d $(JSON_DIR)/chapter_* 2>/dev/null | wc -l)" || \
		echo "Chapters:    0 (not built)"
	@[ -d "$(JSON_DIR)" ] && \
		echo "JSON files:  $$(find $(JSON_DIR) -name "*.json" 2>/dev/null | wc -l)" || \
		echo "JSON files:  0"
	@[ -d "$(JSON_DIR)" ] && \
		echo "Images:      $$(find $(JSON_DIR) -name "*.png" -o -name "*.jpg" 2>/dev/null | wc -l)" || \
		echo "Images:      0"
	@[ -f "$(JSON_DIR)/index.json" ] && \
		echo "Index:       ✓ Present" || \
		echo "Index:       ✗ Missing"

# Quick rebuild (clean and build)
rebuild: clean build

# Full rebuild (clean everything and build)
rebuild-all: clean-all build

# List all chapters
list-chapters:
	@echo "$(BLUE)Chapters in JSON directory:$(NC)"
	@[ -d "$(JSON_DIR)" ] && \
		ls -1 $(JSON_DIR) | grep "chapter_" || \
		echo "No chapters found. Run 'make build' first."

# Deploy to viewer (just copy step)
deploy-viewer:
	@echo "$(BLUE)Deploying content to chapter-viewer...$(NC)"
	@[ -d "$(JSON_DIR)" ] || \
		(echo "$(YELLOW)⚠️  Source content not found. Run 'make build' first$(NC)" && exit 1)
	rm -rf $(VIEWER_PUBLIC)
	cp -r $(JSON_DIR) $(VIEWER_PUBLIC)
	@echo "$(GREEN)✅ Content deployed to viewer$(NC)"

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
	@echo "Generated content:"
	@[ -d "$(JSON_DIR)" ] && \
		echo "  ✓ $(JSON_DIR)/ ($$(ls -d $(JSON_DIR)/chapter_* 2>/dev/null | wc -l) chapters)" || \
		echo "  ✗ $(JSON_DIR)/ (not created)"
	@[ -d "$(VIEWER_PUBLIC)" ] && \
		echo "  ✓ $(VIEWER_PUBLIC)/ (ready)" || \
		echo "  ✗ $(VIEWER_PUBLIC)/ (not deployed)"
	@echo ""
	@echo "Dependencies:"
	@[ -f "venv/bin/python3" ] && echo "  ✓ Python venv" || echo "  ✗ Python venv"
	@[ -f "venv/bin/python3" ] && $(PYTHON) -c "import docx" 2>/dev/null && echo "  ✓ python-docx" || echo "  ✗ python-docx"
	@command -v convert >/dev/null 2>&1 && echo "  ✓ ImageMagick" || echo "  ✗ ImageMagick"
	@command -v node >/dev/null 2>&1 && echo "  ✓ Node.js" || echo "  ✗ Node.js"
	@[ -d "$(VIEWER_DIR)/node_modules" ] && echo "  ✓ Viewer dependencies" || echo "  ✗ Viewer dependencies"
	@echo ""

# Reference script: Split book into DOCX chapters
split-chapters:
	@echo "$(BLUE)Splitting book into DOCX chapter files...$(NC)"
	@test -f $(INPUT_DOCX) || \
		(echo "$(YELLOW)⚠️  Input file not found: $(INPUT_DOCX)$(NC)" && exit 1)
	$(PYTHON) split_chapters.py
	@echo "$(GREEN)✅ Chapter files created in chapters/ directory$(NC)"

# Reference script: Convert chapters to Markdown
split-markdown:
	@echo "$(BLUE)Converting book to Markdown format...$(NC)"
	@test -f $(INPUT_DOCX) || \
		(echo "$(YELLOW)⚠️  Input file not found: $(INPUT_DOCX)$(NC)" && exit 1)
	$(PYTHON) split_to_md_chapters.py
	@echo "$(GREEN)✅ Markdown files created in markdown_chapters/ directory$(NC)"
	@echo "$(CYAN)ℹ️  Open markdown_chapters/README.md to start browsing$(NC)"
