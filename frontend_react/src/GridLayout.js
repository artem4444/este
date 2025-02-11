import React, { useState, useEffect } from "react";
import { Responsive, WidthProvider } from "react-grid-layout";
import "react-grid-layout/css/styles.css";
import "react-resizable/css/styles.css";
import "./GridLayout.css";

const ResponsiveGridLayout = WidthProvider(Responsive);

const GridLayout = () => {
  const [dimensions, setDimensions] = useState({ 
    height: window.innerHeight,
    width: window.innerWidth 
  });

  useEffect(() => {
    function handleResize() {
      setDimensions({
        height: window.innerHeight,
        width: window.innerWidth
      });
    }

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Calculate total rows needed (12 in this case)
  const totalRows = 12;
  const rowHeight = Math.floor(dimensions.height / totalRows);

  const layouts = {
    lg: [
      { i: "navbar", x: 0, y: 0, w: 12, h: 1, static: true },
      { i: "sidebar", x: 0, y: 1, w: 3, h: 10, static: false },
      { i: "content", x: 3, y: 1, w: 6, h: 10, static: false },
      { i: "widgets", x: 9, y: 1, w: 3, h: 10, static: false },
      { i: "footer", x: 0, y: totalRows - 1, w: 12, h: 1, static: true }, // Position at bottom
    ],
    md: [
      { i: "navbar", x: 0, y: 0, w: 12, h: 1, static: true },
      { i: "sidebar", x: 0, y: 1, w: 3, h: 10, static: true },
      { i: "content", x: 3, y: 1, w: 6, h: 10, static: false },
      { i: "widgets", x: 9, y: 1, w: 3, h: 10, static: false },
      { i: "footer", x: 0, y: totalRows - 1, w: 12, h: 1, static: true },
    ],
    sm: [
      { i: "navbar", x: 0, y: 0, w: 12, h: 1, static: true },
      { i: "sidebar", x: 0, y: 1, w: 3, h: 10, static: true },
      { i: "content", x: 3, y: 1, w: 6, h: 10, static: false },
      { i: "widgets", x: 9, y: 1, w: 3, h: 10, static: false },
      { i: "footer", x: 0, y: totalRows - 1, w: 12, h: 1, static: true },
    ],
  };

  const onLayoutChange = (layout, layouts) => {
    // Optional: Handle layout changes
    console.log('Layout changed:', layout);
  };

  return (
    <div className="layout" style={{ height: '100vh', width: '100vw', overflow: 'hidden' }}>
      <ResponsiveGridLayout
        className="grid-container"
        layouts={layouts}
        breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480 }}
        cols={{ lg: 12, md: 12, sm: 12, xs: 12 }}
        rowHeight={rowHeight}
        width={dimensions.width}
        margin={[0, 0]}
        containerPadding={[0, 0]}
        isDraggable={true}
        isResizable={true}
        compactType={null}
        preventCollision={true}
        useCSSTransforms={true}
        verticalCompact={false}
        onLayoutChange={onLayoutChange}
      >
        <div key="navbar" className="box navbar"> 
          <div className="navbar-content">
            <div className="logo">Logo</div>
            <nav className="nav-links">
              <a href="/">Home</a>
              <a href="/about">About</a>
            </nav>
            <div className="user-section">
              <span>User Name</span>
            </div>
          </div>
        </div>


        <div key="sidebar" className="box sidebar">Sidebar</div>

        <div key="content" className="box content">
        
          {/* Video Streaming */}
          <div className="video-container">
            <iframe 
              src="https://www.youtube.com/embed/dQw4w9WgXcQ" 
              title="Stream" 
              frameBorder="0" 
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
              allowFullScreen
            ></iframe>
          </div>
        </div>

        <div key="widgets" className="box widgets">Widgets</div>
        <div key="footer" className="box footer">Footer</div>
      </ResponsiveGridLayout>
    </div>
  );
};

export default GridLayout;