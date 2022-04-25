import Login from "./pages/login/Login";
import Home from "./pages/home/Home";
import Quiz from "./pages/quiz/Quiz";
import QuizPage from "./pages/quiz/QuizPage";

import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

function App() {
  const apiUrl = "http://127.0.0.1:8000";

  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" exact element={<Home />} />
          <Route path="/login" exact element={<Login apiUrl={apiUrl} />} />
          <Route path="/quiz" exact element={<Quiz apiUrl={apiUrl} />} />
          <Route path="/quiz/:id" element={<QuizPage />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
