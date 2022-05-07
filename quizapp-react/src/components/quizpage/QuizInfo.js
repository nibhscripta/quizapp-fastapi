import UpdateQuiz from "./UpdateQuiz";

const QuizInfo = ({ quiz, setQuiz }) => {
  return (
    <div>
      <UpdateQuiz quiz={quiz} setQuiz={setQuiz} />
      {/* <p>{quiz.created_at.substring(0, [10])}</p>
      <p>{quiz.due ? quiz.due.substring(0, [10]) : "None"}</p> */}
    </div>
  );
};

export default QuizInfo;
