import apiUrl from "../../utils/ApiUrl";

const fetchQuizList = async () => {
  const authToken = JSON.parse(localStorage.getItem("authToken"));

  let myHeaders = new Headers();
  myHeaders.append("Authorization", authToken);

  let requestOptions = {
    method: "GET",
    headers: myHeaders,
    redirect: "follow",
  };

  const res = await fetch(`${apiUrl}/q`, requestOptions);

  if (res.status === 200) {
    const data = res.json();
    return data;
  } else {
    console.log(res.status);
  }
};

export default fetchQuizList;
