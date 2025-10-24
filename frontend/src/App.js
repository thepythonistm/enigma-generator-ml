import './App.css';
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Generate from './Components/Generate/Generate';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Generate />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
