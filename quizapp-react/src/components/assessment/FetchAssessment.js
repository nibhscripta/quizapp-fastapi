import apiUrl from "../../utils/ApiUrl";

const fetchAssessment = async (id) => {
  let requestOptions = {
    method: "GET",

    redirect: "follow",
  };

  const res = await fetch(`${apiUrl}/a/${id}`, requestOptions);
  if (res.status === 200) {
    const data = res.json();
    return data;
  } else {
    console.log(res.status);
  }
};

export default fetchAssessment;
