# Deployment Checklist - Animal Health Handbook Chapter Viewer

## Pre-Deployment Checklist

### ✅ Development Complete
- [ ] All components created and functional
- [ ] All CSS files properly linked
- [ ] Routing configured correctly
- [ ] Data loading working from public folder
- [ ] No console errors in development

### ✅ Testing
- [ ] Test on Chrome/Edge (latest)
- [ ] Test on Firefox (latest)
- [ ] Test on Safari (latest)
- [ ] Test on mobile devices (iOS/Android)
- [ ] Test all chapters load correctly
- [ ] Test sidebar open/close on mobile
- [ ] Test navigation between chapters
- [ ] Test image loading
- [ ] Test table rendering (especially expanded tables)
- [ ] Test footnote links
- [ ] Test print functionality
- [ ] Test at different screen sizes (320px, 768px, 1024px, 1920px)

### ✅ Content Verification
- [ ] All 28 chapters present in `public/chapters_json/`
- [ ] `index.json` exists and is valid
- [ ] All chapter JSON files are valid
- [ ] All images exist in respective `pictures/` folders
- [ ] Image paths match JSON references
- [ ] No broken image links

### ✅ Performance
- [ ] Initial load time < 3 seconds
- [ ] Chapter load time < 1 second
- [ ] Images load progressively
- [ ] No memory leaks
- [ ] Smooth scrolling
- [ ] No layout shifts

### ✅ Accessibility
- [ ] Keyboard navigation works
- [ ] Focus indicators visible
- [ ] Touch targets minimum 44x44px
- [ ] Color contrast meets WCAG AA
- [ ] Semantic HTML used
- [ ] Alt text on images (where applicable)

### ✅ Code Quality
- [ ] No ESLint errors
- [ ] No console warnings
- [ ] Code is commented where needed
- [ ] CSS is organized and clean
- [ ] No unused imports or code

## Build Process

### Step 1: Prepare Environment
```bash
cd pp-book/chapter-viewer
pnpm install
```

### Step 2: Verify Data
```bash
# Check that chapters_json exists
ls -la public/chapters_json/

# Verify index.json
cat public/chapters_json/index.json

# Count chapters
ls public/chapters_json/ | grep chapter_ | wc -l
# Should show 28
```

### Step 3: Build
```bash
# Clean build
rm -rf dist/

# Build production version
pnpm build
```

### Step 4: Test Production Build
```bash
# Preview the build
pnpm preview

# Open browser to http://localhost:4173
# Test thoroughly
```

### Step 5: Verify Build Output
```bash
# Check dist folder
ls -la dist/

# Should contain:
# - index.html
# - assets/ (JS and CSS files)
# - chapters_json/ (all chapter data)
```

## Deployment Options

### Option 1: Static Hosting (Netlify)

#### Prerequisites
- [ ] Netlify account created
- [ ] Site name chosen

#### Steps
1. Login to Netlify
2. Click "Add new site" → "Deploy manually"
3. Drag and drop the `dist` folder
4. Wait for deployment
5. Test the live URL
6. Configure custom domain (optional)

#### Configuration
- Build command: `pnpm build`
- Publish directory: `dist`
- Node version: 18+

### Option 2: Vercel

#### Prerequisites
- [ ] Vercel account created
- [ ] Vercel CLI installed (optional)

#### Steps via CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd chapter-viewer
vercel --prod
```

#### Steps via Web
1. Login to Vercel
2. Import project from Git or upload
3. Configure:
   - Framework: Vite
   - Build command: `pnpm build`
   - Output directory: `dist`
4. Deploy

### Option 3: GitHub Pages

#### Prerequisites
- [ ] GitHub repository created
- [ ] Git initialized

#### Steps
```bash
# Install gh-pages
pnpm add -D gh-pages

# Add to package.json scripts:
# "deploy": "gh-pages -d dist"

# Build and deploy
pnpm build
pnpm deploy
```

#### Configure GitHub Pages
1. Go to repository Settings
2. Pages → Source → gh-pages branch
3. Save and wait for deployment

### Option 4: Traditional Web Server (Apache/Nginx)

#### Apache Configuration
```apache
<VirtualHost *:80>
    ServerName animal-health-handbook.example.com
    DocumentRoot /var/www/html/chapter-viewer

    <Directory /var/www/html/chapter-viewer>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
        
        # Enable SPA routing
        RewriteEngine On
        RewriteBase /
        RewriteRule ^index\.html$ - [L]
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule . /index.html [L]
    </Directory>
</VirtualHost>
```

#### Nginx Configuration
```nginx
server {
    listen 80;
    server_name animal-health-handbook.example.com;
    root /var/www/html/chapter-viewer;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Gzip compression
    gzip on;
    gzip_types text/css application/javascript application/json image/svg+xml;
    gzip_min_length 1000;
}
```

#### Deployment Steps
```bash
# Build
pnpm build

