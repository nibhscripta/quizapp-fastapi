import { Link, useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();
  const ToAssessment = (e) => {
    e.preventDefault();
    const quizCode = e.target.quiz_code.value;
    const redirect = `/a/${quizCode}`;
    try {
      navigate(redirect);
    } catch (error) {
      console.log(error);
    }
  };
  return (
    <div className="home-page-container">
      <h1>Home</h1>
      <form onSubmit={(e) => ToAssessment(e)}>
        <input type="text" name="quiz_code" placeholder="Quiz code" />
      </form>
      <Link to="/login">Login</Link>
    </div>
  );
};

export default Home;
