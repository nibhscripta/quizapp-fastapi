const CreateAnswer = ({ addAnswer }) => {
  const newAnswer = (e) => {
    e.preventDefault();
    const answer = e.target.answer.value;
    const correct = e.target.correct.checked;
    addAnswer(answer, correct);
  };

  return (
    <form onSubmit={(e) => newAnswer(e)}>
      <h1>New Answer:</h1>
      <input type="text" name="answer" placeholder="Answer" />
      <label htmlFor="correct">Correct:</label>
      <input type="checkbox" name="correct" id="correct" />
      <input type="submit" value="Create" />
    </form>
  );
};

export default CreateAnswer;
