// remove noscript warning
document.getElementById("noscript").remove();
// render login form
const app = document.getElementById("app");
const loginFormDiv = `
    <div class="login-main">
        <div class="login-form">
            <form id="login-form">
                <input type="text" name="email" placeholder="Email" />
                <input type="password" name="password" placeholder="password" />
                <button type="submit">Login</button>
            </form>
        </div>
    </div>
`;
app.insertAdjacentHTML("beforeend", loginFormDiv);
// handle login submission
const loginForm = document.getElementById("login-form");
loginForm.onsubmit = (e) => {
  e.preventDefault();
  const email = e.target.email.value;
  const password = e.target.password.value;
};
