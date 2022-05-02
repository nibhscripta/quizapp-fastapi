import "./quiz.css";
import fetchQuizList from "./FetchQuizList";
import QuizLink from "./QuizLink";
import CreateQuiz from "./CreateQuiz";

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

  const [quizForm, toggleQuizForm] = useState(false);

  return (
    <div className="quiz-container">
      <h1>Quizzes</h1>
      {quizForm ? (
        <CreateQuiz toggleForm={toggleQuizForm} />
      ) : (
        <button onClick={toggleQuizForm}>Create Quiz</button>
      )}

      {quizList.map((quiz) => (
        <QuizLink key={quiz.id} quiz={quiz} />
      ))}
    </div>
  );
};

export default QuizPage;
