from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import date
from datetime import time

db = SQLAlchemy()

# User Model
class User_Info(db.Model):
    __tablename__ = "user_info"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.Integer, default=1)
    full_name = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    qualification = db.Column(db.String, nullable=False)
    scores = db.relationship("Score", cascade="all,delete", backref="user", lazy=True)

# Subject Model
class Subject(db.Model):
    __tablename__ = "subject"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    chapters = db.relationship("Chapter", cascade="all,delete", backref="subject", lazy=True)

# Chapter Model
class Chapter(db.Model):
    __tablename__ = "chapter"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    quizes = db.relationship("Quiz", cascade="all,delete", backref="chapter", lazy=True)

# Quiz Model
class Quiz(db.Model):
    __tablename__ = "quiz"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date_of_quiz = db.Column(db.Date, nullable=False)
    time_duration = db.Column(db.Integer, nullable=False)
    remarks = db.Column(db.Text, nullable=True, default="No remarks")
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id"), nullable=False)
    scores = db.relationship("Score", cascade="all,delete", backref="quiz", lazy=True)
    questions = db.relationship("Question", cascade="all,delete", backref="quiz", lazy=True)

# Question Model
class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.Text, nullable=False)
    option2 = db.Column(db.Text, nullable=False)
    option3 = db.Column(db.Text, nullable=False)
    option4 = db.Column(db.Text, nullable=False)
    correct_option = db.Column(db.String, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)

# Score Model
class Score(db.Model):
    __tablename__ = "score"
    id = db.Column(db.Integer, primary_key=True)
    time_stamp_of_attempt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_scored = db.Column(db.Integer, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user_info.id"), nullable=False)
