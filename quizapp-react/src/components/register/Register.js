import RegisterForm from "./RegisterForm";

import { Navigate } from "react-router-dom";

const Register = () => {
  let authToken = localStorage.getItem("authToken");
  return authToken ? <Navigate to="/q" /> : <RegisterForm />;
};

export default Register;
