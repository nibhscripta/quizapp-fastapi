import apiUrl from "../../utils/ApiUrl";

const postRegister = async (username, password) => {
  let formdata = new FormData();
  formdata.append("username", username);
  formdata.append("password", password);
  var requestOptions = {
    method: "POST",
    body: formdata,
    redirect: "follow",
  };
  const res = await fetch(`${apiUrl}/register`, requestOptions);
  if (res.status === 200) {
    const data = await res.json();
    const authToken = `${data.token_type} ${data.access_token}`;
    localStorage.setItem("authToken", JSON.stringify(authToken));
  } else {
    console.log(res.status);
  }
};

export default postRegister;
