import fetchQuiz from "./FetchQuiz";
import QuizInfo from "./QuizInfo";
import "./quiz.css";

import { useParams, Link } from "react-router-dom";
import { useState, useEffect } from "react";

const QuizPage = () => {
  const { id } = useParams();

  const [quiz, setQuiz] = useState();

  useEffect(() => {
    const getQuiz = async () => {
      const apiRes = await fetchQuiz(id);
      setQuiz(apiRes);
    };

    getQuiz();
  }, []);

  return (
    <div>
      <div className="quiz-info">
        <Link to="/q">Back</Link>
        {quiz && <QuizInfo quiz={quiz} setQuiz={setQuiz} />}
      </div>
    </div>
  );
};

export default QuizPage;
