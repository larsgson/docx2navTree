# Visual Guide - Animal Health Handbook Chapter Viewer

This guide describes the visual layout and user interface of the application.

## 🎨 Application Layout

### Desktop View (> 768px)

```
┌─────────────────────────────────────────────────────────────┐
│  ┌──────────────┐  ┌───────────────────────────────────┐   │
│  │              │  │                                   │   │
│  │   SIDEBAR    │  │        MAIN CONTENT              │   │
│  │              │  │                                   │   │
│  │ ┌──────────┐ │  │  ┌─────────────────────────┐    │   │
│  │ │   🏠     │ │  │  │  Chapter Title           │    │   │
│  │ │   Home   │ │  │  │  ═══════════════════     │    │   │
│  │ └──────────┘ │  │  │  Statistics: X items     │    │   │
│  │              │  │  └─────────────────────────┘    │   │
│  │ ────────────  │  │                                   │   │
│  │              │  │  Paragraph text with formatting   │   │
│  │ ┌──────────┐ │  │  and images...                   │   │
│  │ │ 1        │ │  │                                   │   │
│  │ │ Health & │ │  │  ┌─────────────────────┐         │   │
│  │ │ Disease  │ │  │  │     [TABLE]         │         │   │
│  │ └──────────┘ │  │  └─────────────────────┘         │   │
│  │              │  │                                   │   │
│  │ ┌──────────┐ │  │  More paragraph content...       │   │
│  │ │ 2        │ │  │                                   │   │
│  │ │ Restraint│ │  │  ┌─────────────────┐             │   │
│  │ └──────────┘ │  │  │   [IMAGE]       │             │   │
│  │              │  │  │   Caption text  │             │   │
│  │ ┌──────────┐ │  │  └─────────────────┘             │   │
│  │ │ 3        │ │  │                                   │   │
│  │ │ Clinical │ │  │  Footnotes:                      │   │
│  │ │ Exam...  │ │  │  ¹ Footnote text here...         │   │
│  │ └──────────┘ │  │                                   │   │
│  │              │  │                                   │   │
│  │     ...      │  │                                   │   │
│  │              │  │                                   │   │
│  └──────────────┘  └───────────────────────────────────┘   │
│     280px                    850px max width                │
└─────────────────────────────────────────────────────────────┘
```

### Mobile View (< 768px)

**Closed Sidebar:**
```
┌───────────────────────────────┐
│  ┌───┐                        │
│  │ ☰ │  Menu Button           │
│  └───┘                        │
│                                │
│  ┌──────────────────────────┐ │
│  │  Chapter Title           │ │
│  │  ═══════════════════     │ │
│  └──────────────────────────┘ │
│                                │
│  Paragraph text that flows    │
│  naturally on mobile screens  │
│  with proper wrapping...      │
│                                │
│  ┌────────────────────────┐   │
│  │    [TABLE]            │   │
│  │  (scrollable →)        │   │
│  └────────────────────────┘   │
│                                │
│  ┌────────────────────┐       │
│  │     [IMAGE]        │       │
│  │  Caption text      │       │
│  └────────────────────┘       │
│                                │
└───────────────────────────────┘
```

**Open Sidebar:**
```
┌───────────────────────────────┐
│ ┌─────────────┐ [Dark overlay]│
│ │ Animal      │ X             │
│ │ Health      │               │
│ │ Handbook    │               │
│ │             │               │
│ │ 🏠 Home     │               │
│ │ ──────────  │               │
│ │             │               │
│ │ ┌─────────┐ │               │
│ │ │ 1       │ │               │
│ │ │ Health  │ │               │
│ │ └─────────┘ │               │
│ │             │               │
│ │ ┌─────────┐ │               │
│ │ │ 2       │ │               │
│ │ │ Restrain│ │               │
│ │ └─────────┘ │               │
│ │             │               │
│ │    ...      │               │
│ │             │               │
│ └─────────────┘               │
└───────────────────────────────┘
```

## 🏠 Home Page

