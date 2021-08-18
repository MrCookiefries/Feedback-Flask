from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()

def connect_db(app):
    """connects app to database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """model for users"""
    __tablename__ = "users"
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship("Feedback", backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        usr = self.username; email = self.email
        first = self.first_name; last = self.last_name
        return f"<User username={usr} email={email} first_name={first} last_name={last}>"
    
    @property
    def full_name(self):
        """combines first and last name"""
        return f"{self.first_name} {self.last_name}"
    
    @classmethod
    def register(cls, data):
        """registers a new user"""
        data["password"] = bcrypt.generate_password_hash(data["password"]).decode("utf8")
        return cls(**data)
    
    @classmethod
    def authenticate(cls, username, password):
        """checks if user credentials exist"""
        user = cls.query.filter_by(username = username).one_or_none()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        return False

class Feedback(db.Model):
    """model for feedback"""
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey("users.username"), nullable=False)

    def __repr__(self):
        id = self.id; title = self.title; username = self.username
        return f"<Feedback id={id} title={title} username={username}>"

