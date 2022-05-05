import { useNavigate } from "react-router-dom";

const Logout = () => {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("authToken");
    navigate("/login");
  };

  return (
    <button onClick={logout} tabIndex="-1" className="logout-btn">
      Logout
    </button>
  );
};

export default Logout;
