# Chapter Viewer - Standalone Book Reader

A modern, mobile-friendly React web application for viewing and navigating book chapters. Originally created for the Animal Health Handbook, this viewer is **fully self-contained** and can be used as a standalone project for any book or documentation.

## 📍 Book Data Location

**All book content is stored in `book_content_json/` within this directory.**

This makes the entire `chapter-viewer` folder self-contained and portable. The `public/book_content_json/` is a symlink to `../book_content_json/` for development server access.

```
chapter-viewer/
├── book_content_json/          ← Your book data lives here!
│   ├── index.json
│   ├── toc_structure.json
│   └── chapter_XX/
│       ├── chapter.json
│       ├── section_XX.json
│       └── pictures/
├── public/
│   └── book_content_json/      ← Symlink to ../book_content_json/
└── src/
```

## 🎯 Standalone Usage

This `chapter-viewer` directory is a **complete, independent project** that can be:

- ✅ Extracted and used separately from the parent project
- ✅ Deployed as its own web application
- ✅ Used to display any book content (just provide your own JSON data)
- ✅ Shared, forked, or integrated into other projects
- ✅ Copied to a new location and it just works!

### Using as a Standalone Viewer

1. **Copy this entire directory** to use it independently:
   ```bash
   cp -r chapter-viewer my-book-viewer
   cd my-book-viewer
   ```

2. **Your book content is already included!**
   - All data is in `book_content_json/` 
   - Images are in `book_content_json/chapter_XX/pictures/`
   - The symlink in `public/` will work automatically

3. **Install and run**:
   ```bash
   pnpm install
   pnpm dev
   ```

That's it! You now have a fully functional, self-contained book viewer.

### Adding Your Own Book Content

To use this viewer with your own book:

1. Replace the content in `book_content_json/` with your book's JSON data
2. Follow the structure described in **Data Format** section below
3. Place images in `book_content_json/chapter_XX/pictures/`
4. The `public/book_content_json/` symlink will automatically point to your new content

### Data Format Required

The viewer expects a `book_content_json/` directory with:
- `index.json` - Chapter list and navigation
- `toc_structure.json` - Table of contents (optional)
- `chapter_XX/` folders containing:
  - `chapter.json` - Chapter metadata
  - `section_XX.json` - Section content
  - `pictures/` - Chapter images

See the **Data Format** section below for detailed structure.

## Features

- 📱 **Mobile-First Design** - Optimized for smartphones and tablets
- 📚 **Easy Navigation** - Side drawer navigation with chapter listing
- 📄 **Document-Style Rendering** - Faithful representation of the original Word documents
- 🖼️ **Image Support** - Embedded images with captions
- 📊 **Table Rendering** - Properly formatted tables with expanded row support
- 🔗 **Footnotes** - Interactive footnote references
- 🎨 **Clean UI** - Professional, readable interface
- 📱 **Responsive** - Works seamlessly on desktop, tablet, and mobile devices

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- pnpm package manager

### Installation

1. Install dependencies:
```bash
pnpm install
```

2. Start the development server:
```bash
pnpm dev
```

The app will open automatically at `http://localhost:3000`

### Building for Production

```bash
pnpm build
```

The production-ready files will be in the `dist` directory.

### Preview Production Build

```bash
pnpm preview
```

## Project Structure

```
chapter-viewer/
├── public/
│   └── book_content_json/          # Chapter data and images
│       ├── index.json              # Navigation index
│       ├── toc_structure.json      # Table of contents
│       ├── chapter_01/
│       │   ├── chapter.json        # Chapter metadata
│       │   ├── section_01.json     # Section 1.1 content
│       │   ├── section_02.json     # Section 1.2 content
│       │   └── pictures/           # Chapter images
│       ├── chapter_02/
│       │   ├── chapter.json
│       │   ├── section_01.json
│       │   └── ...
│       └── ...
├── src/
│   ├── components/
│   │   ├── Sidebar.jsx         # Navigation sidebar
│   │   └── Sidebar.css
│   ├── pages/
│   │   ├── Home.jsx            # Landing page with chapter grid
│   │   ├── Home.css
│   │   ├── ChapterView.jsx     # Chapter content viewer
│   │   └── ChapterView.css
│   ├── App.jsx                 # Main app component with routing
│   ├── App.css
│   ├── main.jsx                # React entry point
│   └── index.css               # Global styles
└── index.html
```

## Usage

### Navigation

- **Mobile**: Tap the menu button (☰) in the top-left to open the navigation drawer
- **Desktop**: The sidebar is always visible on the left side
- Click on any chapter to view its content
- Click "Home" to return to the chapter grid view

### Chapter Content

- Scroll through the chapter content as a continuous page
- Click on footnote references to jump to the footnotes section
- Tables are automatically formatted and scrollable on mobile
- Images are displayed inline with captions when available

### Mobile Features

- Touch-friendly navigation
- Swipe-dismissable sidebar
- Optimized text size for reading on small screens
- Horizontal table scrolling on narrow viewports

## Technologies Used

- **React 19** - UI framework
- **React Router v7** - Client-side routing
- **Vite** - Build tool and dev server
- **CSS3** - Styling with CSS variables and Grid/Flexbox
- **pnpm** - Fast, disk space efficient package manager

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Data Format

The app reads chapter data from JSON files generated by the `build_book.py` script. Each chapter contains:

- Paragraphs with rich text formatting (bold, italic, underline)
- Tables with cell formatting and merged cells
- Images with metadata
- Footnotes with references
- Chapter statistics

## License

This project is part of the Animal Health Handbook documentation system.

## Development

### Available Scripts

- `pnpm dev` - Start development server
- `pnpm build` - Build for production
- `pnpm preview` - Preview production build
- `pnpm lint` - Run ESLint

### Adding New Features

1. Components go in `src/components/`
2. Pages go in `src/pages/`
3. Keep styles co-located with components
4. Use CSS variables defined in `App.css` for consistency

## Troubleshooting

### Images not loading
- Ensure the `book_content_json` folder is in the `public/` directory
- Check that image paths match the folder structure

### Chapter not found
- Verify the chapter JSON file exists in `public/book_content_json/chapter_XX/`
- Check that the chapter number is formatted correctly (e.g., `01`, `02`)

### Sidebar not showing on mobile
- Click the menu button (☰) in the top-left corner
- Check browser console for JavaScript errors

## Contributing

When making changes:
1. Test on mobile devices or use browser dev tools
2. Ensure responsive design works at all breakpoints
3. Check print styles work correctly
4. Verify accessibility (keyboard navigation, screen readers)