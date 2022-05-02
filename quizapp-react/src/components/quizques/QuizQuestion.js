export const QuizQuestion = ({ question }) => {
  return (
    <div>
      <form>
        <input type="text" name="question" defaultValue={question.question} />
        <input type="submit" value="Save Question" />
      </form>
    </div>
  );
};
