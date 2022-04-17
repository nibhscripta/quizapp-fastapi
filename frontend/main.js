// remove noscript warning
document.getElementById("noscript").remove();
// render home form
const app = document.getElementById("app");
const homeFormDiv = `
    
`;
app.insertAdjacentHTML("afterend", homeFormDiv);
// quiz form submit handling
const quizForm = document.getElementById("start-quiz-form");
quizForm.onsubmit = (e) => {
  e.preventDefault();
  const quizID = e.target.quiz_id.value;
};
