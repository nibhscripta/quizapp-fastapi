import { Link } from "react-router-dom";

const LoginForm = ({ onSubmit }) => {
  return (
    <div className="login-page-container">
      <form onSubmit={(e) => onSubmit(e)}>
        <Link to="/">Home</Link>
        <input type="text" name="username" placeholder="Username" />
        <input type="password" name="password" placeholder="Password" />
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default LoginForm;
