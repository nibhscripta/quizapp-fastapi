import { Link } from "react-router-dom";

import "./home.css";

const Home = () => {
  return (
    <div className="home-page-container">
      <h1>Home</h1>
      <form>
        <input type="text" placeholder="Quiz code" />
      </form>
      <Link to="/login">Login</Link>
    </div>
  );
};

export default Home;
