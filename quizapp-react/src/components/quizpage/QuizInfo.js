import React from "react";

const QuizInfo = ({ quiz }) => {
  const isPublic = quiz.public;
  return (
    <div>
      <form>
        <label htmlFor="title">Title</label>
        <input type="text" id="title" name="title" value={quiz.title} />
        <label htmlFor="content">Content</label>
        <input type="text" id="content" name="content" value={quiz.content} />
        <label htmlFor="public">Public</label>
        <input type="checkbox" id="public" checked />
      </form>
      <p>{quiz.created_at.substring(0, [10])}</p>
      <p>{quiz.due ? quiz.due.substring(0, [10]) : "None"}</p>
    </div>
  );
};

export default QuizInfo;
