import apiUrl from "../../utils/ApiUrl";

const authToken = JSON.parse(localStorage.getItem("authToken"));

const deleteAnswer = async (id) => {
  let requestOptions = {
    method: "DELETE",
    redirect: "follow",
    headers: {
      Authorization: authToken,
      "Content-Type": "application/json",
    },
  };

  const res = await fetch(`${apiUrl}/ans/${id}`, requestOptions);
  if (res.status !== 204) {
    console.log(res.status);
  }
};

export default deleteAnswer;
