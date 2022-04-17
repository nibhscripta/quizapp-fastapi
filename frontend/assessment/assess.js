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
// render question fields
document.getElementById("app").insertAdjacentHTML(
  "beforeend",
  `
  <div class="assess-main" id="assess-main">
    <div id="quiz-title">Calculus</div>
    <div id="question-element">
      <div id="question">
      
      </div>
      <form id="answers">
        
      </form>
      <button id="next">Next</button>
      <button id="previous">Previous</button>
    </div>
  </div>
`
);
let questionIndex = 0;
function renderQuestion(qIndex) {
  const qText = document.getElementById("question");
  qText.innerText = questions[qIndex].question;
  const answersForm = document.getElementById("answers");
  while (answersForm.lastChild) {
    answersForm.removeChild(answersForm.lastChild);
  }
  answers[qIndex].forEach((answerDict) => {
    const answerInputElement = document.createElement("input");
    answerInputElement.setAttribute("name", questions[qIndex].id);
    answerInputElement.setAttribute("id", answerDict.id);
    answerInputElement.setAttribute("value", answerDict.id);
    answerInputElement.setAttribute("type", "radio");
    const answerLabel = document.createElement("label");
    answerLabel.setAttribute("for", answerDict.id);
    answerLabel.innerText = answerDict.answer;
    answersForm.appendChild(answerInputElement);
    answersForm.appendChild(answerLabel);
  });
  answersForm.onchange = (e) => {
    e.preventDefault();
    const answerID = e.target.value;
    const questionID = e.target.name;
    console.log(questionID);
  };
}
renderQuestion(questionIndex);
document.getElementById("next").onclick = () => {
  questionIndex += 1;
  if (questionIndex === questions.length) {
    questionIndex -= 1;
  } else {
    renderQuestion(questionIndex);
  }
};
document.getElementById("previous").onclick = () => {
  if (questionIndex === 0) {
  } else {
    questionIndex -= 1;
    renderQuestion(questionIndex);
  }
};
