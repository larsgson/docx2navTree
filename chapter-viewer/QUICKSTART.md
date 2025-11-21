# Quick Start Guide

## Running the Application

### Start Development Server

```bash
cd chapter-viewer
pnpm dev
```

The application will automatically open in your browser at `http://localhost:3000`

### Using on Mobile

1. Start the dev server as above
2. Find your computer's IP address:
   - **Linux/Mac**: `ifconfig` or `ip addr show`
   - **Windows**: `ipconfig`
3. On your mobile device, open the browser and navigate to:
   ```
   http://YOUR_IP_ADDRESS:3000
   ```
   Example: `http://192.168.1.100:3000`

### Building for Production

```bash
pnpm build
pnpm preview
```

## Features Overview

### Mobile Navigation
- Tap the **☰** button (top-left) to open the navigation menu
- Tap anywhere outside the menu to close it
- Scroll through the list of chapters
- Tap a chapter to view its content

### Desktop Navigation
- Navigation sidebar is always visible on the left
- Click any chapter to view its content
- Click "Home" to return to the chapter overview

### Reading Chapters
- Chapters are displayed as a single scrollable page
- Images appear inline with the text
- Tables are properly formatted and scrollable on mobile
- Tap footnote numbers to jump to footnote details
- All formatting (bold, italic, underline) is preserved

### Chapter Features
- **Paragraphs**: Full text with formatting
- **Images**: Embedded with captions
- **Tables**: Responsive tables with headers
- **Footnotes**: Interactive references
- **Statistics**: See paragraph, table, and image counts

## Keyboard Shortcuts

- **Escape**: Close mobile sidebar
- **Tab**: Navigate through interactive elements
- **Enter**: Activate links and buttons

## Browser Compatibility

✅ Chrome/Edge (Recommended)  
✅ Firefox  
✅ Safari (Desktop & iOS)  
✅ Chrome Mobile (Android)  

## Troubleshooting

### Port Already in Use
If port 3000 is busy:
```bash
pnpm dev -- --port 3001
```

### Changes Not Appearing
- Hard refresh: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
- Clear browser cache
- Restart dev server

### Images Not Loading
- Check that `public/book_content_json` folder exists
- Verify image files are in the correct chapter's `pictures` folder
- Check browser console for 404 errors

### Mobile Menu Not Working
- Clear browser cache
- Try in incognito/private mode
- Check browser console for JavaScript errors

## Tips for Best Experience

### Mobile Users
- Use portrait orientation for better text readability
- Rotate to landscape for wide tables
- Pinch to zoom on images for detail
- Use the "Home" button to quickly access the chapter list

### Desktop Users
- Bookmark frequently accessed chapters
- Use browser search (`Ctrl+F` / `Cmd+F`) to find content
- Print chapters directly from the browser
- Adjust browser zoom for comfortable reading

### Printing
- Use browser's print function (`Ctrl+P` / `Cmd+P`)
- Sidebar is automatically hidden when printing
- Tables and images are optimized for print

## Performance Tips

- First load may take a moment to fetch chapter data
- Subsequent chapter loads are faster
- Images load on-demand as you scroll
- Each chapter is loaded independently

## Data Structure

The app reads from `public/book_content_json/`:
```
book_content_json/
├── index.json              # Chapter list and navigation
├── toc_structure.json      # Table of contents
├── chapter_01/
│   ├── chapter.json        # Chapter metadata
│   ├── section_01.json     # Section 1.1 content
│   ├── section_02.json     # Section 1.2 content
│   └── pictures/           # Chapter images
├── chapter_02/
│   ├── chapter.json
│   ├── section_01.json
│   └── ...
└── ...
```

## Support

For issues or questions:
1. Check the main README.md
2. Review browser console for errors
3. Verify chapter JSON files are properly formatted

## Next Steps

- Explore all chapters
- Test on different devices
- Check print preview
- Bookmark your favorites

Enjoy reading the Animal Health Handbook! 📚