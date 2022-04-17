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
questions.forEach((question) => {
  let questionFieldDiv = `
              <div class="quiz-question-field" id="quiz-question-field">
                <div class="quiz-question" id="quiz-question">
                </div>
                <div class="quiz-answers" id="quiz-answers">
                  <form>
                    
                  </form>
                </div>
              </div>
`;
  document
    .getElementById("assess-main")
    .insertAdjacentHTML("beforeend", questionFieldDiv);
});
let questionIndex = 0;
document.querySelectorAll("#quiz-question-field").forEach((field) => {
  const questionId = questions[questionIndex].id;
  const questionDiv = field.childNodes[1];
  const questionP = document.createElement("p");
  const questionText = document.createTextNode(
    questions[questionIndex].question
  );
  questionP.appendChild(questionText);
  questionDiv.appendChild(questionP);
  const answersForm = field.childNodes[3].querySelector("form");
  answersForm.onchange = (e) => {
    e.preventDefault();
    const answerId = e.target.value;
    console.log(questionId);
  };
  answers[questionIndex].forEach((answer) => {
    answersForm.insertAdjacentHTML(
      "beforeend",
      `
          <input type="radio" id="${answer.id}" name="${questions[questionIndex].id}" value="${answer.id}" /> 
          <label for="${answer.id}">${answer.answer}</label>   
    `
    );
  });
  questionIndex = questionIndex + 1;
});
