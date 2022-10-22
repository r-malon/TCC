from peewee import *
from datetime import datetime

db = SqliteDatabase('static/data.db', pragmas={
	'journal_mode': 'wal',
	'cache_size': -1024 * 16,
	'foreign_keys': 1,
	'ignore_check_constraints': 0
})

class BaseModel(Model):
	class Meta:
		database = db


class Student(BaseModel):
	enrollment = IntegerField(unique=True)
	username = CharField(max_length=22)
	name = TextField()

class Assessment(BaseModel):
	date = DateTimeField(default=datetime.utcnow)
	n_choices = IntegerField() # for answer sheet
	n_questions = IntegerField()

class Question(BaseModel):
	statement = TextField()
#	interpret_html = BooleanField(default=True)

class Tag(BaseModel):
	tag = CharField(max_length=20, unique=True)

class QuestionTag(BaseModel):
	question = ForeignKeyField(Question)
	tag = ForeignKeyField(Tag)

class Answer(BaseModel):
	question = ForeignKeyField(Question, backref='answers')
	statement = TextField()

class StudentAssessment(BaseModel):
	student = ForeignKeyField(Student)
	assessment = ForeignKeyField(Assessment)

class AssessmentQuestion(BaseModel):
	question = ForeignKeyField(Question)
	assessment = ForeignKeyField(Assessment)

class Grade(BaseModel):
	student = ForeignKeyField(Student, backref='grades')
	assessment = ForeignKeyField(Assessment, backref='grades')
	grade = IntegerField()
	comment = TextField()
