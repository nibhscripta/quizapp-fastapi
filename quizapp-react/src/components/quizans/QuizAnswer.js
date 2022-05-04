const QuizAnswer = ({ answer, updateAnswerState }) => {
  const answerId = answer.id;

  const onSubmitAnswer = (e) => {
    e.preventDefault();
    const t = e.target;
    const answer = t.answer.value;
    const correct = t.correct.checked;
    updateAnswerState(answer, correct, answerId);
  };

  return (
    <form onSubmit={(e) => onSubmitAnswer(e)}>
      <input type="text" name="answer" defaultValue={answer.answer} />
      <label htmlFor={`correct${answer.id}`}>Correct</label>
      <input
        type="checkbox"
        name="correct"
        id={`correct${answer.id}`}
        defaultChecked={answer.correct}
      />
      <input type="submit" value="Save Answer" />
    </form>
  );
};

export default QuizAnswer;
