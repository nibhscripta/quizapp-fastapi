import apiUrl from "../../utils/ApiUrl";

const authToken = JSON.parse(localStorage.getItem("authToken"));

const fetchQuizList = async () => {
  let myHeaders = new Headers();
  myHeaders.append("Authorization", authToken);

  let requestOptions = {
    method: "GET",
    headers: myHeaders,
    redirect: "follow",
  };

  const res = await fetch(`${apiUrl}/q`, requestOptions);
  const data = res.json();
  return data;
};

export default fetchQuizList;
