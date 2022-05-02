import fetchQuiz from "./FetchQuiz";
import QuizInfo from "./QuizInfo";
import fetchQuestionList from "./FetchQuestionList";
import CreateQuestion from "./CreateQuestion";
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

  const addQuestion = (newQuestion) => {
    setQuestionList([...questionList, newQuestion]);
  };

  const [questionForm, toggleQuestionForm] = useState(false);

  return (
    <div>
      <div className="quiz-info">
        <Link to="/q">Back</Link>
        {quiz && <QuizInfo quiz={quiz} setQuiz={setQuiz} />}
      </div>
      {questionForm ? (
        <CreateQuestion
          addQuestion={addQuestion}
          toggleQuestionForm={toggleQuestionForm}
          id={id}
        />
      ) : (
        <button onClick={toggleQuestionForm}>Create Question</button>
      )}
      {questionList.map((question) => (
        <QuizQuestion key={question.id} question={question} />
      ))}
    </div>
  );
};

export default QuizPage;
