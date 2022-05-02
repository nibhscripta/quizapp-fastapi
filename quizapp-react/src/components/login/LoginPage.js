import { Navigate } from "react-router-dom";

import FetchAuthToken from "./FetchAuthToken";
import LoginForm from "./LoginForm";

const Login = () => {
  const login = async (e) => {
    e.preventDefault();
    const username = e.target.username.value;
    const password = e.target.password.value;
    await FetchAuthToken(username, password);
    e.target.password.value = "";
  };

  let authToken = localStorage.getItem("authToken");

  if (authToken) {
    return <Navigate to="/q" />;
  } else {
    return <LoginForm onSubmit={login} />;
  }
};

export default Login;
