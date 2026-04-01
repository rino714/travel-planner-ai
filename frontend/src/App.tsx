import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import PlanPage from "./pages/PlanPage";

function App() {
  return (
    <BrowserRouter>
      <div style={{ maxWidth: 800, margin: "0 auto", padding: "20px" }}>
        <h1 style={{ textAlign: "center", marginBottom: 32 }}>
          🗺️ Travel Planner AI
        </h1>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/plan/:tripId" element={<PlanPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
