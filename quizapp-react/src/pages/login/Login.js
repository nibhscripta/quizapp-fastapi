import { Link } from "react-router-dom";

import "./login.css";

const Login = ({ apiUrl }) => {
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
    const data = await res.json();
    const authToken = `${data.token_type} ${data.access_token}`;
    localStorage.setItem("authorization", JSON.stringify(authToken));
    console.log(JSON.parse(localStorage.getItem("authorization")));
  };

  const login = async (e) => {
    e.preventDefault();
    const username = e.target.username.value;
    const password = e.target.password.value;
    await getJWT(username, password, apiUrl);
    e.target.password.value = "";
  };

  return (
    <div className="login-page-container">
      <form onSubmit={(e) => login(e)}>
        <Link to="/">Home</Link>
        <input type="text" name="username" placeholder="Username" />
        <input type="password" name="password" placeholder="Password" />
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
