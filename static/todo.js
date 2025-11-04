


// remove task button
// const removeTaskButtons = document.querySelectorAll('.remove-btn');
// removeTaskButtons.forEach(button => {
//   button.addEventListener('click', (event) => {
//     event.preventDefault();
//     const taskId = button.getAttribute('task-id');
//     console.log(`Removing task with ID: ${taskId}`);
//     fetch(`/remove/${taskId}`, { method: 'GET' })
//       .then(response => {
//         if (response.ok) {
//           button.closest('li').remove();
//         }
//       });
//   });
// });


// remove task (delegated)
document.addEventListener('click', (e) => {
  const btn = e.target.closest('.remove-btn');
  if (!btn) return;

  e.preventDefault();

  const id = btn.dataset.taskId || btn.getAttribute('task-id');
  if (!id) return;

  fetch(`/remove/${id}`, { method: 'POST' }) 
    .then((res) => {
      if (!res.ok) throw new Error('remove failed');
      const li = btn.closest('li');
      if (li) li.remove();     
    })
    .catch(console.error);
});
