import { Link } from "react-router-dom";

const LoginForm = ({ login }) => {
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

export default LoginForm;
