import apiUrl from "../../utils/ApiUrl";

const authToken = JSON.parse(localStorage.getItem("authToken"));

const postQuestion = async (question, id) => {
  const raw = JSON.stringify({
    question: question,
  });

  let requestOptions = {
    method: "POST",
    redirect: "follow",
    headers: {
      Authorization: authToken,
      "Content-Type": "application/json",
    },
    body: raw,
  };

  const res = await fetch(`${apiUrl}/ques?quiz_id=${id}`, requestOptions);
  if (res.status === 200) {
    const data = res.json();
    return data;
  } else {
    console.log(res.status);
  }
};

export default postQuestion;
