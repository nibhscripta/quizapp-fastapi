import { Link } from "react-router-dom";

import DeleteBtn from "./DeleteBtn";

const QuizLink = ({ quiz, deleteQuizState }) => {
  return (
    <div className="quiz-link">
      <Link
        to={{
          pathname: `/q/${quiz.id}`,
          state: { quiz: quiz },
        }}
      >
        <h1>{quiz.title}</h1>
        <p>{quiz.content}</p>
        {/* <p className="public">{quiz.public ? "Public" : "Private"}</p>
        <p>{quiz.created_at.substring(0, [10])}</p>
        <p>Due:</p>
        <p>{quiz.due ? quiz.due.substring(0, [10]) : "None"}</p> */}
      </Link>
      <DeleteBtn quizId={quiz.id} deleteQuizState={deleteQuizState} />
    </div>
  );
};

export default QuizLink;
