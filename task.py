class Task:
    _id_counter = 1  # auto id

    def __init__(self, title, done=False):
        self.id = Task._id_counter
        Task._id_counter += 1
        self.title = title
        self.status = 'completed' if done else 'not-completed'

    def toggle(self):
        # flip status
        self.status = 'completed' if self.status == 'not-completed' else 'not-completed'

    def __repr__(self):
        return f"<Task id={self.id} title='{self.title}' status={self.status}>"
