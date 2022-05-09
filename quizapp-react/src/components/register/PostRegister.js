import apiUrl from "../../utils/ApiUrl";

const postRegister = async (username, password) => {
  const raw = JSON.stringify({
    email: username,
    password: password,
  });
  const requestOptions = {
    method: "POST",
    redirect: "follow",
    headers: {
      "Content-Type": "application/json",
    },
    body: raw,
  };
  const res = await fetch(`${apiUrl}/users`, requestOptions);
  if (res.status === 200) {
  } else {
    console.log(res.status);
  }
};

export default postRegister;
