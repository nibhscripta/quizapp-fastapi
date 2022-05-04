import apiUrl from "../../utils/ApiUrl";

const authToken = JSON.parse(localStorage.getItem("authToken"));

const postAnswer = async (answer, correct, id) => {
  const raw = JSON.stringify({
    answer: answer,
    correct: correct,
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

  const res = await fetch(`${apiUrl}/ans?qid=${id}`, requestOptions);
  if (res.status === 200) {
    const data = res.json();
    return data;
  } else {
    console.log(res.status);
  }
};

export default postAnswer;
