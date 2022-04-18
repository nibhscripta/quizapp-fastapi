// remove noscript warning
document.getElementById("noscript").remove();
// sample data
const questions = [
  {
    id: 1,
    question: "What is a limit?",
  },
  {
    id: 2,
    question: "What is a derivative?",
  },
  {
    id: 3,
    question: "What is an integral?",
  },
];
const answers = [
  [
    {
      id: 1,
      answer: "A point on a curve.",
    },
    {
      id: 2,
      answer: "A tangent line",
    },
    {
      id: 3,
      answer: "The area under the curve.",
    },
  ],
  [
    {
      id: 4,
      answer: "A point on a curve.",
    },
    {
      id: 5,
      answer: "A tangent line",
    },
    {
      id: 6,
      answer: "The area under the curve.",
    },
  ],
  [
    {
      id: 7,
      answer: "A point on a curve.",
    },
    {
      id: 8,
      answer: "A tangent line",
    },
    {
      id: 9,
      answer: "The area under the curve.",
    },
  ],
];
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
