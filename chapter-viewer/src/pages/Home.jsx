import { Link } from 'react-router-dom';
import './Home.css';

function Home({ index }) {
  if (!index) {
    return (
      <div className="home-page">
        <p>Loading...</p>
      </div>
    );
  }

  const cleanTitle = (title) => {
    // Remove page numbers and dots from TOC entries
    return title.replace(/\.{2,}\s*\d+$/, '').trim();
  };

  return (
    <div className="home-page">
      <header className="home-header">
        <h1>{index.book_title}</h1>
        <p className="subtitle">A comprehensive guide to livestock health and disease management</p>
        <div className="stats">
          <span>{index.total_chapters} chapters</span>
          <span>•</span>
          <span>{index.total_sections} sections</span>
        </div>
      </header>

      <div className="chapters-grid">
        {index.chapters.map((chapter) => (
          <Link
            key={chapter.number}
            to={`/chapter/${chapter.number}`}
            className="chapter-card"
          >
            <div className="chapter-card-number">
              Chapter {chapter.number}
            </div>
            <div className="chapter-card-title">
              {cleanTitle(chapter.title)}
            </div>
            <div className="chapter-card-stats">
              {chapter.total_sections} section{chapter.total_sections !== 1 ? 's' : ''}
            </div>
            <div className="chapter-card-arrow">→</div>
          </Link>
        ))}
      </div>
    </div>
  );
}

export default Home;