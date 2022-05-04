import { Navigate, useNavigate } from "react-router-dom";

import FetchAuthToken from "./FetchAuthToken";
import LoginForm from "./LoginForm";

const Login = () => {
  let authToken = localStorage.getItem("authToken");

  const navigate = useNavigate();

  const login = async (e) => {
    e.preventDefault();
    const username = e.target.username.value;
    const password = e.target.password.value;
    await FetchAuthToken(username, password);
    e.target.password.value = "";
    authToken = localStorage.getItem("authToken");
    if (authToken) {
      navigate("/q");
    }
  };

  return authToken ? <Navigate to="/q" /> : <LoginForm onSubmit={login} />;
};

export default Login;
