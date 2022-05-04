import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

import fetchAssessment from "./FetchAssessment";

const Assessment = () => {
  const { id } = useParams();

  const [assessment, setAssessment] = useState({});

  useEffect(() => {
    const getAssessment = async () => {
      const apiRes = await fetchAssessment(id);
      setAssessment(apiRes);
    };

    getAssessment();
  }, [id]);

  return (
    <div>
      <h1>{assessment.title}</h1>
      <h3>{assessment.content}</h3>
      <p>{assessment.due ? assessment.due.substring(0, [10]) : "None"}</p>
    </div>
  );
};

export default Assessment;
