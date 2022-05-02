import apiUrl from "../../utils/ApiUrl";

const authToken = JSON.parse(localStorage.getItem("authToken"));

const postQuiz = async (title, content, quizPublic) => {
  const raw = JSON.stringify({
    title: title,
    content: content,
    public: quizPublic,
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

  const res = await fetch(`${apiUrl}/q`, requestOptions);
  const data = res.json();
  return data;
};

export default postQuiz;
