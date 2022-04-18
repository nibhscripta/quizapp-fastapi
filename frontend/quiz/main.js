// remove noscript warning
document.getElementById("noscript").remove();
// render quiz page

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
