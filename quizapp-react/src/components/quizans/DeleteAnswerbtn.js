import { useState } from "react";

const DeleteAnswerBtn = ({ id, deleteAnswerState }) => {
  const [confirmBtn, toggleConfirm] = useState(false);

  const cancel = () => {
    toggleConfirm();
  };

  const deleteEvent = () => {
    deleteAnswerState(id);
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

export default DeleteAnswerBtn;
