import DeleteQuestionBtn from "./DeleteQuestionBtn";

export const QuizQuestion = ({ question, deleteQuestionState }) => {
  return (
    <div>
      <form>
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
