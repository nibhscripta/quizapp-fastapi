import "./quiz.css";
import fetchQuizList from "./FetchQuizList";
import QuizLink from "./QuizLink";

import { useState, useEffect } from "react";

const QuizPage = () => {
  const [quizList, setQuizList] = useState([]);

  useEffect(() => {
    const getQuizList = async () => {
      const apiRes = await fetchQuizList();
      setQuizList(apiRes);
    };

    getQuizList();
  }, []);

  return (
    <div className="quiz-container">
      <h1>Quizzes</h1>
      {quizList.map((quiz) => (
        <QuizLink key={quiz.id} quiz={quiz} />
      ))}
    </div>
  );
};

export default QuizPage;
