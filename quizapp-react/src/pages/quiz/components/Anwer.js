import { useState, useEffect } from "react";

const Anwer = ({ id, apiUrl, authToken, qid }) => {
  const [answers, setAnswers] = useState();

  const fetchAnswers = async (qid) => {
    let myHeaders = new Headers();
    myHeaders.append("Authorization", authToken);

    let requestOptions = {
      method: "GET",
      headers: myHeaders,
      redirect: "follow",
    };

    const res = await fetch(
      `${apiUrl}/quiz/${id}/question/${qid}/answer`,
      requestOptions
    );
    const data = res.json();
    return data;
  };

  useEffect(() => {
    const getAnswers = async () => {
      const answersFromApi = await fetchAnswers(qid);
      setAnswers(answersFromApi);
    };

    getAnswers();
  }, []);
  return (
    <ul>
      {answers &&
        answers.map((answer) => (
          <li key={answer.id} className={answer.correct && "correct"}>
            {answer.answer}
          </li>
        ))}
    </ul>
  );
};

export default Anwer;