### Desktop Home View
```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│              Animal Health Handbook                          │
│     A comprehensive guide to livestock health and disease    │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ CHAPTER 1│  │ CHAPTER 2│  │ CHAPTER 3│  │ CHAPTER 4│   │
│  │          │  │          │  │          │  │          │   │
│  │ Health & │  │ Restraint│  │ Clinical │  │ Principl │   │
│  │ Disease  │  │ Handling │  │ Exam...  │  │ Treatmnt │   │
│  │       →  │  │       →  │  │       →  │  │       →  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ CHAPTER 5│  │ CHAPTER 6│  │ CHAPTER 7│  │ CHAPTER 8│   │
│  │          │  │          │  │          │  │          │   │
│  │ First Aid│  │ Infectio │  │ Nutritio │  │ Parasite │   │
│  │          │  │ Diseases │  │ n        │  │ on Skin  │   │
│  │       →  │  │       →  │  │       →  │  │       →  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                              │
│                        ...more cards...                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Mobile Home View
```
┌───────────────────────────────┐
│  ┌───┐                        │
│  │ ☰ │                        │
│  └───┘                        │
│                                │
│    Animal Health Handbook      │
│  A comprehensive guide to      │
│  livestock health...           │
│                                │
│  ┌──────────────────────────┐ │
│  │ CHAPTER 1                │ │
│  │                          │ │
│  │ Health & Disease         │ │
│  │                       → │ │
│  └──────────────────────────┘ │
│                                │
│  ┌──────────────────────────┐ │
│  │ CHAPTER 2                │ │
│  │                          │ │
│  │ Restraint & Handling     │ │
│  │                       → │ │
│  └──────────────────────────┘ │
│                                │
│  ┌──────────────────────────┐ │
│  │ CHAPTER 3                │ │
│  │                          │ │
│  │ Clinical Examination...  │ │
│  │                       → │ │
│  └──────────────────────────┘ │
│                                │
│         (scrollable)           │
│                                │
└───────────────────────────────┘
```

## 📄 Chapter View Details

### Chapter Header
```
┌───────────────────────────────────────────┐
│  2.0 Restraint & Handling, Aging & Weight │
│  ═════════════════════════════════════════│
│  📊 145 paragraphs | 7 tables | 12 images │
└───────────────────────────────────────────┘
```

### Formatted Paragraph
```
┌───────────────────────────────────────────┐
│  **1.1 HEALTH & DISEASE DEFINED**         │
│                                            │
│  Health is a state of complete physical,  │
│  mental and social well-being. Disease is │
│  *any deviation from normal health*.      │
│                                            │
│  Key symptoms include:                     │
│  • Loss of appetite                        │
│  • Fever                                   │
│  • Behavioral changes¹                     │
│                                            │
└───────────────────────────────────────────┘
```

### Table Display
```
┌─────────────────────────────────────────────┐
│ ┌─────────────────────────────────────────┐ │
│ │ Species    │ Normal Temp │ Heart Rate   │ │
│ ├────────────┼─────────────┼──────────────┤ │
│ │ Cattle     │ 38.5°C      │ 60-80 bpm    │ │
│ │ Sheep      │ 39.0°C      │ 70-90 bpm    │ │
│ │ Goat       │ 39.5°C      │ 70-95 bpm    │ │
│ │ Horse      │ 38.0°C      │ 30-40 bpm    │ │
│ └────────────┴─────────────┴──────────────┘ │
│                                              │
│ Note: This table was automatically expanded  │
│ from 1 original row(s)                       │
└─────────────────────────────────────────────┘
```

### Image Display
```
┌───────────────────────────────────────────┐
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │                                      │ │
│  │         [Image of cattle]            │ │
│  │                                      │ │
│  │     (scales to fit screen width)     │ │
│  │                                      │ │
│  └──────────────────────────────────────┘ │
│     Figure 2.3: Proper restraint          │
│     technique for cattle examination      │
│                                            │
└───────────────────────────────────────────┘
```

### Footnotes Section
```
┌───────────────────────────────────────────┐
│  Footnotes                                 │
│  ═════════                                 │
│                                            │
│  ¹ Behavioral changes may include lethargy│
│    isolation from herd, or unusual        │
│    vocalizations.                         │
│                                            │
│  ² Temperature should be measured rectally│
│    for accuracy.                          │
│                                            │
└───────────────────────────────────────────┘
```

## 🎨 Color Scheme

### Primary Colors
- **Sidebar Background**: Forest Green (#2c5f2d)
- **Active Items**: Darker Green (#1e4620)
- **Hover States**: Light Green (#4a8f4c)

### Text Colors
- **Primary Text**: Dark Gray (#333)
- **Secondary Text**: Medium Gray (#666)
- **Links**: Forest Green (#2c5f2d)

### Backgrounds
- **Main Background**: White (#fff)
- **Table Headers**: Forest Green (#2c5f2d)
- **Alternate Rows**: Light Gray (#f9f9f9)
- **Sidebar**: Forest Green (#2c5f2d)

### Borders & Shadows
- **Borders**: Light Gray (#ddd)
- **Card Shadow**: 0 2px 4px rgba(0,0,0,0.1)
- **Hover Shadow**: 0 4px 12px rgba(0,0,0,0.15)

## 🔘 Interactive Elements

### Buttons & Links

**Menu Button (Mobile)**
```
┌─────┐
│  ☰  │  ← Green background
└─────┘     White icon
            44x44px touch target
