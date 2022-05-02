import postQuestion from "./PostQuestion";

const CreateQuestion = ({ toggleQuestionForm, addQuestion, id }) => {
  const newQuiz = (e) => {
    e.preventDefault();
    const question = e.target.question.value;
    postQuestion(question, id).then((question) => addQuestion(question));
    toggleQuestionForm();
  };

  return (
    <form onSubmit={(e) => newQuiz(e)}>
      <h1>New Question</h1>
      <input type="text" name="question" placeholder="Question" />
      <input type="submit" value="Create" />
    </form>
  );
};

export default CreateQuestion;
