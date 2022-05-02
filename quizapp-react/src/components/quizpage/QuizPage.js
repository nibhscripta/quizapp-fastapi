import fetchQuiz from "./FetchQuiz";
import QuizInfo from "./QuizInfo";
import fetchQuestionList from "./FetchQuestionList";
import "./quiz.css";

import { QuizQuestion } from "../quizques/QuizQuestion";

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
  }, [id]);

  const [questionList, setQuestionList] = useState([]);

  useEffect(() => {
    const getQuestionList = async () => {
      const apiRes = await fetchQuestionList(id);
      setQuestionList(apiRes);
    };

    getQuestionList();
  }, [id]);

  return (
    <div>
      <div className="quiz-info">
        <Link to="/q">Back</Link>
        {quiz && <QuizInfo quiz={quiz} setQuiz={setQuiz} />}
        {questionList.map((question) => (
          <QuizQuestion key={question.id} question={question} />
        ))}
      </div>
    </div>
  );
};

export default QuizPage;
