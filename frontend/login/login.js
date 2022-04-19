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
loginForm.onsubmit = async (e) => {
  e.preventDefault();
  const email = e.target.email.value;
  const password = e.target.password.value;
  const loginData = new FormData();
  loginData.append("username", email);
  loginData.append("password", password);

  const axiosConfig = {
    method: "post",
    url: "/login",
    baseURL: apiUrl,
    data: loginData,
  };

  await axios(axiosConfig)
    .then(function (response) {
      let tokenData = JSON.stringify(response.data);
      tokenData = JSON.parse(tokenData);
      localStorage.setItem("access_token", tokenData["access_token"]);
      window.location.replace(window.location.href.replace("login", "quiz"));
    })
    .catch(function (error) {
      const errorData = error;
      console.log(errorData);
    });
};
