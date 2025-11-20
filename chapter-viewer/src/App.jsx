import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ChapterView from './pages/ChapterView';
import Home from './pages/Home';
import './App.css';

function App() {
  const [index, setIndex] = useState(null);
  const [loading, setLoading] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [expandedChapter, setExpandedChapter] = useState(null);

  useEffect(() => {
    // Load the index.json to get all chapters and sections
    fetch('/book_content_json/index.json')
      .then(res => res.json())
      .then(data => {
        setIndex(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error loading index:', err);
        setLoading(false);
      });
  }, []);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  // Set expanded chapter (called from ChapterView to keep chapter expanded)
  const setExpandedChapterNum = (chapterNum) => {
    setExpandedChapter(chapterNum);
  };

  // Toggle expanded chapter (called from Sidebar when user clicks chapter)
  const toggleChapterExpand = (chapterNum) => {
    setExpandedChapter(current => current === chapterNum ? null : chapterNum);
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Loading handbook...</p>
      </div>
    );
  }

  return (
    <Router>
      <div className="app">
        <Sidebar 
          index={index}
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          expandedChapter={expandedChapter}
          onChapterToggle={toggleChapterExpand}
        />
        
        <div className="main-content">
          <button 
            className="menu-button"
            onClick={toggleSidebar}
            aria-label="Toggle menu"
          >
            ☰
          </button>
          
          <Routes>
            <Route path="/" element={<Home index={index} />} />
            <Route 
              path="/chapter/:chapterNum" 
              element={
                <ChapterView 
                  index={index}
                  expandedChapter={expandedChapter}
                  setExpandedChapter={setExpandedChapterNum}
                />
              } 
            />
            <Route 
              path="/chapter/:chapterNum/section/:sectionNum" 
              element={
                <ChapterView 
                  index={index}
                  expandedChapter={expandedChapter}
                  setExpandedChapter={setExpandedChapterNum}
                />
              } 
            />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;