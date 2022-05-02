import { Link } from "react-router-dom";

const QuizLink = ({ quiz }) => {
  const quizLink = `/q/${quiz.id}`;
  return (
    <Link to={quizLink}>
      <div className="quiz-link">
        <h1>{quiz.title}</h1>
        <p>{quiz.content}</p>
        <p>{quiz.public ? "Public" : "Private"}</p>
        <p>{quiz.created_at.substring(0, [10])}</p>
        <p>{quiz.due ? quiz.due.substring(0, [10]) : "None"}</p>
      </div>
    </Link>
  );
};

export default QuizLink;
