import apiUrl from "../../utils/ApiUrl";

const FetchAuthToken = async (username, password) => {
  let loginHeaders = new Headers();
  let formdata = new FormData();
  formdata.append("username", username);
  formdata.append("password", password);
  var requestOptions = {
    method: "POST",
    headers: loginHeaders,
    body: formdata,
    redirect: "follow",
  };
  const res = await fetch(`${apiUrl}/login`, requestOptions);
  if (res.status === 200) {
    const data = await res.json();
    const authToken = `${data.token_type} ${data.access_token}`;
    localStorage.setItem("authToken", JSON.stringify(authToken));
  } else {
    console.log(res.status);
    return res.status;
  }
};

export default FetchAuthToken;
