import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import "./ChapterView.css";

function ChapterView({ index, expandedChapter, setExpandedChapter }) {
  const { chapterNum, sectionNum } = useParams();
  const navigate = useNavigate();

  // Get current chapter and section info
  const currentChapter = index?.chapters.find(
    (c) => c.number === parseInt(chapterNum),
  );
  const currentSectionNum = sectionNum ? parseInt(sectionNum) : 0;
  const currentSection = currentChapter?.sections.find(
    (s) => s.section_number === currentSectionNum,
  );

  // Create a unique key for the current section to trigger effect reset
  const sectionKey = `${chapterNum}-${currentSectionNum}`;
  const [dataState, setDataState] = useState({
    content: null,
    loading: true,
    error: null,
    key: sectionKey,
  });

  // Touch/swipe handling for mobile navigation
  const touchStartX = useRef(null);
  const touchStartY = useRef(null);
  const containerRef = useRef(null);
  const [swipeDirection, setSwipeDirection] = useState(null);

  useEffect(() => {
    if (!currentSection) {
      return;
    }

    const path = `/book_content_json/${currentSection.path}`;

    fetch(path)
      .then((res) => {
        if (!res.ok) throw new Error("Section not found");
        return res.json();
      })
      .then((data) => {
        setDataState({
          content: data,
          loading: false,
          error: null,
          key: sectionKey,
        });
      })
      .catch((err) => {
        console.error("Error loading section:", err);
        setDataState({
          content: null,
          loading: false,
          error: err.message,
          key: sectionKey,
        });
      });
  }, [sectionKey, currentSection]);

  const { content, loading, error } = dataState;

  // Auto-expand chapter in sidebar (only if not already expanded)
  useEffect(() => {
    const chapterNumber = currentChapter?.number;
    if (
      chapterNumber &&
      setExpandedChapter &&
      expandedChapter !== chapterNumber
    ) {
      setExpandedChapter(chapterNumber);
    }
  }, [currentChapter, expandedChapter, setExpandedChapter]);

  // Navigation helpers
  const getNextSection = () => {
    if (!currentChapter || !index) return null;

    const currentIdx = currentChapter.sections.findIndex(
      (s) => s.section_number === currentSectionNum,
    );

    // Next section in current chapter
    if (currentIdx < currentChapter.sections.length - 1) {
      const nextSection = currentChapter.sections[currentIdx + 1];
      return {
        chapterNum: currentChapter.number,
        sectionNum: nextSection.section_number,
        title: nextSection.title,
      };
    }

    // First section of next chapter
    const chapterIdx = index.chapters.findIndex(
      (c) => c.number === currentChapter.number,
    );
    if (chapterIdx < index.chapters.length - 1) {
      const nextChapter = index.chapters[chapterIdx + 1];
      return {
        chapterNum: nextChapter.number,
        sectionNum: 0,
        title: nextChapter.sections[0]?.title || "Intro",
      };
    }

    return null;
  };

  const getPreviousSection = () => {
    if (!currentChapter || !index) return null;

    const currentIdx = currentChapter.sections.findIndex(
      (s) => s.section_number === currentSectionNum,
    );

    // Previous section in current chapter
    if (currentIdx > 0) {
      const prevSection = currentChapter.sections[currentIdx - 1];
      return {
        chapterNum: currentChapter.number,
        sectionNum: prevSection.section_number,
        title: prevSection.title,
      };
    }

    // Last section of previous chapter
    const chapterIdx = index.chapters.findIndex(
      (c) => c.number === currentChapter.number,
    );
    if (chapterIdx > 0) {
      const prevChapter = index.chapters[chapterIdx - 1];
      const lastSection = prevChapter.sections[prevChapter.sections.length - 1];
      return {
        chapterNum: prevChapter.number,
        sectionNum: lastSection.section_number,
        title: lastSection.title,
      };
    }

    return null;
  };

  const handleNavigate = (chapterNum, sectionNum) => {
    if (sectionNum === 0) {
      navigate(`/chapter/${chapterNum}`);
    } else {
      navigate(`/chapter/${chapterNum}/section/${sectionNum}`);
    }
  };

  const nextSection = getNextSection();
  const previousSection = getPreviousSection();

  // Handle touch start
  const handleTouchStart = (e) => {
    touchStartX.current = e.touches[0].clientX;
    touchStartY.current = e.touches[0].clientY;
  };

  // Handle touch move - show visual feedback
  const handleTouchMove = (e) => {
    if (!touchStartX.current || !touchStartY.current) {
      return;
    }

    const touchCurrentX = e.touches[0].clientX;
    const touchCurrentY = e.touches[0].clientY;

    const deltaX = touchCurrentX - touchStartX.current;
    const deltaY = touchCurrentY - touchStartY.current;

    // Only show feedback for horizontal swipes
    if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 10) {
      if (deltaX > 0 && previousSection) {
        setSwipeDirection("right");
      } else if (deltaX < 0 && nextSection) {
        setSwipeDirection("left");
      }
    }
  };

  // Handle touch end - detect swipe gesture
  const handleTouchEnd = (e) => {
    if (!touchStartX.current || !touchStartY.current) {
      return;
    }

    const touchEndX = e.changedTouches[0].clientX;
    const touchEndY = e.changedTouches[0].clientY;

    const deltaX = touchEndX - touchStartX.current;
    const deltaY = touchEndY - touchStartY.current;

    // Only trigger swipe if horizontal movement is greater than vertical
    // This prevents interfering with scrolling
    if (Math.abs(deltaX) > Math.abs(deltaY)) {
      const minSwipeDistance = 50; // Minimum distance for a swipe

      if (deltaX > minSwipeDistance) {
        // Swipe right - go to previous section
        if (previousSection) {
          handleNavigate(
            previousSection.chapterNum,
            previousSection.sectionNum,
          );
        }
      } else if (deltaX < -minSwipeDistance) {
        // Swipe left - go to next section
        if (nextSection) {
          handleNavigate(nextSection.chapterNum, nextSection.sectionNum);
        }
      }
    }

    // Reset touch positions and swipe direction
    touchStartX.current = null;
    touchStartY.current = null;
    setSwipeDirection(null);
  };

  if (!currentSection) {
    return (
      <div className="chapter-error">
        <h2>Section Not Found</h2>
        <p>The requested section does not exist.</p>
      </div>
    );
  }

  if (loading || !content) {
    return (
      <div className="chapter-loading">
        <div className="spinner"></div>
        <p>Loading section...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="chapter-error">
        <h2>Error Loading Section</h2>
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div
      className={`chapter-view ${swipeDirection ? `swiping-${swipeDirection}` : ""}`}
      ref={containerRef}
      onTouchStart={handleTouchStart}
      onTouchMove={handleTouchMove}
      onTouchEnd={handleTouchEnd}
    >
      <div className="chapter-container">
        {/* Breadcrumb navigation */}
        <div className="breadcrumb">
          <button onClick={() => navigate("/")} className="breadcrumb-link">
            Home
          </button>
          <span className="breadcrumb-separator">›</span>
          <span className="breadcrumb-current">
            Chapter {currentChapter.number}
            {currentSectionNum > 0 && ` › Section ${currentSectionNum}`}
          </span>
        </div>

        {/* Section header */}
        <header className="chapter-header">
          <h1 className="chapter-title">
            {currentSection?.title || content.chapter_title}
          </h1>
          {content.statistics && (
            <div className="chapter-stats">
              <span>{content.statistics.paragraphs} paragraphs</span>
              <span>{content.statistics.tables} tables</span>
              <span>{content.statistics.images} images</span>
            </div>
          )}
        </header>

        {/* Section content */}
        <div className="chapter-content">
          {content.content &&
            content.content.map((item, index) => (
              <ContentItem key={index} item={item} chapterNum={chapterNum} />
            ))}
        </div>

        {/* Footnotes */}
        {content.footnotes && Object.keys(content.footnotes).length > 0 && (
          <div className="chapter-footnotes">
            <h3>Footnotes</h3>
            {Object.entries(content.footnotes).map(([id, text]) => (
              <div key={id} className="footnote" id={`footnote-${id}`}>
                <sup>{id}</sup> {text}
              </div>
            ))}
          </div>
        )}

        {/* Navigation buttons */}
        <div className="section-navigation">
          {previousSection && (
            <button
              className="nav-button nav-previous"
              onClick={() =>
                handleNavigate(
                  previousSection.chapterNum,
                  previousSection.sectionNum,
                )
              }
            >
              <span className="nav-arrow">←</span>
              <span className="nav-text">
                <span className="nav-label">Previous</span>
                <span className="nav-title">{previousSection.title}</span>
              </span>
            </button>
          )}

          {nextSection && (
            <button
              className="nav-button nav-next"
              onClick={() =>
                handleNavigate(nextSection.chapterNum, nextSection.sectionNum)
              }
            >
              <span className="nav-text">
                <span className="nav-label">Next</span>
                <span className="nav-title">{nextSection.title}</span>
              </span>
              <span className="nav-arrow">→</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

function ContentItem({ item, chapterNum }) {
  if (item.type === "paragraph") {
    return <ParagraphContent item={item} chapterNum={chapterNum} />;
  } else if (item.type === "table") {
    return <TableContent item={item} />;
  }
  return null;
}

function ParagraphContent({ item, chapterNum }) {
  const isEmpty = !item.text || item.text.trim() === "";

  if (isEmpty && (!item.images || item.images.length === 0)) {
    return <div className="paragraph-spacer"></div>;
  }

  const getTextAlign = (alignment) => {
    if (!alignment) return "left";
    if (alignment.includes("CENTER")) return "center";
    if (alignment.includes("RIGHT")) return "right";
    if (alignment.includes("JUSTIFY")) return "justify";
    return "left";
  };

  const renderRuns = () => {
    if (!item.runs || item.runs.length === 0) {
      return <span>{item.text}</span>;
    }

    return item.runs.map((run, idx) => {
      let style = {};
      let className = "";

      if (run.bold) className += " bold";
      if (run.italic) className += " italic";
      if (run.underline) className += " underline";
      if (run.font_size) style.fontSize = `${run.font_size}pt`;

      return (
        <span key={idx} className={className.trim()} style={style}>
          {run.text}
        </span>
      );
    });
  };

  const style = {
    textAlign: getTextAlign(item.alignment),
  };

  // Check if this is a heading
  const isHeading =
    item.runs &&
    item.runs.some((run) => run.bold && run.font_size && run.font_size >= 12);

  return (
    <div className="content-paragraph">
      <p className={`paragraph ${isHeading ? "heading" : ""}`} style={style}>
        {renderRuns()}
        {item.footnotes &&
          item.footnotes.map((fn, idx) => (
            <sup key={idx}>
              <a href={`#footnote-${fn.id}`} className="footnote-ref">
                {fn.id}
              </a>
            </sup>
          ))}
      </p>

      {item.images && item.images.length > 0 && (
        <div className="paragraph-images">
          {item.images.map((img, idx) => {
            // Use the path from JSON if available, otherwise construct it
            const imagePath = img.path
              ? `/book_content_json/chapter_${String(chapterNum).padStart(2, "0")}/${img.path}`
              : `/book_content_json/chapter_${String(chapterNum).padStart(2, "0")}/pictures/${img.filename}`;

            return <ImageWithRetry key={idx} imagePath={imagePath} img={img} />;
          })}
        </div>
      )}
    </div>
  );
}

function ImageWithRetry({ imagePath, img }) {
  const [retryCount, setRetryCount] = useState(0);
  const [imageKey, setImageKey] = useState(0);
  const maxRetries = 2;

  const handleImageError = (e) => {
    console.error("Image load error:", {
      filename: img.filename,
      attemptedPath: imagePath,
      fullUrl: e.target.src,
      retryCount: retryCount,
    });

    if (retryCount < maxRetries) {
      // Retry after a short delay
      setTimeout(
        () => {
          setRetryCount(retryCount + 1);
          setImageKey(imageKey + 1); // Force re-render with new key
        },
        500 * (retryCount + 1),
      ); // Increasing delay: 500ms, 1000ms
    } else {
      // After max retries, hide the image
      e.target.style.display = "none";
      const container = e.target.closest(".image-container");
      if (container) {
        container.style.display = "none";
      }
    }
  };

  return (
    <div className="image-container">
      <img
        key={imageKey}
        src={imagePath}
        alt={img.description || `Image ${img.index}`}
        className="chapter-image"
        onError={handleImageError}
      />
      {img.description && <p className="image-caption">{img.description}</p>}
    </div>
  );
}

function TableContent({ item }) {
  if (!item.cells || item.cells.length === 0) {
    return null;
  }

  const hasHeader = item.rows > 1;

  return (
    <div className="content-table">
      <div className="table-wrapper">
        <table className="chapter-table">
          <tbody>
            {item.cells.map((row, rowIdx) => (
              <tr
                key={rowIdx}
                className={rowIdx === 0 && hasHeader ? "table-header-row" : ""}
              >
                {row.map((cell, cellIdx) => {
                  // Skip merged cells
                  if (
                    cell.merged_from &&
                    (cell.merged_from[0] !== cell.row ||
                      cell.merged_from[1] !== cell.col)
                  ) {
                    return null;
                  }

                  const CellTag = rowIdx === 0 && hasHeader ? "th" : "td";

                  return (
                    <CellTag
                      key={cellIdx}
                      className={cell.text ? "" : "empty-cell"}
                    >
                      {cell.paragraphs && cell.paragraphs.length > 0
                        ? cell.paragraphs.map((para, paraIdx) => (
                            <div key={paraIdx} className="table-cell-paragraph">
                              {para.runs && para.runs.length > 0
                                ? para.runs.map((run, runIdx) => {
                                    let className = "";
                                    if (run.bold) className += " bold";
                                    if (run.italic) className += " italic";
                                    if (run.underline)
                                      className += " underline";

                                    return (
                                      <span
                                        key={runIdx}
                                        className={className.trim()}
                                      >
                                        {run.text}
                                      </span>
                                    );
                                  })
                                : para.text}
                            </div>
                          ))
                        : cell.text}
                    </CellTag>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {item.expanded && (
        <p className="table-note">
          <em>
            Note: This table was automatically expanded from{" "}
            {item.original_rows} original row(s)
          </em>
        </p>
      )}
    </div>
  );
}

export default ChapterView;
