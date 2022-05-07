import postQuestion from "./PostQuestion";

const CreateQuestion = ({ toggleQuestionForm, addQuestion, id }) => {
  const newQuiz = (e) => {
    e.preventDefault();
    const question = e.target.question.value;
    postQuestion(question, id).then((question) => addQuestion(question));
    toggleQuestionForm();
  };

  return (
    <form onSubmit={(e) => newQuiz(e)} className="create-question">
      <input type="text" name="question" placeholder="New Question" />
      <button type="submit">Create</button>
    </form>
  );
};

export default CreateQuestion;