# Copy to server
scp -r dist/* user@server:/var/www/html/chapter-viewer/

# Or use rsync
rsync -avz --delete dist/ user@server:/var/www/html/chapter-viewer/

# Set permissions
ssh user@server "chmod -R 755 /var/www/html/chapter-viewer"
```

### Option 5: Docker Container

#### Dockerfile
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json pnpm-lock.yaml ./
RUN npm install -g pnpm
RUN pnpm install
COPY . .
RUN pnpm build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Build and Run
```bash
# Build image
docker build -t chapter-viewer .

# Run container
docker run -d -p 80:80 chapter-viewer

# Or with docker-compose
docker-compose up -d
```

## Post-Deployment Checklist

### ✅ Verification
- [ ] Site is accessible at deployment URL
- [ ] All chapters load correctly
- [ ] Images load properly
- [ ] Navigation works on mobile
- [ ] No 404 errors in browser console
- [ ] No mixed content warnings (if using HTTPS)
- [ ] Sidebar opens/closes correctly on mobile
- [ ] Routing works (refresh on any page)

### ✅ Performance Check
- [ ] Run Lighthouse audit (score > 90)
- [ ] Check load times with slow 3G
- [ ] Verify images load progressively
- [ ] Check memory usage
- [ ] Test on actual mobile devices

### ✅ SEO & Metadata
- [ ] Title tag is correct
- [ ] Meta description is present
- [ ] Favicon displays correctly
- [ ] Open Graph tags (if needed)
- [ ] robots.txt configured (if needed)

### ✅ Analytics (Optional)
- [ ] Google Analytics configured
- [ ] Privacy policy added (if collecting data)
- [ ] Cookie consent (if required by region)

### ✅ Monitoring
- [ ] Uptime monitoring configured
- [ ] Error tracking setup (Sentry, etc.)
- [ ] Analytics dashboard setup
- [ ] Alert notifications configured

## Troubleshooting

### Images Not Loading
**Problem**: 404 errors for images  
**Solution**: 
- Check `public/chapters_json/` folder structure
- Verify image paths in JSON files
- Ensure images were included in build

### Routing Errors on Refresh
**Problem**: 404 when refreshing chapter pages  
**Solution**:
- Configure server for SPA routing (see configs above)
- All routes should fallback to index.html

### Blank Page After Deployment
**Problem**: White screen, no errors  
**Solution**:
- Check browser console for errors
- Verify base URL in vite.config.js
- Check if assets are loading correctly

### Slow Initial Load
**Problem**: Long time to first render  
**Solution**:
- Enable gzip compression on server
- Configure CDN (Cloudflare, etc.)
- Check network waterfall in DevTools

## Maintenance

### Regular Updates
- [ ] Update dependencies monthly: `pnpm update`
- [ ] Check for security vulnerabilities: `pnpm audit`
- [ ] Review and update content as needed
- [ ] Monitor error logs

### Content Updates
When chapters are updated:
1. Run `split_chapters_to_json.py` to regenerate JSON
2. Copy updated `chapters_json/` to `public/`
3. Rebuild: `pnpm build`
4. Deploy updated `dist/` folder

### Backup
- [ ] Backup `chapters_json/` data regularly
- [ ] Keep source .docx files safe
- [ ] Version control for code (Git)
- [ ] Document any configuration changes

## Support & Documentation

### User Documentation
- [ ] README.md is up to date
- [ ] QUICKSTART.md is accurate
- [ ] VISUAL_GUIDE.md reflects current UI
- [ ] Help section or FAQ (if needed)

### Developer Documentation
- [ ] Code comments are sufficient
- [ ] Component structure is documented
- [ ] API/data format is documented
- [ ] Deployment process is documented

## Final Sign-Off

- [ ] All checklist items completed
- [ ] Testing passed on all target devices
- [ ] Stakeholders have reviewed and approved
- [ ] Documentation is complete
- [ ] Deployment is successful
- [ ] Monitoring is active

---

**Deployment Date**: _______________  
**Deployed By**: _______________  
**Deployment URL**: _______________  
**Version**: 1.0.0

**Notes**:
_____________________________________________
_____________________________________________
_____________________________________________

---

## Quick Deployment Commands

```bash
# Development
pnpm dev

# Production Build
pnpm build

# Preview Production
pnpm preview

# Deploy with script
./deploy.sh

# Check for issues
pnpm lint
```

## Emergency Rollback

If something goes wrong:

1. **Netlify/Vercel**: Use platform's rollback feature
2. **Manual**: Replace with previous `dist/` folder
3. **Git**: Revert to previous commit and rebuild
4. **Docker**: Redeploy previous image tag

```bash
# Git rollback
git revert HEAD
pnpm build
# Redeploy

# Docker rollback
docker pull chapter-viewer:previous-tag
docker run -d -p 80:80 chapter-viewer:previous-tag
```

---

**Remember**: Always test thoroughly before deploying to production!

🎉 **Good luck with your deployment!**