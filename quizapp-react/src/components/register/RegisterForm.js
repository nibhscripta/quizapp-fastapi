import { useNavigate } from "react-router-dom";
import postRegister from "./PostRegister";

const RegisterForm = () => {
  const navigate = useNavigate();
  const register = async (e) => {
    e.preventDefault();

    const email = e.target.email.value;
    const password = e.target.password.value;
    await postRegister(email, password);
    navigate(`/login?username=${email}`);
  };
  return (
    <form onSubmit={(e) => register(e)}>
      <input type="text" name="email" placeholder="Email" />
      <input type="password" name="password" placeholder="Password" />
      <button type="submit">Register</button>
    </form>
  );
};

export default RegisterForm;
