import { useState } from "react";

import deleteQuiz from "./DeleteQuiz";

const DeleteBtn = ({ quizId, deleteQuizState }) => {
  const [confirm, toggleConfirm] = useState(false);

  const cancel = () => {
    toggleConfirm();
  };

  const delQuiz = () => {
    deleteQuiz(quizId);
    deleteQuizState(quizId);
  };

  return (
    <div className="delete-btn">
      {!confirm && <button onClick={toggleConfirm}>Delete</button>}
      {confirm && (
        <div>
          <button onClick={cancel}>Cancel</button>
          <button onClick={delQuiz}>Confirm</button>
        </div>
      )}
    </div>
  );
};

export default DeleteBtn;
