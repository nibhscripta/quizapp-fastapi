import fetchQuiz from "./FetchQuiz";
import QuizInfo from "./QuizInfo";

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
      <Link to="/q">Back</Link>
      {quiz && <QuizInfo quiz={quiz} />}
    </div>
  );
};

export default QuizPage;
