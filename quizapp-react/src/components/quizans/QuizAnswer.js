const QuizAnswer = ({ answer }) => {
  return (
    <form>
      <input type="text" name="answer" defaultValue={answer.answer} />
      <label htmlFor={`correct${answer.id}`}>Correct</label>
      <input
        type="checkbox"
        id={`correct${answer.id}`}
        defaultChecked={answer.correct}
      />
      <input type="submit" value="Save Answer" />
    </form>
  );
};

export default QuizAnswer;
