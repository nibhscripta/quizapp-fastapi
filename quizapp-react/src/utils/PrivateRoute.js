import { Navigate } from "react-router-dom";

const PrivateRoute = ({ children }) => {
  let authToken = localStorage.getItem("authToken");
  return authToken ? children : <Navigate to="/login" />;
};

export default PrivateRoute;
