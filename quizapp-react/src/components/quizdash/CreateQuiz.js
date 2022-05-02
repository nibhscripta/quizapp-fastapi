const CreateQuiz = ({ toggleForm }) => {
  const newQuiz = (e) => {
    e.preventDefault();
    const t = e.target;
    const title = t.title.value;
    const content = t.content.value;
    const quizPublic = t.public.checked;
    console.log(title, content, quizPublic);
    toggleForm();
  };

  return (
    <form onSubmit={(e) => newQuiz(e)}>
      <h1>New Quiz</h1>
      <input type="text" name="title" placeholder="Title" />
      <input type="text" name="content" placeholder="Content" />
      <label htmlFor="public">Public</label>
      <input type="checkbox" name="public" id="public" value="public" />
      <input type="submit" value="Create" />
    </form>
  );
};

export default CreateQuiz;