```

**Navigation Items**
```
┌──────────────────────────────┐
│  [2]  Restraint & Handling   │  ← Default state
└──────────────────────────────┘

┌──────────────────────────────┐
│ █[2]  Restraint & Handling   │  ← Active (left border)
└──────────────────────────────┘

┌──────────────────────────────┐
│    [2]  Restraint & Handling │  ← Hover (indent right)
└──────────────────────────────┘
```

**Chapter Cards (Home)**
```
┌────────────────────┐       ┌────────────────────┐
│ CHAPTER 1          │       │ CHAPTER 1          │
│                    │  →    │                    │
│ Health & Disease   │       │ Health & Disease   │
│                 →  │       │                 →  │
└────────────────────┘       └────────────────────┘
   Default state            Hover (raised, shadow)
```

## 📱 Mobile Interactions

### Touch Gestures
- **Tap**: Navigate to chapter/page
- **Tap outside**: Close sidebar
- **Scroll**: Navigate content
- **Pinch**: Zoom images
- **Swipe**: (Browser native scroll)

### Responsive Text Sizes
- **Mobile Title**: 24px
- **Mobile Body**: 15px
- **Mobile Table**: 13px
- **Desktop Title**: 28px
- **Desktop Body**: 16px
- **Desktop Table**: 14px

## 🖨️ Print Layout

When printing (Ctrl+P / Cmd+P):
```
┌───────────────────────────────────────────┐
│                                            │
│  2.0 Restraint & Handling, Aging & Weight │
│  ═════════════════════════════════════════│
│                                            │
│  [Sidebar hidden]                          │
│  [Full width content]                      │
│  [Optimized spacing]                       │
│  [Page breaks at logical points]           │
│                                            │
│  Content flows naturally for printing...  │
│                                            │
│  Tables and images avoid page breaks...   │
│                                            │
└───────────────────────────────────────────┘
```

## 🎯 Key Visual Features

### ✅ Consistent Spacing
- Sidebar items: 12px vertical padding
- Content paragraphs: 16px bottom margin
- Tables: 24px top/bottom margin
- Images: 20px top/bottom margin

### ✅ Visual Hierarchy
- Chapter titles: Large, bold, green
- Section headings: Bold, larger than body
- Body text: Regular weight, high line-height
- Footnotes: Smaller, lighter color

### ✅ Feedback Indicators
- Hover: Background color change + cursor pointer
- Active: Border highlight + background shade
- Loading: Animated spinner
- Error: Red text with clear message

### ✅ Accessibility
- High contrast ratios (4.5:1 minimum)
- Focus indicators: 2px green outline
- Touch targets: Minimum 44x44px
- Clear visual hierarchy
- Keyboard navigation support

## 🌈 State Variations

### Loading State
```
    ⊙     ← Spinning animation
    
  Loading chapter 5...
```

### Error State
```
  ⚠ Error Loading Chapter
  
  Chapter not found
```

### Empty State
```
  📚 Welcome!
  
  Select a chapter to begin reading
```

## 📐 Measurements

### Desktop
- Sidebar: 280px fixed width
- Content: 850px max width
- Content padding: 60px
- Margins: Auto-centered

### Mobile
- Full width: 100vw
- Content padding: 20px
- No fixed widths
- Flexible layouts

### Breakpoints
- Mobile: 0-768px
- Tablet: 769-1024px
- Desktop: 1025px+
- Large: 1400px+

---

This visual guide provides a comprehensive overview of the application's user interface and visual design system.