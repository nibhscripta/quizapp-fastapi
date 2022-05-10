import { Navigate, useNavigate } from "react-router-dom";
import { useState } from "react";

import FetchAuthToken from "./FetchAuthToken";
import LoginForm from "./LoginForm";
import "./login.css";

const Login = () => {
  let authToken = localStorage.getItem("authToken");

  const navigate = useNavigate();

  const [loginError, setLoginError] = useState(false);

  const login = async (e) => {
    e.preventDefault();
    const username = e.target.username.value;
    const password = e.target.password.value;
    FetchAuthToken(username, password).then((res) => {
      if (res) {
        setLoginError(true);
      } else {
        navigate("/q");
      }
    });
    e.target.password.value = "";
  };

  return authToken ? (
    <Navigate to="/q" />
  ) : (
    <LoginForm onSubmit={login} error={loginError} />
  );
};

export default Login;
