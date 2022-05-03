import apiUrl from "../../utils/ApiUrl";

const authToken = JSON.parse(localStorage.getItem("authToken"));

const putQuestion = async (question, id) => {
  const raw = JSON.stringify({
    question: question,
  });

  let requestOptions = {
    method: "PUT",
    redirect: "follow",
    headers: {
      Authorization: authToken,
      "Content-Type": "application/json",
    },
    body: raw,
  };

  const res = await fetch(`${apiUrl}/ques/${id}`, requestOptions);
  if (res.status === 200) {
    const data = res.json();
    return data;
  } else {
    console.log(res.status);
  }
};

export default putQuestion;
