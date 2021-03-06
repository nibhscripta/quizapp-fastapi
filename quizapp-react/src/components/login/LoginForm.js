import { Link } from "react-router-dom";

const LoginForm = ({ onSubmit, error, paramName }) => {
  document.querySelector("title").innerText = "Quiz! - Login";
  const defaultName = paramName;
  return (
    <div className="login-page-container">
      <form onSubmit={(e) => onSubmit(e)}>
        <Link to="/" tabIndex="-1">
          Home
        </Link>
        <input
          type="text"
          name="username"
          placeholder="Username"
          defaultValue={defaultName}
        />
        <input type="password" name="password" placeholder="Password" />
        {error && <p>an error occurred</p>}
        <button type="submit">Login</button>
        <Link to="/register">Create an account</Link>
      </form>
    </div>
  );
};

export default LoginForm;
