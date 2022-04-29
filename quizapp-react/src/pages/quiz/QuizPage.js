import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import QuizCard from "./components/QuizCard";
import Question from "./components/Question";

const QuizPage = ({ apiUrl }) => {
  const { id } = useParams();

  const authToken = JSON.parse(localStorage.getItem("authorization"));

  const [quiz, setQuiz] = useState();

  const fetchQuiz = async () => {
    let myHeaders = new Headers();
    myHeaders.append("Authorization", authToken);

    let requestOptions = {
      method: "GET",
      headers: myHeaders,
      redirect: "follow",
    };

    const res = await fetch(`${apiUrl}/q/${id}`, requestOptions);
    const data = res.json();
    return data;
  };

  useEffect(() => {
    const getQuiz = async () => {
      const quizFromApi = await fetchQuiz();
      setQuiz(quizFromApi);
    };

    getQuiz();
  }, []);

  return (
    <div>
      {quiz && <QuizCard quiz={quiz} />}
      <Question apiUrl={apiUrl} id={id} authToken={authToken} />
    </div>
  );
};

export default QuizPage;
