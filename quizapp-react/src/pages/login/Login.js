import { Link } from "react-router-dom";

import "./login.css";

const Login = () => {
  const login = (e) => {
    e.preventDefault();
    const username = e.target.username.value;
    const password = e.target.password.value;
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
