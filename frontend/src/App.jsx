import { Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Stream from "./pages/Stream";
import Upload from "./pages/Upload";

import "./App.css";

function App() {
  return (
    <div className="app">
      <Routes>
        {/* Redirect root to login */}
        <Route path="/" element={<Navigate to="/login" replace />} />

        {/* Pages */}
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard/:user" element={<Dashboard />} />
        <Route path="/upload/:user" element={<Upload />} />
        <Route path="/stream/:id" element={<Stream />} />

        {/* 404 */}
        <Route path="*" element={<h1>404 - Page Not Found</h1>} />
      </Routes>
    </div>
  );
}

export default App;