function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/notes";
  });
}


function deleteContact(contactId) {
  fetch("/delete-contact", {
    method: "POST",
    body: JSON.stringify({ contactId: contactId }),
  }).then((_res) => {
    window.location.href = "/contacts";
  });
}


function deleteTask(taskId) {
  fetch("/delete-task", {
    method: "POST",
    body: JSON.stringify({ taskid: taskId }),
  }).then((_res) => {
    window.location.href = "/todo";
  });
}
