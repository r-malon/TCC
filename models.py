from peewee import *
from datetime import datetime

db = SqliteDatabase('data.db', pragmas={
	'journal_mode': 'wal',
	'cache_size': -1024 * 16,
	'foreign_keys': 0,
	'ignore_check_constraints': 0
})

class BaseModel(Model):
	class Meta:
		database = db


class Student(BaseModel):
	name = TextField()
	enrollment = IntegerField()

class Teacher(BaseModel):
	name = TextField()

class Assessment(BaseModel):
	date = DateTimeField(default=datetime.utcnow)
	n_choices = IntegerField()
	n_questions = IntegerField()
