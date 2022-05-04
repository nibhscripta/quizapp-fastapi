import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import Home from "./components/home/Home";
import Login from "./components/login/LoginPage";
import QuizDash from "./components/quizdash/QuizDashPage";
import QuizPage from "./components/quizpage/QuizPage";
import Assessment from "./components/assessment/Assessment";
import PrivateRoute from "./utils/PrivateRoute";

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" exact element={<Home />} />
          <Route path="/login" exact element={<Login />} />
          <Route
            path="/q"
            exact
            element={
              <PrivateRoute>
                <QuizDash />
              </PrivateRoute>
            }
          />
          <Route
            path="/q/:id"
            exact
            element={
              <PrivateRoute>
                <QuizPage />
              </PrivateRoute>
            }
          />
          <Route path="/a/:id" exact element={<Assessment />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
