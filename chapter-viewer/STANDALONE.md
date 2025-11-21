# Using Chapter Viewer as a Standalone Application

This directory is a **fully self-contained, portable book viewer** that works independently of the parent project.

## 🎯 What Makes It Standalone?

✅ **All book data is stored within this directory**
- Book content: `book_content_json/`
- Images: `book_content_json/chapter_XX/pictures/`
- No external dependencies on parent project

✅ **Complete React application**
- All source code in `src/`
- Build configuration in place
- Package dependencies defined

✅ **Ready to distribute**
- Copy this entire directory anywhere
- Share with others
- Deploy to any hosting service

## 📦 Quick Start (Standalone)

```bash
# If someone shared this chapter-viewer with you:

# 1. Install dependencies
pnpm install
# or: npm install

# 2. Start the development server
pnpm dev
# or: npm run dev

# 3. Open http://localhost:5173 in your browser
```

That's it! The book will load automatically.

## 📂 Directory Structure

```
chapter-viewer/
├── book_content_json/          ← All book data (self-contained!)
│   ├── index.json              ← Chapter list
│   ├── toc_structure.json      ← Table of contents
│   └── chapter_XX/             ← Individual chapters
│       ├── chapter.json        ← Chapter metadata
│       ├── section_XX.json     ← Section content
│       └── pictures/           ← Chapter images
│
├── public/
│   └── book_content_json/      ← Symlink to ../book_content_json/
│
├── src/                        ← React application source
│   ├── components/
│   ├── pages/
│   └── App.jsx
│
├── package.json                ← Dependencies
└── vite.config.js              ← Build configuration
```

## 🚀 Distribution Options

### Option 1: Share as Archive

```bash
# Create a compressed archive
tar -czf my-book-viewer.tar.gz chapter-viewer/

# Or zip it
zip -r my-book-viewer.zip chapter-viewer/
```

Recipients extract and run:
```bash
tar -xzf my-book-viewer.tar.gz
cd chapter-viewer
pnpm install
pnpm dev
```

### Option 2: Deploy to Web

Build for production and deploy:

```bash
pnpm build
# Output is in dist/

# Deploy to:
# - GitHub Pages
# - Netlify
# - Vercel
# - Any static hosting
```

### Option 3: Git Repository

```bash
cd chapter-viewer
git init
git add .
git commit -m "Initial commit: Standalone book viewer"
git remote add origin https://github.com/user/my-book-viewer.git
git push -u origin main
```

## 🔄 Using with Your Own Book Content

To replace the book content with your own:

### Method 1: Direct Replacement

```bash
# 1. Remove existing content
rm -rf book_content_json/

# 2. Add your content
mkdir book_content_json
# Copy your book JSON files here

# 3. Update the symlink (if broken)
cd public
rm -f book_content_json
ln -s ../book_content_json book_content_json
cd ..

# 4. Run the viewer
pnpm dev
```

### Method 2: Generate from Word Document

If you have the parent project that generates content:

```bash
# In the parent project directory:
make build

# The chapter-viewer/ directory will be updated with new content
# Copy the chapter-viewer directory to distribute
cp -r chapter-viewer ../my-new-book-viewer/
```

## 📋 Content Format

Your `book_content_json/` directory must contain:

### index.json
```json
{
  "chapters": [
    {
      "number": 1,
      "title": "Chapter Title",
      "sections": 5
    }
  ]
}
```

### chapter_XX/chapter.json
```json
{
  "chapter_number": 1,
  "chapter_title": "Chapter Title",
  "sections": [
    {"section_number": 1, "title": "Section Title"}
  ]
}
```

### chapter_XX/section_XX.json
```json
{
  "chapter_number": 1,
  "chapter_title": "Chapter Title",
  "content": [
    {
      "type": "paragraph",
      "text": "Paragraph text",
      "runs": [
        {"text": "Bold text", "bold": true}
      ]
    }
  ]
}
```

## 🛠️ Customization

### Change Branding

Edit `index.html`:
```html
<title>Your Book Title</title>
```

Edit `src/App.jsx`:
```jsx
// Update the home page title
<h1>Your Book Title</h1>
```

### Styling

Modify `src/index.css` for global styles:
```css
:root {
  --primary-color: #your-color;
}
```

### Add Features

The React codebase is clean and modular:
- `src/components/Sidebar.jsx` - Navigation
- `src/pages/Home.jsx` - Landing page
- `src/pages/ChapterView.jsx` - Chapter display

## 🌐 Deployment Examples

### GitHub Pages

```bash
# 1. Build
pnpm build

# 2. Deploy
# Push dist/ folder to gh-pages branch
# Or use GitHub Actions
```

### Netlify

```bash
# 1. Connect repository to Netlify
# 2. Build command: pnpm build
# 3. Publish directory: dist
```

### Vercel

```bash
# 1. Import project in Vercel
# 2. Framework: Vite
# 3. Build command: pnpm build
# 4. Output directory: dist
```

### Static Server

```bash
# Build
pnpm build

# Serve with any static file server
cd dist
python -m http.server 8000
# or
npx serve
```

## 📝 Notes

### The Symlink

The `public/book_content_json/` is a symbolic link to `../book_content_json/`. This allows:
- Development server to access the data
- Easy content updates (edit in one place)
- Self-contained distribution

If the symlink breaks, recreate it:
```bash
cd public
ln -s ../book_content_json book_content_json
```

### Windows Users

Windows may have issues with symlinks. Instead, you can:
1. Copy (not symlink) content to public folder
2. Or run as administrator to create symlinks
3. Or use WSL (Windows Subsystem for Linux)

For distribution on Windows:
```bash
# Replace symlink with actual folder
rm public/book_content_json
cp -r book_content_json public/
```

### Large Books

For very large books (100+ chapters, 1000+ images):
- Consider lazy loading sections
- Optimize images (WebP format)
- Enable production build minification
- Use CDN for hosting

## 🤝 Contributing

To improve the viewer itself:
1. Fork this directory as a separate project
2. Make improvements to the React app
3. Share back improvements via the parent project

## 📄 License

This viewer is part of the Document Conversion System, licensed under GPL-3.0.

See the parent project's LICENSE file for details.

## 🆘 Troubleshooting

### "Cannot find book_content_json"
- Ensure `book_content_json/` exists in this directory
- Check that it contains `index.json`
- Verify the symlink: `ls -la public/book_content_json`

### Images Not Loading
- Check images are in `book_content_json/chapter_XX/pictures/`
- Verify image paths in section JSON files
- Ensure image filenames match references

### Build Fails
- Check Node.js version: `node --version` (should be 16+)
- Clear node_modules: `rm -rf node_modules && pnpm install`
- Check for port conflicts: `lsof -i :5173`

### Blank Page After Deploy
- Check browser console for errors
- Ensure `dist/` folder is deployed completely
- Verify base URL in `vite.config.js` if not at root path

## 📚 More Information

See the other documentation files:
- `README.md` - Full viewer documentation
- `QUICKSTART.md` - Quick setup guide
- `DEPLOYMENT_CHECKLIST.md` - Production deployment guide
- `VISUAL_GUIDE.md` - UI/UX documentation

---

**You now have a complete, portable book viewer!** 🎉

Share it, deploy it, or customize it for your needs.