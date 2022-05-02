import apiUrl from "../../utils/ApiUrl";

const authToken = JSON.parse(localStorage.getItem("authToken"));

const fetchQuestionList = async (id) => {
  let myHeaders = new Headers();
  myHeaders.append("Authorization", authToken);

  let requestOptions = {
    method: "GET",
    headers: myHeaders,
    redirect: "follow",
  };

  const res = await fetch(`${apiUrl}/ques?quiz_id=${id}`, requestOptions);
  const data = res.json();
  return data;
};

export default fetchQuestionList;
