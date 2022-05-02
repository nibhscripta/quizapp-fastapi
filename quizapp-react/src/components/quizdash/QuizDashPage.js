import "./quiz.css";
import fetchQuizList from "./FetchQuizList";
import QuizLink from "./QuizLink";
import CreateQuiz from "./CreateQuiz";
import postQuiz from "./PostQuiz";

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

  const addQuiz = (newQuiz) => {
    setQuizList([...quizList, newQuiz]);
  };

  return (
    <div className="quiz-container">
      <h1>Quizzes</h1>
      {quizForm ? (
        <CreateQuiz toggleForm={toggleQuizForm} addQuiz={addQuiz} />
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
