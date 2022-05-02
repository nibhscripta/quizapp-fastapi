import apiUrl from "../../utils/ApiUrl";

const authToken = JSON.parse(localStorage.getItem("authToken"));

const putQuiz = async (title, content, quizPublic, id) => {
  const raw = JSON.stringify({
    title: title,
    content: content,
    public: quizPublic,
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

  const res = await fetch(`${apiUrl}/q/${id}`, requestOptions);
  if (res.status === 200) {
    const data = res.json();
    return data;
  } else {
    console.log(res.status);
  }
};

export default putQuiz;
