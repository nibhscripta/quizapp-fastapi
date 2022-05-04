import DeleteQuestionBtn from "./DeleteQuestionBtn";

import fetchAnswerList from "../quizans/FetchAnswerList";
import QuizAnswer from "../quizans/QuizAnswer";
import CreateAnswer from "../quizans/CreateAnswer";
import postAnswer from "../quizans/PostAnswer";
import putAnswer from "../quizans/PutAnswer";

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

  const [answerList, setAnswerList] = useState([]);

  useEffect(() => {
    const getAnswerList = async () => {
      const apiRes = await fetchAnswerList(question.id);
      setAnswerList(apiRes);
    };

    getAnswerList();
  }, [question]);

  const [answerForm, toggleAnswerForm] = useState(false);

  const addAnswer = (answer, correct) => {
    const createAnswer = async () => {
      const apiRes = await postAnswer(answer, correct, question.id);
      setAnswerList([...answerList, apiRes]);
    };

    createAnswer();
    toggleAnswerForm();
  };

  const updateAnswerState = (updatedAnswer, updatedCorrect, answerId) => {
    const updateAnswer = async () => {
      const apiRes = await putAnswer(updatedAnswer, updatedCorrect, answerId);

      setAnswerList(
        answerList.map((answer) =>
          answer.id === answerId ? { ...apiRes } : answer
        )
      );
    };

    updateAnswer();
  };

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
      {!answerForm ? (
        <button onClick={toggleAnswerForm}>Create Answer</button>
      ) : (
        <CreateAnswer addAnswer={addAnswer} />
      )}
      <h2>Answers:</h2>
      {answerList.map((answer) => (
        <QuizAnswer
          key={answer.id}
          answer={answer}
          updateAnswerState={updateAnswerState}
        />
      ))}
    </div>
  );
};
