import { useParams } from "react-router-dom";

const QuizPage = () => {
  const { id } = useParams();
  console.log(id);
  return <div>QuizPage</div>;
};

export default QuizPage;
