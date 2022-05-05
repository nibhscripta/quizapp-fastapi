import "./quiz.css";
import fetchQuizList from "./FetchQuizList";
import QuizLink from "./QuizLink";
import CreateQuiz from "./CreateQuiz";
import Logout from "../login/Logout";

import { useState, useEffect } from "react";

const QuizDash = () => {
  document.querySelector("title").innerText = "Quiz! - Dashboard";

  const [quizList, setQuizList] = useState([]);

  useEffect(() => {
    const getQuizList = async () => {
      const apiRes = await fetchQuizList();
      setQuizList(apiRes);
    };

    getQuizList();
  }, []);

  const [quizForm, toggleQuizForm] = useState(false);

  const addQuiz = (newQuiz) => {
    setQuizList([...quizList, newQuiz]);
  };

  const deleteQuizState = (id) => {
    setQuizList(quizList.filter((quiz) => quiz.id !== id));
  };

  return (
    <div className="quiz-container">
      <Logout />
      <div className="create-quiz-form">
        {quizForm ? (
          <CreateQuiz toggleForm={toggleQuizForm} addQuiz={addQuiz} />
        ) : (
          <button onClick={toggleQuizForm}>Create Quiz</button>
        )}
      </div>
      <div className="quiz-list">
        {quizList.map((quiz) => (
          <QuizLink
            key={quiz.id}
            quiz={quiz}
            deleteQuizState={deleteQuizState}
          />
        ))}
      </div>
    </div>
  );
};

export default QuizDash;
