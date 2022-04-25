const QuizCard = ({ quiz }) => {
  return (
    <div className="quiz-card">
      <h1>{quiz.title}</h1>
      <h2>{quiz.content}</h2>
      <span>{quiz.public ? "Public" : "Private"}</span>
      <span>{quiz.created_at.substring(0, [10])}</span>
    </div>
  );
};

export default QuizCard;
