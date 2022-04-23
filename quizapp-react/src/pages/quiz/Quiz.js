import { Link } from "react-router-dom";
import { useState, useEffect } from "react";

import "./quiz.css";

const Quiz = ({ apiUrl }) => {
  const authToken = JSON.parse(localStorage.getItem("authorization"));
  console.log(authToken);

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
        <h2 key={quiz.id}>{quiz.title}</h2>
      ))}
    </div>
  );
};

export default Quiz;
