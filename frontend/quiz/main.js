// remove noscript warning
document.getElementById("noscript").remove();
// render quiz page
const apiUrl = "http://127.0.0.1:8000/";
let access_token = localStorage.getItem("access_token");
if (!access_token) {
  window.location.replace(window.location.href.replace("quiz", "login"));
}
let token = "Bearer " + access_token;
const axiosConfig = {
  method: "get",
  url: "/quiz",
  baseURL: apiUrl,
  headers: {
    Authorization: token,
  },
};
axios(axiosConfig)
  .then((response) => {
    let data = JSON.stringify(response.data);
    data = JSON.parse(data);
    data.forEach((quiz) => {
      const quizLink = document.createElement("a");
      quizLink.text = quiz["title"];
      quizLink.setAttribute("id", quiz["id"]);
      quizLink.style.cssText = "cursor:pointer;";
      quizLink.addEventListener("click", renderQuiz(quiz["id"]));
      document.getElementById("quiz-list").appendChild(quizLink);
    });
  })
  .catch((error) => {
    const errorData = error;
    console.log(errorData);
  });
// toggle add quiz form
const quizForm = document.getElementById("add-quiz-form");
const addBtn = document.getElementById("add-btn");
const quizListDiv = document.getElementById("quiz-list");
const quizListHead = document.getElementById("quiz-list-head");
addBtn.onclick = () => {
  if (quizForm.classList.contains("none")) {
    quizForm.classList.remove("none");
    quizListDiv.classList.add("none");
    quizListHead.classList.add("none");
  } else if (!quizForm.classList.contains("none")) {
    quizForm.classList.add("none");
    quizListDiv.classList.remove("none");
    quizListHead.classList.remove("none");
  }
};
// create quiz
quizForm.onsubmit = (e) => {
  e.preventDefault();
  const quizTitle = e.target.quiz_name.value;
  const quizContent = e.target.quiz_content.value;
  quizForm.classList.add("none");
  quizListDiv.classList.remove("none");
  quizListHead.classList.remove("none");
};
// render quiz
let count = 0;
function renderQuiz(id) {
  console.log(id);
  count += 1;
  console.log(count);
}
