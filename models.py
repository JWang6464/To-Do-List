from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    # one-to-many: user -> tasks
    tasks = db.relationship(
        'Task',
        backref='user',
        lazy='dynamic',      
        cascade='all, delete-orphan'   
    )

    def set_password(self, password):
        """Hash the password and store it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='not-completed', nullable=False)  # completed / not-completed
    priority = db.Column(db.String(10), default='low', nullable=False)  # low / medium / high
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)

    def toggle(self):
        """Mark the task as done/undone."""
        self.status = 'completed' if self.status == 'not-completed' else 'not-completed'

    def __repr__(self):
        return f"<Task id={self.id} title='{self.title}' status={self.status} priority={self.priority}>"
