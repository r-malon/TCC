from flask import *
from models import *

@app.before_first_request
def first_run():
	try:
		db.create_tables([
			Student, Assessment, StudentAssessment, 
			Question, AssessmentQuestion, Answer, Grade, Tag, QuestionTag
		])
	except Exception as e:
		app.logger.error(e)
		db.close()

@app.before_request
def before_run():
	try:
		db.connect()
	except Exception as e:
		app.logger.error(e)
		db.close()

@app.teardown_request
def teardown(error=None):
	db.close()
	if error:
		app.logger.error(error)


@app.route('/<username>/<int:student_id>')
def get_student(username, student_id):
	return render_template()

@app.route('/top/<int:n>')
def top_n(n):
	return render_template()

@app.route('/<int:assessment_id>')
def get_assessment(assessment_id):
	return render_template()


@app.errorhandler(404)
def not_found(e):
	return render_template('404.html'), 404

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
