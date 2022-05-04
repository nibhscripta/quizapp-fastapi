import apiUrl from "../../utils/ApiUrl";

const authToken = JSON.parse(localStorage.getItem("authToken"));

const putAnswer = async (answer, correct, id) => {
  const raw = JSON.stringify({
    answer: answer,
    correct: correct,
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

  const res = await fetch(`${apiUrl}/ans/${id}`, requestOptions);
  if (res.status === 200) {
    const data = res.json();
    return data;
  } else {
    console.log(res.status);
  }
};

export default putAnswer;
