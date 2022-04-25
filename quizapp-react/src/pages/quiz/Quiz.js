import { Link } from "react-router-dom";
import { useState, useEffect } from "react";

import "./quiz.css";
import QuizCard from "./components/QuizCard";

const Quiz = ({ apiUrl }) => {
  const authToken = JSON.parse(localStorage.getItem("authorization"));

  const [quizzes, setQuizzes] = useState([]);

  const fetchQuizzes = async () => {
    let myHeaders = new Headers();
    myHeaders.append("Authorization", authToken);

    let requestOptions = {
      method: "GET",
      headers: myHeaders,
      redirect: "follow",
    };

    const res = await fetch(`${apiUrl}/quiz`, requestOptions);
    const data = res.json();
    return data;
  };

  useEffect(() => {
    const getQuizzes = async () => {
      const quizzesFromApi = await fetchQuizzes();
      setQuizzes(quizzesFromApi);
    };

    getQuizzes();
  }, []);

  return (
    <div className="quiz-page-container">
      <Link to="/">home</Link>
      {quizzes.map((quiz) => (
        <Link to={`/quiz/${quiz.id}`} key={quiz.id} quiz={quiz}>
          <QuizCard quiz={quiz} />
        </Link>
      ))}
    </div>
  );
};

export default Quiz;
