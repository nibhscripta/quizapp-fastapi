import { useState } from "react";

const DeleteQuestionBtn = ({ id, deleteQuestionState }) => {
  const [confirmBtn, toggleConfirm] = useState(false);

  const cancel = () => {
    toggleConfirm();
  };

  const deleteEvent = () => {
    deleteQuestionState(id);
  };

  return (
    <>
      {!confirmBtn && <button onClick={toggleConfirm}>Delete</button>}
      {confirmBtn && (
        <>
          <button onClick={cancel}>Cancel</button>
          <button onClick={deleteEvent}>Confirm</button>
        </>
      )}
    </>
  );
};

export default DeleteQuestionBtn;
