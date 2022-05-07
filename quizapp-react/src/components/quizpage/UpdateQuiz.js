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
    <div className="update-quiz-form">
      <form onSubmit={(e) => updateQuiz(e)}>
        <label htmlFor="title">Title:</label>
        <input type="text" id="title" name="title" defaultValue={quiz.title} />
        <label htmlFor="content">Content:</label>
        <input
          type="text"
          id="content"
          name="content"
          defaultValue={quiz.content}
        />
        <div className="quiz-public">
          <input
            type="checkbox"
            name="public"
            id="public"
            defaultChecked={quiz.public}
            value="public"
          />
          <label htmlFor="public">Public</label>
        </div>
        <button type="submit">Save</button>
      </form>
    </div>
  );
};

export default UpdateQuiz;
