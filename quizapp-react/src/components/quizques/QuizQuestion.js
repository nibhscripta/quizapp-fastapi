import DeleteQuestionBtn from "./DeleteQuestionBtn";

import fetchAnswerList from "../quizans/FetchAnswerList";
import QuizAnswer from "../quizans/QuizAnswer";

import { useState, useEffect } from "react";

export const QuizQuestion = ({
  question,
  deleteQuestionState,
  updateQuestionState,
}) => {
  const submitQuestion = (e) => {
    e.preventDefault();
    const newQuestion = e.target.question.value;
    updateQuestionState(question.id, newQuestion);
  };

  const [asnwerList, setAnswerList] = useState([]);

  useEffect(() => {
    const getAnswerList = async () => {
      const apiRes = await fetchAnswerList(question.id);
      setAnswerList(apiRes);
    };

    getAnswerList();
  }, [question]);

  return (
    <div className="question">
      <h1>Question:</h1>
      <form onSubmit={(e) => submitQuestion(e)}>
        <input type="text" name="question" defaultValue={question.question} />
        <input type="submit" value="Save Question" />
      </form>
      <DeleteQuestionBtn
        deleteQuestionState={deleteQuestionState}
        id={question.id}
      />
      <h2>Answers:</h2>
      {asnwerList.map((answer) => (
        <QuizAnswer key={answer.id} answer={answer} />
      ))}
    </div>
  );
};
