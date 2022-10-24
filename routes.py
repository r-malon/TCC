from flask import *
from models import *
from datetime import date

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


@app.route('/user/<int:user_id>')
@app.route('/student/<int:user_id>')
def get_user(user_id):
	try:
		query = Student.get(Student.enrollment == user_id)
		return render_template()
	except Exception as e:
		flash('User not found')
		return redirect('/home')

@app.route('/top/<int:n>')
def top_n(n):
	query = Student.grades.desc().limit(n)
	return render_template()

@app.route('/<int:assessment_id>')
def get_assessment(assessment_id):
	return render_template()

@app.route('/assessment')
def build_assessment():
	request.args.get()
	return render_template('answer_sheet.html', 
		date=date.today().strftime('%A, %d/%m/%Y'))


@app.errorhandler(404)
def not_found(e):
	return render_template('404.html'), 404

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
