import DeleteQuestionBtn from "./DeleteQuestionBtn";

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

  return (
    <div>
      <form onSubmit={(e) => submitQuestion(e)}>
        <input type="text" name="question" defaultValue={question.question} />
        <input type="submit" value="Save Question" />
      </form>
      <DeleteQuestionBtn
        deleteQuestionState={deleteQuestionState}
        id={question.id}
      />
    </div>
  );
};
