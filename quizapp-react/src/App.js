import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import Home from "./components/home/Home";
import Login from "./components/login/LoginPage";
import QuizPage from "./components/quizdash/QuizDashPage";
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
                <QuizPage />
              </PrivateRoute>
            }
          />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
