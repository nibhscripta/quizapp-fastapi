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
const apiUrl = "http://127.0.0.1:8000/";

const loginForm = document.getElementById("login-form");
loginForm.onsubmit = (e) => {
  e.preventDefault();
  const email = e.target.email.value;
  const password = e.target.password.value;
  const data = new FormData();
  data.append("username", email);
  data.append("password", password);

  const config = {
    method: "post",
    url: "/login",
    baseURL: apiUrl,
    data: data,
  };

  axios(config)
    .then(function (response) {
      const tokenData = JSON.stringify(response.data);
      console.log(tokenData);
    })
    .catch(function (error) {
      const errorData = error;
      console.log(errorData);
    });
};
