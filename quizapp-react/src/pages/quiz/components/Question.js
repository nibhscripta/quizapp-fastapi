import { useState, useEffect } from "react";
import Anwer from "./Anwer";

const Question = ({ id, apiUrl, authToken }) => {
  const [questions, setQuestions] = useState();

  const fetchQuestions = async () => {
    let myHeaders = new Headers();
    myHeaders.append("Authorization", authToken);

    let requestOptions = {
      method: "GET",
      headers: myHeaders,
      redirect: "follow",
    };

    const res = await fetch(`${apiUrl}/quiz/${id}/question`, requestOptions);
    const data = res.json();
    return data;
  };

  useEffect(() => {
    const getQuestions = async () => {
      const questionsFromApi = await fetchQuestions();
      setQuestions(questionsFromApi);
    };

    getQuestions();
  }, []);

  return (
    <div>
      {questions &&
        questions.map((question) => (
          <div className="question" key={question.id}>
            <h3>{question.question}</h3>

            <Anwer
              qid={question.id}
              apiUrl={apiUrl}
              id={id}
              authToken={authToken}
            />
          </div>
        ))}
    </div>
  );
};

export default Question;
