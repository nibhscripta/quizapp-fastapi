import putQuiz from "./PutQuiz";

const UpdateQuiz = ({ quiz, setQuiz }) => {
  const updateQuiz = (e) => {
    e.preventDefault();
    const t = e.target;
    const title = t.title.value;
    const content = t.content.value;
    const quizPublic = t.public.checked;
    putQuiz(title, content, quizPublic, quiz.id).then((res) => setQuiz(res));
  };
  return (
    <form onSubmit={(e) => updateQuiz(e)}>
      <label htmlFor="title">Title</label>
      <input type="text" id="title" name="title" defaultValue={quiz.title} />
      <label htmlFor="content">Content</label>
      <input
        type="text"
        id="content"
        name="content"
        defaultValue={quiz.content}
      />
      <label htmlFor="public">Public</label>
      <input type="checkbox" id="public" defaultChecked={quiz.public} />
      <input type="submit" value="Save" />
    </form>
  );
};

export default UpdateQuiz;
