import fetchQuiz from "./FetchQuiz";
import QuizInfo from "./QuizInfo";
import fetchQuestionList from "./FetchQuestionList";
import CreateQuestion from "./CreateQuestion";
import "./quiz.css";

import putQuestion from "../quizques/PutQuestion";
import deleteQuestion from "../quizques/DeleteQuestion";
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

  const deleteQuestionState = (questionId) => {
    deleteQuestion(questionId);
    setQuestionList(
      questionList.filter((question) => question.id !== questionId)
    );
  };

  const updateQuestionState = (questionId, updatedQuestion) => {
    const updateQuestion = async () => {
      const apiRes = await putQuestion(updatedQuestion, questionId);

      setQuestionList(
        questionList.map((question) =>
          question.id === questionId ? { ...apiRes } : question
        )
      );
    };

    updateQuestion();
  };

  if (quiz) {
    document.querySelector("title").innerText = `Quiz! - ${quiz.title}`;
  }

  return (
    <div className="quiz-page-container">
      <div className="quiz-info">
        <Link to="/q" tabIndex="-1">
          Back
        </Link>
        {quiz && <QuizInfo quiz={quiz} setQuiz={setQuiz} />}
      </div>
      {questionForm ? (
        <CreateQuestion
          addQuestion={addQuestion}
          toggleQuestionForm={toggleQuestionForm}
          id={id}
        />
      ) : (
        <button onClick={toggleQuestionForm} className="toggle-question">
          Create Question
        </button>
      )}
      <div className="question-list">
        {questionList.map((question) => (
          <QuizQuestion
            key={question.id}
            question={question}
            deleteQuestionState={deleteQuestionState}
            updateQuestionState={updateQuestionState}
          />
        ))}
      </div>
    </div>
  );
};

export default QuizPage;
