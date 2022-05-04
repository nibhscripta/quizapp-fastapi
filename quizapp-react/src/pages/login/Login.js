import { useState } from "react";
import { Navigate } from "react-router-dom";

import "./login.css";
import LoginForm from "./LoginForm";

const Login = ({ apiUrl }) => {
  const [authenticated, setAuthenticated] = useState(false);

  const getJWT = async (username, passord, apiUrl) => {
    let loginHeaders = new Headers();
    let formdata = new FormData();
    formdata.append("username", username);
    formdata.append("password", passord);
    var requestOptions = {
      method: "POST",
      headers: loginHeaders,
      body: formdata,
      redirect: "follow",
    };
    const res = await fetch(`${apiUrl}/login`, requestOptions);
    if (res.status === 200) {
      const data = await res.json();
      const authToken = `${data.token_type} ${data.access_token}`;
      // localStorage.setItem("authorization", JSON.stringify(authToken));
    } else {
      console.log(res.status);
    }
  };

  const login = async (e) => {
    e.preventDefault();
    const username = e.target.username.value;
    const password = e.target.password.value;
    await getJWT(username, password, apiUrl);
    e.target.password.value = "";
  };

  return authenticated ? <Navigate to="/login" /> : <LoginForm login={login} />;
};

export default Login;
