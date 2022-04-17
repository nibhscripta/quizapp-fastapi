// remove noscript warning
document.getElementById("noscript").remove();
// render home form
const app = document.getElementById("app");
const homeFormDiv = `
    <div class="home-main">
        <div class="home-quiz-form">
          <form id="start-quiz-form">
            <input type="text" name="quiz_id" placeholder="Enter Quiz ID" />
            <button type="submit">Start</button>
          </form>
          <div class="home-user-links">
            <a href="./quiz">Create a quiz</a>
            <a href="./login">Login</a>
          </div>
        </div>
      </div>
`;
app.insertAdjacentHTML("afterend", homeFormDiv);
