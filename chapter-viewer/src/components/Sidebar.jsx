import { Link, useLocation, useNavigate } from 'react-router-dom';
import './Sidebar.css';

function Sidebar({ index, isOpen, onClose, expandedChapter, onChapterToggle }) {
  const location = useLocation();
  const navigate = useNavigate();

  if (!index) {
    return null;
  }

  const cleanTitle = (title) => {
    // Remove chapter number prefix for cleaner display
    return title.replace(/^\d+\.\d+\s*/, '').trim();
  };

  const isActiveChapter = (chapterNum) => {
    const match = location.pathname.match(/^\/chapter\/(\d+)/);
    return match && parseInt(match[1]) === chapterNum;
  };

  const isActiveSection = (chapterNum, sectionNum) => {
    const match = location.pathname.match(/^\/chapter\/(\d+)(?:\/section\/(\d+))?$/);
    if (!match) return false;
    
    const currentChapter = parseInt(match[1]);
    const currentSection = match[2] ? parseInt(match[2]) : 0;
    
    return currentChapter === chapterNum && currentSection === sectionNum;
  };

  const handleChapterClick = (chapter) => {
    // Toggle expand/collapse sections
    onChapterToggle(chapter.number);
    
    // Navigate to chapter intro
    navigate(`/chapter/${chapter.number}`);
    
    // Close sidebar on mobile
    if (window.innerWidth <= 768) {
      onClose();
    }
  };

  const handleSectionClick = (chapterNum, sectionNum) => {
    if (sectionNum === 0) {
      navigate(`/chapter/${chapterNum}`);
    } else {
      navigate(`/chapter/${chapterNum}/section/${sectionNum}`);
    }
    
    // Close sidebar on mobile
    if (window.innerWidth <= 768) {
      onClose();
    }
  };

  return (
    <>
      {/* Overlay for mobile */}
      {isOpen && (
        <div className="sidebar-overlay" onClick={onClose}></div>
      )}
      
      <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <h1 className="sidebar-title">{index.book_title}</h1>
          <button 
            className="close-button"
            onClick={onClose}
            aria-label="Close menu"
          >
            ✕
          </button>
        </div>
        
        <nav className="sidebar-nav">
          <Link 
            to="/" 
            className={`nav-item home-link ${location.pathname === '/' ? 'active' : ''}`}
            onClick={onClose}
          >
            <span className="nav-icon">🏠</span>
            <span>Home</span>
          </Link>
          
          <div className="nav-divider"></div>
          
          <div className="chapters-list">
            {index.chapters.map((chapter) => {
              const isExpanded = expandedChapter === chapter.number;
              const isActive = isActiveChapter(chapter.number);
              
              return (
                <div key={chapter.number} className="chapter-group">
                  <div
                    className={`nav-item chapter-item ${isActive ? 'active' : ''}`}
                    onClick={() => handleChapterClick(chapter)}
                  >
                    <div className="sidebar-chapter-content">
                      <span className="sidebar-chapter-number">{chapter.number}</span>
                      <span className="sidebar-chapter-title">{cleanTitle(chapter.title)}</span>
                    </div>
                    {chapter.sections && chapter.sections.length > 1 && (
                      <span className={`expand-icon ${isExpanded ? 'expanded' : ''}`}>
                        ▼
                      </span>
                    )}
                  </div>
                  
                  {/* Section list - only show when chapter is expanded */}
                  {isExpanded && chapter.sections && chapter.sections.length > 1 && (
                    <div className="sections-list">
                      {chapter.sections.map((section) => (
                        <div
                          key={section.section_number}
                          className={`nav-item section-item ${
                            isActiveSection(chapter.number, section.section_number) ? 'active' : ''
                          }`}
                          onClick={() => handleSectionClick(chapter.number, section.section_number)}
                        >
                          <span className="sidebar-section-number">
                            {section.section_number === 0 ? 'Intro' : `${chapter.number}.${section.section_number}`}
                          </span>
                          <span className="sidebar-section-title">
                            {cleanTitle(section.title)}
                          </span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </nav>
      </aside>
    </>
  );
}

export default Sidebar;