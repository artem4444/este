// GridLayout.js

import React, { useState, useEffect } from "react";
import { Responsive, WidthProvider } from "react-grid-layout";
import "react-grid-layout/css/styles.css";
import "react-resizable/css/styles.css";
import "./GridLayout.css";

import Chatbot from "react-chatbot-kit";
import "react-chatbot-kit/build/main.css";
import config from "./react-chatbot/Config";
import MessageParser from "./react-chatbot/MessageParser";
import ActionProvider from "./react-chatbot/ActionProvider";

const ResponsiveGridLayout = WidthProvider(Responsive);

const GridLayout = () => {
  const [dimensions, setDimensions] = useState({
    height: window.innerHeight,
    width: window.innerWidth,
  });

  useEffect(() => {
    const handleResize = () => {
      setDimensions({
        height: window.innerHeight,
        width: window.innerWidth,
      });
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const totalRows = 12;
  const rowHeight = Math.floor(dimensions.height / totalRows);

  const layouts = {
    lg: [
      { i: "navbar", x: 0, y: 0, w: 12, h: 1, static: true },
      { i: "sidebar", x: 0, y: 1, w: 3, h: 10, static: false },
      { i: "content", x: 3, y: 1, w: 6, h: 10, static: false },
      { i: "chatbot", x: 9, y: 1, w: 3, h: 10, static: false },
      { i: "footer", x: 0, y: totalRows - 1, w: 12, h: 1, static: true },
    ],
    md: [
      { i: "navbar", x: 0, y: 0, w: 12, h: 1, static: true },
      { i: "sidebar", x: 0, y: 1, w: 3, h: 10, static: true },
      { i: "content", x: 3, y: 1, w: 6, h: 10, static: false },
      { i: "chatbot", x: 9, y: 1, w: 3, h: 10, static: false },
      { i: "footer", x: 0, y: totalRows - 1, w: 12, h: 1, static: true },
    ],
    sm: [
      { i: "navbar", x: 0, y: 0, w: 12, h: 1, static: true },
      { i: "sidebar", x: 0, y: 1, w: 3, h: 10, static: true },
      { i: "content", x: 3, y: 1, w: 6, h: 10, static: false },
      { i: "chatbot", x: 9, y: 1, w: 3, h: 10, static: false },
      { i: "footer", x: 0, y: totalRows - 1, w: 12, h: 1, static: true },
    ],
  };

  const onLayoutChange = (layout, layouts) => {
    console.log("Layout changed:", layout);
  };

  return (
    <div className="layout" style={{ height: "100vh", width: "100vw", overflow: "hidden" }}>
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
        {/* Navbar */}
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

        {/* Sidebar */}
        <div key="sidebar" className="box sidebar">Sidebar</div>

        {/* Content with Responsive Video */}
        <div key="content" className="box content bg-red-200 p-2">
          <div className="relative w-full pb-[56.25%] h-0">
            <iframe
              className="absolute top-0 left-0 w-full h-full rounded-2xl shadow-lg"
              src="https://www.youtube.com/embed/dQw4w9WgXcQ"
              title="Stream"
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            ></iframe>
          </div>
        </div>


        {/* Chatbot Container */}
        <div key="chatbot" className="box chatbot p-2 border-2 border-gray-300">
          <div className="h-full w-full sm:max-w-xs md:max-w-md lg:max-w-lg xl:max-w-xl rounded-2xl shadow-lg overflow-hidden">
            <Chatbot 
              config={config} 
              messageParser={MessageParser} 
              actionProvider={ActionProvider} 
            />
          </div>
        </div>



        {/* Footer */}
        <div key="footer" className="box footer">Footer</div>
      </ResponsiveGridLayout>
    </div>
  );
};

export default GridLayout;
